"""Vector Store client for GE HealthCare IDS SDK."""

import os
import time
from typing import Dict, List, Optional, Any, Union, BinaryIO
import requests
from urllib.parse import urljoin

from .auth import IDSAuth
from .exceptions import raise_for_status
from .models import (
    Collection, Document, Batch, SearchResult, RAGResponse,
    CreateCollectionRequest, CreateBatchRequest, AddChunksRequest,
    SemanticSearchRequest, RAGQueryRequest, CollectionListResponse,
    DocumentListResponse, HealthCheckResponse, RecordCountResponse
)


class VectorStoreClient:
    """
    Client for interacting with GE HealthCare Vector Store API.
    
    Provides methods for managing collections, documents, and performing
    semantic search and RAG queries.
    """
    
    def __init__(
        self,
        auth: IDSAuth,
        base_url: str = "https://ids-test.ailab.gehealthcare.com/api/v1",
        verify_ssl: bool = True,
        timeout: int = 30
    ):
        """
        Initialize Vector Store client.
        
        Args:
            auth: Authentication handler
            base_url: Base URL for Vector Store API
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
        """
        self.auth = auth
        self.base_url = base_url.rstrip('/')
        self.verify_ssl = verify_ssl
        self.timeout = timeout
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """Make an authenticated HTTP request."""
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        
        request_headers = {
            "Accept": "application/json",
            **self.auth.get_auth_headers()
        }
        
        if json_data is not None:
            request_headers["Content-Type"] = "application/json"
        
        if headers:
            request_headers.update(headers)
        
        response = requests.request(
            method=method,
            url=url,
            json=json_data,
            params=params,
            files=files,
            data=data,
            headers=request_headers,
            verify=self.verify_ssl,
            timeout=self.timeout
        )
        
        if response.status_code >= 400:
            raise_for_status(response)
        
        return response

    # Health Check Methods
    
    def health_check_vector_db(self) -> HealthCheckResponse:
        """
        Check health of Vector DB service.
        
        Returns:
            Health check response
        """
        response = self._make_request("GET", "/check-connection")
        return HealthCheckResponse(status="Healthy", message="Vector DB service is running")
    
    def health_check_query_service(self) -> HealthCheckResponse:
        """
        Check health of Query service.
        
        Returns:
            Health check response
        """
        response = self._make_request("GET", "/doc_query/health_check")
        return HealthCheckResponse(status="Healthy", message="Query service is running")
    
    def health_check_batch_service(self) -> HealthCheckResponse:
        """
        Check health of Batch service.
        
        Returns:
            Health check response
        """
        response = self._make_request("GET", "/batch/health_check")
        return HealthCheckResponse(status="Healthy", message="Batch service is running")

    # Collection Management Methods
    
    def create_collection(
        self,
        title: str,
        description: Optional[str] = None,
        status: str = "active",
        model_id: str = "model_ada002_beta_embeddings"
    ) -> Collection:
        """
        Create a new collection.
        
        Args:
            title: Unique name for the collection (3-100 chars, no special chars)
            description: Optional description
            status: Collection status (default: "active")
            model_id: Model ID for embeddings
            
        Returns:
            Created collection
        """
        request_data = CreateCollectionRequest(
            title=title,
            description=description,
            status=status,
            model_id=model_id
        )
        
        response = self._make_request("POST", "/collections", json_data=request_data.dict())
        response_data = response.json()
        
        # Extract collection ID from response message
        collection_id = response_data["response"].split(":")[1].strip()
        
        return Collection(
            id=collection_id,
            title=title,
            description=description,
            status=status,
            model_id=model_id
        )
    
    def list_collections(self) -> List[Collection]:
        """
        List all collections for the authenticated application.
        
        Returns:
            List of collections
        """
        response = self._make_request("GET", "/collections")
        response_data = response.json()
        
        collections = []
        for collection_data in response_data.get("collections", []):
            collections.append(Collection(**collection_data))
        
        return collections
    
    def delete_collection(self, collection_id: str, soft_delete: bool = True) -> bool:
        """
        Delete a collection.
        
        Args:
            collection_id: ID of collection to delete
            soft_delete: If True, soft delete; if False, hard delete
            
        Returns:
            True if successful
        """
        params = {"soft_delete": str(soft_delete).lower()}
        response = self._make_request("DELETE", f"/collections/{collection_id}", params=params)
        return response.status_code == 200

    # Document Management Methods
    
    def create_batch(
        self,
        collection_id: str,
        file_list: List[str],
        batch_name: str,
        batch_description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Batch:
        """
        Create a batch for document upload.
        
        Args:
            collection_id: Target collection ID
            file_list: List of file names to upload
            batch_name: Name for the batch
            batch_description: Optional batch description
            metadata: Optional metadata
            
        Returns:
            Created batch with pre-signed URLs
        """
        request_data = CreateBatchRequest(
            collection_id=collection_id,
            file_list=file_list,
            batch_name=batch_name,
            batch_description=batch_description,
            metadata=metadata or {}
        )
        
        response = self._make_request("POST", "/batch/create", json_data=request_data.dict())
        response_data = response.json()
        
        return Batch(**response_data)
    
    def upload_file_to_s3(self, presigned_url: str, fields: Dict[str, str], file_path: str) -> bool:
        """
        Upload a file using pre-signed URL.
        
        Args:
            presigned_url: Pre-signed S3 URL
            fields: Form fields for the upload
            file_path: Path to the file to upload
            
        Returns:
            True if successful
        """
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            
            response = requests.post(
                presigned_url,
                data=fields,
                files=files,
                verify=self.verify_ssl,
                timeout=self.timeout
            )
        
        return response.status_code in (201, 204)
    
    def get_batch_status(self, batch_id: str) -> Batch:
        """
        Get status of a batch.
        
        Args:
            batch_id: ID of the batch
            
        Returns:
            Batch with current status
        """
        response = self._make_request("GET", f"/batch/{batch_id}")
        response_data = response.json()
        
        return Batch(**response_data)
    
    def wait_for_batch_completion(
        self,
        batch_id: str,
        poll_interval: int = 20,
        max_wait_time: int = 3600
    ) -> Batch:
        """
        Wait for batch processing to complete.
        
        Args:
            batch_id: ID of the batch
            poll_interval: Seconds between status checks
            max_wait_time: Maximum time to wait in seconds
            
        Returns:
            Final batch status
            
        Raises:
            TimeoutError: If batch doesn't complete within max_wait_time
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            batch = self.get_batch_status(batch_id)
            
            if batch.files:
                total_files = len(batch.files)
                completed_files = sum(
                    1 for file_info in batch.files.values()
                    if file_info.status in ("success", "failed")
                )
                
                if completed_files == total_files:
                    return batch
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Batch {batch_id} did not complete within {max_wait_time} seconds")
    
    def get_batches(
        self,
        detailed: bool = False,
        limit: int = 10,
        last_evaluated_batch_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get batches for the client.
        
        Args:
            detailed: Get detailed failure information
            limit: Number of batches per response
            last_evaluated_batch_id: For pagination
            
        Returns:
            Batch information
        """
        request_data = {
            "detailed": detailed,
            "limit": limit,
            "last_evaluated_batch_id": last_evaluated_batch_id
        }
        
        response = self._make_request("POST", "/batch/batches", json_data=request_data)
        return response.json()
    
    def add_chunks_to_collection(
        self,
        collection_id: str,
        document_id: str,
        document_name: str,
        chunks: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add custom chunks to a collection.
        
        Args:
            collection_id: Target collection ID
            document_id: Client-generated document ID
            document_name: Name for the document
            chunks: List of text chunks
            metadata: Optional metadata
            
        Returns:
            True if successful
        """
        request_data = AddChunksRequest(
            collection_id=collection_id,
            document_id=document_id,
            document_name=document_name,
            chunk=chunks,
            metadata=metadata
        )
        
        response = self._make_request("POST", "/collections/store", json_data=request_data.dict())
        return response.status_code == 200
    
    def list_documents(
        self,
        collection_id: str,
        only_deleted: bool = False,
        page: Optional[int] = None,
        size: Optional[int] = None
    ) -> DocumentListResponse:
        """
        List documents in a collection.
        
        Args:
            collection_id: Collection ID
            only_deleted: Show only deleted documents
            page: Page number for pagination
            size: Number of documents per page
            
        Returns:
            Document list response
        """
        params = {
            "collection_id": collection_id,
            "only_deleted": only_deleted
        }
        
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        
        response = self._make_request("GET", "/collections/documents", params=params)
        response_data = response.json()
        
        documents = []
        for doc_data in response_data.get("documents", []):
            documents.append(Document(**doc_data))
        
        return DocumentListResponse(
            documents=documents,
            total_count=response_data.get("total_count"),
            page=response_data.get("page"),
            size=response_data.get("size")
        )
    
    def delete_document(
        self,
        collection_id: str,
        document_id: str,
        soft_delete: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Delete a document from a collection.
        
        Args:
            collection_id: Collection ID
            document_id: Document ID
            soft_delete: If True, soft delete; if False, hard delete
            metadata: Optional metadata
            
        Returns:
            True if successful
        """
        params = {"soft_delete": str(soft_delete).lower()}
        if metadata:
            params["metadata"] = metadata
        
        response = self._make_request(
            "DELETE",
            f"/collections/{collection_id}/documents/{document_id}",
            params=params
        )
        return response.status_code == 200
    
    def count_records(
        self,
        collection_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RecordCountResponse:
        """
        Count records in a collection.
        
        Args:
            collection_id: Collection ID
            metadata: Optional metadata filter
            
        Returns:
            Record count response
        """
        params = {"collection_id": collection_id}
        if metadata:
            params["metadata"] = metadata
        
        response = self._make_request("GET", "/records/count", params=params)
        response_data = response.json()
        
        return RecordCountResponse(
            count=response_data["count"],
            collection_id=collection_id
        )

    # Query Methods
    
    def semantic_search(
        self,
        collection_id: str,
        query: str,
        limit: int = 10,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Perform semantic search within a collection.
        
        Args:
            collection_id: Collection to search
            query: Search query
            limit: Maximum number of results
            metadata: Optional metadata filter
            
        Returns:
            List of search results
        """
        request_data = SemanticSearchRequest(
            collection_id=collection_id,
            query=query,
            limit=limit,
            metadata=metadata
        )
        
        response = self._make_request("POST", "/search/collections", json_data=request_data.dict())
        response_data = response.json()
        
        results = []
        for result_data in response_data.get("results", []):
            results.append(SearchResult(**result_data))
        
        return results
    
    def rag_query(
        self,
        collection_id: str,
        message: str,
        limit: int = 10,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RAGResponse:
        """
        Perform RAG (Retrieval-Augmented Generation) query.
        
        Args:
            collection_id: Collection to query
            message: Query message
            limit: Maximum number of documents to retrieve
            metadata: Optional metadata filter
            
        Returns:
            RAG response with generated answer and sources
        """
        request_data = RAGQueryRequest(
            collection_id=collection_id,
            message=message,
            limit=limit,
            metadata=metadata
        )
        
        response = self._make_request("POST", "/chat/conversation", json_data=request_data.dict())
        response_data = response.json()
        
        # Parse sources if available
        sources = []
        if "sources" in response_data:
            for source_data in response_data["sources"]:
                sources.append(SearchResult(**source_data))
        
        return RAGResponse(
            answer=response_data.get("answer", ""),
            sources=sources,
            metadata=response_data.get("metadata")
        )

    # Convenience Methods
    
    def upload_documents(
        self,
        collection_id: str,
        file_paths: List[str],
        batch_name: str,
        batch_description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        wait_for_completion: bool = True,
        poll_interval: int = 20,
        max_wait_time: int = 3600
    ) -> Batch:
        """
        Complete document upload workflow.
        
        Args:
            collection_id: Target collection ID
            file_paths: List of file paths to upload
            batch_name: Name for the batch
            batch_description: Optional batch description
            metadata: Optional metadata
            wait_for_completion: Whether to wait for processing to complete
            poll_interval: Seconds between status checks
            max_wait_time: Maximum time to wait for completion
            
        Returns:
            Final batch status
        """
        # Extract file names from paths
        file_names = [os.path.basename(path) for path in file_paths]
        
        # Create batch
        batch = self.create_batch(
            collection_id=collection_id,
            file_list=file_names,
            batch_name=batch_name,
            batch_description=batch_description,
            metadata=metadata
        )
        
        # Upload files
        for file_path, upload_info in zip(file_paths, batch.pre_signed_urls):
            self.upload_file_to_s3(
                presigned_url=upload_info.url,
                fields=upload_info.fields,
                file_path=file_path
            )
        
        # Wait for completion if requested
        if wait_for_completion:
            return self.wait_for_batch_completion(
                batch_id=batch.id,
                poll_interval=poll_interval,
                max_wait_time=max_wait_time
            )
        
        return batch