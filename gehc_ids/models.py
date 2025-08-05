"""Data models for the GE HealthCare IDS SDK."""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator
import re


class Collection(BaseModel):
    """Model for a Vector Store collection."""
    
    id: Optional[str] = Field(None, alias="_id")
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    status: str = "active"
    model_id: str = "model_ada002_beta_embeddings"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @validator('title')
    def validate_title(cls, v):
        """Validate title doesn't contain special characters."""
        forbidden_chars = r'[~!%^()+={}\[\]|\\;"\',<>?/$]'
        if re.search(forbidden_chars, v):
            raise ValueError("Title contains forbidden special characters")
        return v

    class Config:
        populate_by_name = True


class Document(BaseModel):
    """Model for a document in Vector Store."""
    
    id: Optional[str] = Field(None, alias="document_id")
    name: str = Field(..., alias="document_name")
    collection_id: str
    file_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    chunks: Optional[List[str]] = None
    status: Optional[str] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class FileUpload(BaseModel):
    """Model for file upload information."""
    
    file_name: str
    url: str
    fields: Dict[str, str]


class Batch(BaseModel):
    """Model for batch operations."""
    
    id: Optional[str] = Field(None, alias="batch_id")
    name: str = Field(..., alias="batch_name")
    description: Optional[str] = Field(None, alias="batch_description")
    collection_id: str
    file_list: List[str]
    metadata: Optional[Dict[str, Any]] = None
    pre_signed_urls: Optional[List[FileUpload]] = None
    files: Optional[Dict[str, Document]] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class SearchResult(BaseModel):
    """Model for semantic search results."""
    
    document_id: str
    content: str
    score: float
    metadata: Optional[Dict[str, Any]] = None


class RAGResponse(BaseModel):
    """Model for RAG query responses."""
    
    answer: str
    sources: List[SearchResult]
    metadata: Optional[Dict[str, Any]] = None


class PromptTemplate(BaseModel):
    """Model for prompt templates."""
    
    id: Optional[str] = Field(None, alias="_id")
    name: str
    type: str = "System"
    provider: str = "OpenAI"
    content: str
    params: Union[str, Dict[str, Any]] = "{}"
    category: str = "completion"
    tags: Optional[List[str]] = None
    version: Optional[int] = None
    default: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator('content')
    def validate_content(cls, v):
        """Validate content contains required variables."""
        if '{context}' not in v.lower() or '{question}' not in v.lower():
            raise ValueError("Content must include {context} and {question} variables")
        return v

    class Config:
        populate_by_name = True


# Request Models
class CreateCollectionRequest(BaseModel):
    """Request model for creating a collection."""
    
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    status: str = "active"
    model_id: str = "model_ada002_beta_embeddings"


class CreateBatchRequest(BaseModel):
    """Request model for creating a batch."""
    
    collection_id: str
    file_list: List[str]
    batch_name: str
    batch_description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AddChunksRequest(BaseModel):
    """Request model for adding chunks to collection."""
    
    collection_id: str
    document_id: str
    document_name: str
    chunk: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class SemanticSearchRequest(BaseModel):
    """Request model for semantic search."""
    
    collection_id: str
    query: str
    limit: Optional[int] = 10
    metadata: Optional[Dict[str, Any]] = None


class RAGQueryRequest(BaseModel):
    """Request model for RAG queries."""
    
    collection_id: str
    message: str
    limit: Optional[int] = 10
    metadata: Optional[Dict[str, Any]] = None


class CreatePromptRequest(BaseModel):
    """Request model for creating a prompt template."""
    
    name: str
    type: str = "System"
    provider: str = "OpenAI"
    content: str
    params: Union[str, Dict[str, Any]] = "{}"
    category: str = "completion"
    tags: Optional[List[str]] = None


class UpdatePromptRequest(BaseModel):
    """Request model for updating a prompt template."""
    
    type: Optional[str] = None
    provider: Optional[str] = None
    content: Optional[str] = None
    params: Optional[Union[str, Dict[str, Any]]] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class SetDefaultPromptRequest(BaseModel):
    """Request model for setting default prompt version."""
    
    justification: Optional[str] = None


# Response Models
class CollectionListResponse(BaseModel):
    """Response model for listing collections."""
    
    collections: List[Collection]


class DocumentListResponse(BaseModel):
    """Response model for listing documents."""
    
    documents: List[Document]
    total_count: Optional[int] = None
    page: Optional[int] = None
    size: Optional[int] = None


class PromptListResponse(BaseModel):
    """Response model for listing prompts."""
    
    prompts: List[PromptTemplate]
    total_count: Optional[int] = Field(None, alias="totalCount")
    total_pages: Optional[int] = Field(None, alias="totalPages")
    next_page: Optional[int] = Field(None, alias="nextPage")

    class Config:
        populate_by_name = True


class HealthCheckResponse(BaseModel):
    """Response model for health checks."""
    
    status: str
    message: str


class RecordCountResponse(BaseModel):
    """Response model for record count."""
    
    count: int
    collection_id: str