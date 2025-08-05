"""Unified client for GE HealthCare Intelligent Data Store SDK."""

from typing import Optional

from .auth import IDSAuth
from .vector_store import VectorStoreClient
from .prompt_store import PromptStoreClient


class IDSClient:
    """
    Unified client for GE HealthCare Intelligent Data Store.
    
    Provides access to both Vector Store and Prompt Store services
    through a single interface.
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        audience: str,
        vector_store_url: str = "https://ids-test.ailab.gehealthcare.com/api/v1",
        prompt_store_url: str = "https://prompt-test.ailab.gehealthcare.com",
        idam_url: str = "https://idam.gehealthcloud.io/oauth2/token",
        verify_ssl: bool = True,
        timeout: int = 30
    ):
        """
        Initialize IDS client with authentication and service URLs.
        
        Args:
            client_id: Application client ID from IDAM
            client_secret: Application client secret from IDAM
            audience: IDS audience identifier
            vector_store_url: Vector Store service URL
            prompt_store_url: Prompt Store service URL
            idam_url: IDAM token endpoint URL
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
        """
        # Initialize authentication
        self.auth = IDSAuth(
            client_id=client_id,
            client_secret=client_secret,
            audience=audience,
            idam_url=idam_url,
            verify_ssl=verify_ssl
        )
        
        # Initialize service clients
        self.vector_store = VectorStoreClient(
            auth=self.auth,
            base_url=vector_store_url,
            verify_ssl=verify_ssl,
            timeout=timeout
        )
        
        self.prompt_store = PromptStoreClient(
            auth=self.auth,
            base_url=prompt_store_url,
            verify_ssl=verify_ssl,
            timeout=timeout
        )
    
    @classmethod
    def from_environment(
        cls,
        client_id_env: str = "IDS_CLIENT_ID",
        client_secret_env: str = "IDS_CLIENT_SECRET",
        audience_env: str = "IDS_AUDIENCE",
        **kwargs
    ) -> "IDSClient":
        """
        Create client from environment variables.
        
        Args:
            client_id_env: Environment variable name for client ID
            client_secret_env: Environment variable name for client secret
            audience_env: Environment variable name for audience
            **kwargs: Additional arguments passed to constructor
            
        Returns:
            Configured IDS client
            
        Raises:
            ValueError: If required environment variables are not set
        """
        import os
        
        client_id = os.getenv(client_id_env)
        client_secret = os.getenv(client_secret_env)
        audience = os.getenv(audience_env)
        
        if not client_id:
            raise ValueError(f"Environment variable {client_id_env} is not set")
        if not client_secret:
            raise ValueError(f"Environment variable {client_secret_env} is not set")
        if not audience:
            raise ValueError(f"Environment variable {audience_env} is not set")
        
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            audience=audience,
            **kwargs
        )
    
    def health_check(self) -> dict:
        """
        Check health of all IDS services.
        
        Returns:
            Dictionary with health status of each service
        """
        health_status = {}
        
        try:
            vs_health = self.vector_store.health_check_vector_db()
            health_status["vector_store"] = {
                "status": vs_health.status,
                "message": vs_health.message
            }
        except Exception as e:
            health_status["vector_store"] = {
                "status": "Error",
                "message": str(e)
            }
        
        try:
            query_health = self.vector_store.health_check_query_service()
            health_status["query_service"] = {
                "status": query_health.status,
                "message": query_health.message
            }
        except Exception as e:
            health_status["query_service"] = {
                "status": "Error",
                "message": str(e)
            }
        
        try:
            batch_health = self.vector_store.health_check_batch_service()
            health_status["batch_service"] = {
                "status": batch_health.status,
                "message": batch_health.message
            }
        except Exception as e:
            health_status["batch_service"] = {
                "status": "Error",
                "message": str(e)
            }
        
        try:
            prompt_health = self.prompt_store.health_check()
            health_status["prompt_store"] = {
                "status": prompt_health.status,
                "message": prompt_health.message
            }
        except Exception as e:
            health_status["prompt_store"] = {
                "status": "Error",
                "message": str(e)
            }
        
        return health_status
    
    def refresh_token(self) -> None:
        """Force refresh of authentication token."""
        self.auth.invalidate_token()
        self.auth.get_access_token(force_refresh=True)
    
    def get_token_info(self) -> dict:
        """
        Get information about the current authentication token.
        
        Returns:
            Dictionary with token information
        """
        return {
            "has_token": self.auth._access_token is not None,
            "token_expires_at": self.auth._token_expires_at,
            "is_expired": self.auth._is_token_expired()
        }