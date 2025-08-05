"""Prompt Store client for GE HealthCare IDS SDK."""

from typing import Dict, List, Optional, Any, Union
import requests
from urllib.parse import urljoin

from .auth import IDSAuth
from .exceptions import raise_for_status
from .models import (
    PromptTemplate, CreatePromptRequest, UpdatePromptRequest,
    SetDefaultPromptRequest, PromptListResponse, HealthCheckResponse
)


class PromptStoreClient:
    """
    Client for interacting with GE HealthCare Prompt Store API.
    
    Provides methods for managing prompt templates, versions, and lifecycle.
    """
    
    def __init__(
        self,
        auth: IDSAuth,
        base_url: str = "https://prompt-test.ailab.gehealthcare.com",
        verify_ssl: bool = True,
        timeout: int = 30
    ):
        """
        Initialize Prompt Store client.
        
        Args:
            auth: Authentication handler
            base_url: Base URL for Prompt Store API
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
            headers=request_headers,
            verify=self.verify_ssl,
            timeout=self.timeout
        )
        
        if response.status_code >= 400:
            raise_for_status(response)
        
        return response

    # Health Check Methods
    
    def health_check(self) -> HealthCheckResponse:
        """
        Check health of Prompt Store service.
        
        Returns:
            Health check response
        """
        response = self._make_request("GET", "/prompts/health")
        response_data = response.json()
        
        return HealthCheckResponse(
            status=response_data.get("status", "Healthy"),
            message=response_data.get("message", "Prompt Store service is running smoothly")
        )

    # Prompt Template Management
    
    def create_prompt_template(
        self,
        name: str,
        content: str,
        type: str = "System",
        provider: str = "OpenAI", 
        params: Union[str, Dict[str, Any]] = "{}",
        category: str = "completion",
        tags: Optional[List[str]] = None
    ) -> PromptTemplate:
        """
        Create a new prompt template.
        
        Args:
            name: Unique name for the prompt template
            content: Template content with {context} and {question} variables
            type: Prompt type (System, User, etc.)
            provider: Model provider (OpenAI, Amazon, Anthropic)
            params: Model parameters as string or dict
            category: Prompt category (completion, chat, etc.)
            tags: Optional list of tags
            
        Returns:
            Created prompt template
        """
        request_data = CreatePromptRequest(
            name=name,
            type=type,
            provider=provider,
            content=content,
            params=params,
            category=category,
            tags=tags
        )
        
        response = self._make_request("POST", "/prompts", json_data=request_data.dict())
        response_data = response.json()
        
        prompt_data = response_data.get("prompt", {})
        prompt_data.update({
            "name": name,
            "type": type,
            "provider": provider,
            "content": content,
            "params": params,
            "category": category,
            "tags": tags,
            "version": 1,
            "default": True
        })
        
        return PromptTemplate(**prompt_data)
    
    def create_prompt_version(
        self,
        name: str,
        type: Optional[str] = None,
        provider: Optional[str] = None,
        content: Optional[str] = None,
        params: Optional[Union[str, Dict[str, Any]]] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> PromptTemplate:
        """
        Create a new version of an existing prompt template.
        
        Args:
            name: Name of the existing prompt template
            type: Updated prompt type
            provider: Updated model provider
            content: Updated template content
            params: Updated model parameters
            category: Updated prompt category
            tags: Updated list of tags
            
        Returns:
            New prompt template version
        """
        request_data = UpdatePromptRequest(
            type=type,
            provider=provider,
            content=content,
            params=params,
            category=category,
            tags=tags
        )
        
        # Remove None values
        request_dict = {k: v for k, v in request_data.dict().items() if v is not None}
        
        response = self._make_request("PUT", f"/prompts/{name}", json_data=request_dict)
        response_data = response.json()
        
        prompt_data = response_data.get("prompt", {})
        return PromptTemplate(**prompt_data)
    
    def get_all_prompts(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        prompt_name: Optional[str] = None,
        version: Optional[Union[int, str]] = None,
        type: Optional[str] = None,
        provider: Optional[str] = None,
        category: Optional[str] = None,
        scope: Optional[str] = None,
        tag: Optional[str] = None
    ) -> PromptListResponse:
        """
        Retrieve all prompt templates with optional filtering.
        
        Args:
            page: Page number for pagination
            size: Number of items per page
            prompt_name: Filter by prompt name
            version: Filter by version (number, "latest", or "default")
            type: Filter by prompt type
            provider: Filter by model provider
            category: Filter by category
            scope: Search scope ("client" for client-wide search)
            tag: Filter by tag
            
        Returns:
            Paginated list of prompt templates
        """
        params = {}
        
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if prompt_name is not None:
            params["name"] = prompt_name
        if version is not None:
            params["version"] = str(version)
        if type is not None:
            params["type"] = type
        if provider is not None:
            params["provider"] = provider
        if category is not None:
            params["category"] = category
        if scope is not None:
            params["scope"] = scope
        if tag is not None:
            params["tag"] = tag
        
        response = self._make_request("GET", "/prompts", params=params)
        response_data = response.json()
        
        prompts = []
        for prompt_data in response_data.get("prompts", []):
            prompts.append(PromptTemplate(**prompt_data))
        
        return PromptListResponse(
            prompts=prompts,
            total_count=response_data.get("totalCount"),
            total_pages=response_data.get("totalPages"),
            next_page=response_data.get("nextPage")
        )
    
    def get_prompt_versions(
        self,
        name: str,
        page: Optional[int] = None,
        size: Optional[int] = None,
        version: Optional[Union[int, str]] = None,
        type: Optional[str] = None,
        provider: Optional[str] = None,
        category: Optional[str] = None,
        scope: Optional[str] = None,
        tag: Optional[str] = None
    ) -> PromptListResponse:
        """
        Retrieve all versions of a specific prompt template.
        
        Args:
            name: Name of the prompt template
            page: Page number for pagination
            size: Number of items per page
            version: Filter by version (number, "latest", or "default")
            type: Filter by prompt type
            provider: Filter by model provider
            category: Filter by category
            scope: Search scope ("client" for client-wide search)
            tag: Filter by tag
            
        Returns:
            Paginated list of prompt template versions
        """
        params = {}
        
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if version is not None:
            params["version"] = str(version)
        if type is not None:
            params["type"] = type
        if provider is not None:
            params["provider"] = provider
        if category is not None:
            params["category"] = category
        if scope is not None:
            params["scope"] = scope
        if tag is not None:
            params["tag"] = tag
        
        response = self._make_request("GET", f"/prompts/{name}", params=params)
        response_data = response.json()
        
        prompts = []
        for prompt_data in response_data.get("prompts", []):
            prompts.append(PromptTemplate(**prompt_data))
        
        return PromptListResponse(
            prompts=prompts,
            total_count=response_data.get("totalCount"),
            total_pages=response_data.get("totalPages"),
            next_page=response_data.get("nextPage")
        )
    
    def get_prompt_version(
        self,
        name: str,
        version: Union[int, str] = "latest"
    ) -> PromptTemplate:
        """
        Retrieve a specific version of a prompt template.
        
        Args:
            name: Name of the prompt template
            version: Version to retrieve (number, "latest", or "default")
            
        Returns:
            Specific prompt template version
        """
        response = self._make_request("GET", f"/prompts/{name}/version/{version}")
        response_data = response.json()
        
        prompt_data = response_data.get("prompt", {})
        return PromptTemplate(**prompt_data)
    
    def set_default_version(
        self,
        name: str,
        version: Union[int, str] = "latest",
        justification: Optional[str] = None
    ) -> bool:
        """
        Set a specific version as the default for a prompt template.
        
        Args:
            name: Name of the prompt template
            version: Version to set as default (number or "latest")
            justification: Optional justification for the change
            
        Returns:
            True if successful
        """
        request_data = SetDefaultPromptRequest(justification=justification)
        
        response = self._make_request(
            "PUT",
            f"/prompts/{name}/version/{version}",
            json_data=request_data.dict()
        )
        
        return response.status_code == 201
    
    def delete_prompt_version(
        self,
        name: str,
        version: Union[int, str]
    ) -> bool:
        """
        Delete a specific version of a prompt template.
        
        Args:
            name: Name of the prompt template
            version: Version to delete
            
        Returns:
            True if successful
        """
        response = self._make_request("DELETE", f"/prompts/{name}/version/{version}")
        return response.status_code == 200

    # Convenience Methods
    
    def get_default_prompt(self, name: str) -> PromptTemplate:
        """
        Get the default version of a prompt template.
        
        Args:
            name: Name of the prompt template
            
        Returns:
            Default prompt template version
        """
        return self.get_prompt_version(name, "default")
    
    def get_latest_prompt(self, name: str) -> PromptTemplate:
        """
        Get the latest version of a prompt template.
        
        Args:
            name: Name of the prompt template
            
        Returns:
            Latest prompt template version
        """
        return self.get_prompt_version(name, "latest")
    
    def list_prompt_names(self) -> List[str]:
        """
        Get a list of all prompt template names.
        
        Returns:
            List of prompt template names
        """
        response = self.get_all_prompts()
        
        # Get unique prompt names
        names = set()
        for prompt in response.prompts:
            names.add(prompt.name)
        
        return sorted(list(names))
    
    def update_prompt_and_set_default(
        self,
        name: str,
        content: Optional[str] = None,
        type: Optional[str] = None,
        provider: Optional[str] = None,
        params: Optional[Union[str, Dict[str, Any]]] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        justification: Optional[str] = None
    ) -> PromptTemplate:
        """
        Create a new version of a prompt and set it as default.
        
        Args:
            name: Name of the existing prompt template
            content: Updated template content
            type: Updated prompt type
            provider: Updated model provider
            params: Updated model parameters
            category: Updated prompt category
            tags: Updated list of tags
            justification: Justification for setting as default
            
        Returns:
            New default prompt template version
        """
        # Create new version
        new_version = self.create_prompt_version(
            name=name,
            type=type,
            provider=provider,
            content=content,
            params=params,
            category=category,
            tags=tags
        )
        
        # Set as default
        self.set_default_version(
            name=name,
            version=new_version.version,
            justification=justification
        )
        
        # Return updated prompt with default flag
        new_version.default = True
        return new_version
    
    def clone_prompt_template(
        self,
        source_name: str,
        target_name: str,
        source_version: Union[int, str] = "default",
        modifications: Optional[Dict[str, Any]] = None
    ) -> PromptTemplate:
        """
        Clone an existing prompt template with optional modifications.
        
        Args:
            source_name: Name of the source prompt template
            target_name: Name for the new prompt template
            source_version: Version to clone from
            modifications: Optional modifications to apply
            
        Returns:
            New cloned prompt template
        """
        # Get source prompt
        source_prompt = self.get_prompt_version(source_name, source_version)
        
        # Apply modifications if provided
        if modifications:
            for key, value in modifications.items():
                if hasattr(source_prompt, key):
                    setattr(source_prompt, key, value)
        
        # Create new prompt with cloned data
        return self.create_prompt_template(
            name=target_name,
            content=source_prompt.content,
            type=source_prompt.type,
            provider=source_prompt.provider,
            params=source_prompt.params,
            category=source_prompt.category,
            tags=source_prompt.tags
        )