"""Authentication module for GE HealthCare IDS SDK."""

import base64
import uuid
import time
from typing import Optional, Dict, Any
import requests
from .exceptions import AuthenticationError


class IDSAuth:
    """
    Authentication handler for GE HealthCare IDAM.
    
    Manages OAuth2 client credentials flow and token caching.
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        audience: str,
        idam_url: str = "https://idam.gehealthcloud.io/oauth2/token",
        verify_ssl: bool = True
    ):
        """
        Initialize IDAM authentication.
        
        Args:
            client_id: Application client ID from IDAM
            client_secret: Application client secret from IDAM
            audience: IDS audience identifier
            idam_url: IDAM token endpoint URL
            verify_ssl: Whether to verify SSL certificates
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.audience = audience
        self.idam_url = idam_url
        self.verify_ssl = verify_ssl
        
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[float] = None
        self._token_buffer_seconds = 300  # Refresh 5 minutes before expiry
    
    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Get a valid access token, refreshing if necessary.
        
        Args:
            force_refresh: Force token refresh even if current token is valid
            
        Returns:
            Valid access token
            
        Raises:
            AuthenticationError: If authentication fails
        """
        if force_refresh or self._is_token_expired():
            self._refresh_token()
        
        if not self._access_token:
            raise AuthenticationError("Failed to obtain access token")
            
        return self._access_token
    
    def _is_token_expired(self) -> bool:
        """Check if the current token is expired or about to expire."""
        if not self._access_token or not self._token_expires_at:
            return True
        
        current_time = time.time()
        return current_time >= (self._token_expires_at - self._token_buffer_seconds)
    
    def _refresh_token(self) -> None:
        """
        Refresh the access token using client credentials flow.
        
        Raises:
            AuthenticationError: If token refresh fails
        """
        try:
            # Prepare basic auth credentials
            basic_auth_creds = f"{self.client_id}:{self.client_secret}"
            basic_auth_creds = base64.b64encode(basic_auth_creds.encode()).decode("ascii")
            
            # Prepare request
            payload = (
                f"grant_type=client_credentials"
                f"&scope={uuid.uuid4()}"
                f"&audience={self.audience}"
            )
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {basic_auth_creds}",
            }
            
            # Make token request
            response = requests.post(
                self.idam_url,
                headers=headers,
                data=payload,
                verify=self.verify_ssl,
                timeout=30
            )
            
            if response.status_code != 200:
                raise AuthenticationError(
                    f"Failed to obtain access token: {response.status_code} {response.text}",
                    response.status_code,
                    response.json() if response.headers.get('content-type') == 'application/json' else {}
                )
            
            token_data = response.json()
            self._access_token = token_data["access_token"]
            
            # Calculate expiry time (default to 1 hour if not provided)
            expires_in = token_data.get("expires_in", 3600)
            self._token_expires_at = time.time() + expires_in
            
        except requests.RequestException as e:
            raise AuthenticationError(f"Token request failed: {str(e)}")
        except KeyError as e:
            raise AuthenticationError(f"Invalid token response format: missing {str(e)}")
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary with Authorization header
        """
        token = self.get_access_token()
        return {"Authorization": f"Bearer {token}"}
    
    def invalidate_token(self) -> None:
        """Invalidate the current token, forcing a refresh on next use."""
        self._access_token = None
        self._token_expires_at = None


class APIKeyAuth:
    """
    Simple API key authentication (if supported by IDS in the future).
    """
    
    def __init__(self, api_key: str):
        """
        Initialize API key authentication.
        
        Args:
            api_key: The API key for authentication
        """
        self.api_key = api_key
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary with API key header
        """
        return {"X-API-Key": self.api_key}
    
    def get_access_token(self) -> str:
        """Return the API key as the access token."""
        return self.api_key