"""Custom exceptions for the GE HealthCare IDS SDK."""

from typing import Optional, Dict, Any


class IDSException(Exception):
    """Base exception class for all IDS SDK errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(IDSException):
    """Raised when authentication fails (401, 403)."""
    pass


class ValidationError(IDSException):
    """Raised when request validation fails (400, 422)."""
    pass


class NotFoundError(IDSException):
    """Raised when a resource is not found (404)."""
    pass


class ConflictError(IDSException):
    """Raised when there's a conflict with the request (409)."""
    pass


class PayloadTooLargeError(IDSException):
    """Raised when the request payload is too large (413)."""
    pass


class ServerError(IDSException):
    """Raised when there's a server error (500, 502, 504)."""
    pass


class GatewayTimeoutError(ServerError):
    """Raised when the gateway times out (504)."""
    pass


class TooManyRequestsError(IDSException):
    """Raised when rate limit is exceeded (429)."""
    pass


def raise_for_status(response) -> None:
    """
    Raise appropriate exception based on HTTP status code.
    
    Args:
        response: HTTP response object
        
    Raises:
        IDSException: Appropriate exception based on status code
    """
    status_code = response.status_code
    
    try:
        response_data = response.json()
    except:
        response_data = {"error": response.text}
    
    message = response_data.get("message", f"HTTP {status_code} error")
    
    if status_code == 400:
        raise ValidationError(message, status_code, response_data)
    elif status_code == 401:
        raise AuthenticationError(message, status_code, response_data)
    elif status_code == 403:
        raise AuthenticationError(message, status_code, response_data)
    elif status_code == 404:
        raise NotFoundError(message, status_code, response_data)
    elif status_code == 409:
        raise ConflictError(message, status_code, response_data)
    elif status_code == 413:
        raise PayloadTooLargeError(message, status_code, response_data)
    elif status_code == 422:
        raise ValidationError(message, status_code, response_data)
    elif status_code == 429:
        raise TooManyRequestsError(message, status_code, response_data)
    elif status_code == 500:
        raise ServerError(message, status_code, response_data)
    elif status_code == 502:
        raise ServerError(message, status_code, response_data)
    elif status_code == 504:
        raise GatewayTimeoutError(message, status_code, response_data)
    elif status_code >= 400:
        raise IDSException(message, status_code, response_data)