"""
GE HealthCare Intelligent Data Store SDK

A Python SDK for interacting with GE HealthCare's AI Fabric Intelligent Data Store,
including Vector Store and Prompt Store services.
"""

__version__ = "1.0.0"
__author__ = "GE HealthCare"
__email__ = "ai-fabric@gehealthcare.com"

from .client import IDSClient
from .vector_store import VectorStoreClient
from .prompt_store import PromptStoreClient
from .auth import IDSAuth
from .models import *
from .exceptions import *

__all__ = [
    "IDSClient",
    "VectorStoreClient", 
    "PromptStoreClient",
    "IDSAuth",
    # Models
    "Collection",
    "Document", 
    "Batch",
    "PromptTemplate",
    "SearchResult",
    "RAGResponse",
    # Exceptions
    "IDSException",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "ServerError",
]