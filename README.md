# GE HealthCare Intelligent Data Store SDK

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](docs/)

A comprehensive Python SDK for interacting with GE HealthCare's AI Fabric Intelligent Data Store, providing seamless access to Vector Store and Prompt Store services for building advanced AI applications with RAG (Retrieval-Augmented Generation) architecture.

## 🚀 Features

### Vector Store
- **Collection Management**: Create, list, and delete document collections
- **Document Upload**: Bulk document ingestion with batch processing
- **Custom Chunks**: Add pre-processed text chunks with metadata
- **Semantic Search**: Perform similarity searches across stored documents
- **RAG Queries**: Generate contextual responses using retrieved documents
- **Health Monitoring**: Check service status and monitor batch processing

### Prompt Store
- **Template Management**: Create and manage reusable prompt templates
- **Version Control**: Track template changes with semantic versioning
- **Default Management**: Set and manage default template versions
- **Advanced Filtering**: Search templates by category, provider, tags
- **Template Cloning**: Clone and customize existing templates

### Authentication & Security
- **IDAM Integration**: Secure OAuth2 client credentials flow
- **Token Management**: Automatic token refresh and caching
- **SSL Support**: Configurable SSL verification
- **Environment Variables**: Secure credential management

## 📦 Installation

```bash
pip install gehc-ids-sdk
```

### Development Installation

```bash
git clone https://github.com/gehealthcare/ids-sdk-python.git
cd ids-sdk-python
pip install -e ".[dev]"
```

## 🔧 Quick Start

### 1. Setup Authentication

First, obtain your credentials from IDAM (Identity and Access Manager):

```python
from gehc_ids import IDSClient

# Method 1: Direct initialization
client = IDSClient(
    client_id="your-client-id",
    client_secret="your-client-secret", 
    audience="your-audience-id"
)

# Method 2: Environment variables
# Set IDS_CLIENT_ID, IDS_CLIENT_SECRET, IDS_AUDIENCE
client = IDSClient.from_environment()
```

### 2. Vector Store Operations

```python
# Create a collection
collection = client.vector_store.create_collection(
    title="Medical Documents",
    description="Collection of medical research papers"
)

# Upload documents
batch = client.vector_store.upload_documents(
    collection_id=collection.id,
    file_paths=["/path/to/document1.pdf", "/path/to/document2.txt"],
    batch_name="Initial Upload",
    wait_for_completion=True
)

# Semantic search
results = client.vector_store.semantic_search(
    collection_id=collection.id,
    query="What are the symptoms of diabetes?",
    limit=5
)

# RAG query
response = client.vector_store.rag_query(
    collection_id=collection.id,
    message="Explain the different types of diabetes",
    limit=3
)
print(f"Answer: {response.answer}")
```

### 3. Prompt Store Operations

```python
# Create a prompt template
prompt = client.prompt_store.create_prompt_template(
    name="Medical_Summarizer",
    content="Based on {context}, provide a summary for: {question}",
    category="summarization",
    tags=["medical", "summary"]
)

# Create a new version
updated_prompt = client.prompt_store.create_prompt_version(
    name="Medical_Summarizer",
    content="As a medical expert, analyze {context} and answer: {question}",
    params='{"model": "gpt-4", "temperature": 0.3}'
)

# Set as default
client.prompt_store.set_default_version(
    name="Medical_Summarizer",
    version=updated_prompt.version,
    justification="Improved medical accuracy"
)
```

## 📖 Detailed Usage

### Vector Store Client

#### Collection Management

```python
from gehc_ids import VectorStoreClient, IDSAuth

# Initialize
auth = IDSAuth(client_id="...", client_secret="...", audience="...")
vs_client = VectorStoreClient(auth=auth)

# Create collection
collection = vs_client.create_collection(
    title="Clinical_Guidelines",
    description="Evidence-based clinical practice guidelines"
)

# List collections
collections = vs_client.list_collections()
for coll in collections:
    print(f"{coll.title}: {coll.description}")

# Delete collection
vs_client.delete_collection(collection.id, soft_delete=True)
```

#### Document Management

```python
# Bulk upload workflow
batch = vs_client.create_batch(
    collection_id=collection.id,
    file_list=["doc1.pdf", "doc2.txt"],
    batch_name="Medical Literature Upload"
)

# Upload files using pre-signed URLs
for file_path, upload_info in zip(file_paths, batch.pre_signed_urls):
    vs_client.upload_file_to_s3(
        presigned_url=upload_info.url,
        fields=upload_info.fields,
        file_path=file_path
    )

# Monitor batch status
final_batch = vs_client.wait_for_batch_completion(batch.id)
print(f"Processing complete: {final_batch.status}")

# Add custom text chunks
vs_client.add_chunks_to_collection(
    collection_id=collection.id,
    document_id="custom-doc-1",
    document_name="Clinical Guidelines",
    chunks=["Treatment protocol 1...", "Treatment protocol 2..."],
    metadata={"source": "clinical_trials", "evidence_level": "A"}
)
```

#### Querying

```python
# Semantic search with metadata filtering
results = vs_client.semantic_search(
    collection_id=collection.id,
    query="diabetes treatment guidelines",
    limit=10,
    metadata={"evidence_level": "A"}
)

for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Content: {result.content[:200]}...")

# RAG query for contextual answers
rag_response = vs_client.rag_query(
    collection_id=collection.id,
    message="What are the latest recommendations for Type 2 diabetes management?",
    limit=5
)

print(f"Generated Answer: {rag_response.answer}")
print(f"Based on {len(rag_response.sources)} sources")
```

### Prompt Store Client

#### Template Creation and Management

```python
from gehc_ids import PromptStoreClient, IDSAuth

# Initialize
ps_client = PromptStoreClient(auth=auth)

# Create comprehensive prompt template
prompt = ps_client.create_prompt_template(
    name="Clinical_Analysis_Assistant",
    content="""You are a clinical analysis AI assistant.

Clinical Context: {context}
Analysis Question: {question}

Provide a thorough clinical analysis including:
- Key clinical findings
- Differential diagnosis considerations  
- Recommended follow-up actions
- Risk assessment

Clinical Analysis:""",
    type="System",
    provider="OpenAI",
    params='{"model": "gpt-4", "temperature": 0.2, "max_tokens": 600}',
    category="clinical-analysis",
    tags=["clinical", "analysis", "diagnosis", "medical"]
)
```

#### Version Management

```python
# Create improved version
v2 = ps_client.create_prompt_version(
    name="Clinical_Analysis_Assistant",
    content="""You are an expert clinical AI with board certification knowledge.

Patient Context: {context}
Clinical Question: {question}

Evidence-based analysis framework:
- Apply clinical decision rules
- Reference current guidelines (2024)
- Include ICD-10 codes when relevant
- Assess urgency and priority
- Provide clear recommendations

Comprehensive Clinical Assessment:""",
    params='{"model": "gpt-4-turbo", "temperature": 0.15}',
    tags=["clinical", "evidence-based", "guidelines", "icd10"]
)

# Set as default with justification
ps_client.set_default_version(
    name="Clinical_Analysis_Assistant",
    version=v2.version,
    justification="Enhanced with 2024 guidelines and ICD-10 integration"
)
```

#### Advanced Querying

```python
# Filter by multiple criteria
clinical_prompts = ps_client.get_all_prompts(
    category="clinical-analysis",
    provider="OpenAI", 
    tag="evidence-based"
)

# Get all versions of a template
versions = ps_client.get_prompt_versions("Clinical_Analysis_Assistant")
for v in versions.prompts:
    default_marker = " (DEFAULT)" if v.default else ""
    print(f"Version {v.version}{default_marker}: {v.category}")

# Clone and customize for specialization
pediatric_prompt = ps_client.clone_prompt_template(
    source_name="Clinical_Analysis_Assistant",
    target_name="Pediatric_Clinical_Assistant", 
    modifications={
        "content": "You are a pediatric clinical AI specialist...",
        "tags": ["pediatric", "children", "clinical"],
        "category": "pediatric-analysis"
    }
)
```

## 🔐 Authentication and Security

### IDAM Setup

1. **Create Application Group** (if needed):
   - Use [Support Central](https://app.sc.ge.com/workflows/initiate/1813108)
   - Request type: "Create application group request"

2. **Create Application in IDAM**:
   - Follow Support Central workflow
   - Obtain client_id and client_secret

3. **Subscribe to IDS Services**:
   - Subscribe application to Vector Store and Prompt Store
   - Obtain audience identifier

### Environment Variables

```bash
# Set in your environment
export IDS_CLIENT_ID="your-client-id"
export IDS_CLIENT_SECRET="your-client-secret"  
export IDS_AUDIENCE="your-audience-id"

# Optional: Custom endpoints
export IDS_VECTOR_STORE_URL="https://ids-test.ailab.gehealthcare.com/api/v1"
export IDS_PROMPT_STORE_URL="https://prompt-test.ailab.gehealthcare.com"
```

### Security Best Practices

```python
# Use environment variables
client = IDSClient.from_environment()

# Configure SSL verification
client = IDSClient(
    client_id="...",
    client_secret="...", 
    audience="...",
    verify_ssl=True  # Always True in production
)

# Monitor token status
token_info = client.get_token_info()
if token_info["is_expired"]:
    client.refresh_token()
```

## 🔧 Configuration

### Client Configuration

```python
# Custom endpoints and timeouts
client = IDSClient(
    client_id="...",
    client_secret="...",
    audience="...",
    vector_store_url="https://your-custom-vs-endpoint.com/api/v1",
    prompt_store_url="https://your-custom-ps-endpoint.com",
    timeout=60,  # seconds
    verify_ssl=True
)

# Individual service clients
auth = IDSAuth(client_id="...", client_secret="...", audience="...")

vector_client = VectorStoreClient(
    auth=auth,
    base_url="https://custom-vector-store.com/api/v1",
    timeout=30
)

prompt_client = PromptStoreClient(
    auth=auth, 
    base_url="https://custom-prompt-store.com",
    timeout=30
)
```

### Error Handling

```python
from gehc_ids.exceptions import (
    IDSException, AuthenticationError, ValidationError,
    NotFoundError, ServerError
)

try:
    collection = client.vector_store.create_collection(
        title="Test Collection",
        description="Test description"
    )
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    # Handle token refresh
except ValidationError as e:
    print(f"Invalid request: {e.message}")
    # Fix request parameters
except ServerError as e:
    print(f"Server error: {e.message}")
    # Retry logic
except IDSException as e:
    print(f"IDS error: {e.message} (Status: {e.status_code})")
```

## 📋 API Reference

### IDSClient

Main unified client providing access to all services.

#### Methods
- `health_check()` - Check health of all services
- `refresh_token()` - Force token refresh
- `get_token_info()` - Get token status information

#### Properties
- `vector_store` - VectorStoreClient instance
- `prompt_store` - PromptStoreClient instance
- `auth` - IDSAuth instance

### VectorStoreClient

Client for Vector Store operations.

#### Collection Methods
- `create_collection(title, description)` - Create new collection
- `list_collections()` - List all collections
- `delete_collection(collection_id, soft_delete)` - Delete collection

#### Document Methods
- `upload_documents(collection_id, file_paths, batch_name)` - Upload documents
- `add_chunks_to_collection(collection_id, document_id, chunks)` - Add text chunks
- `list_documents(collection_id)` - List documents in collection
- `delete_document(collection_id, document_id)` - Delete document

#### Query Methods
- `semantic_search(collection_id, query, limit)` - Semantic search
- `rag_query(collection_id, message, limit)` - RAG-based query

### PromptStoreClient

Client for Prompt Store operations.

#### Template Methods
- `create_prompt_template(name, content, category)` - Create template
- `create_prompt_version(name, content)` - Create new version
- `get_prompt_version(name, version)` - Get specific version
- `delete_prompt_version(name, version)` - Delete version

#### Management Methods
- `set_default_version(name, version, justification)` - Set default version
- `get_all_prompts(category, provider, tag)` - List with filtering
- `clone_prompt_template(source_name, target_name)` - Clone template

## 🧪 Examples

See the [`examples/`](examples/) directory for comprehensive usage examples:

- [`basic_usage.py`](examples/basic_usage.py) - Complete workflow demonstration
- [`vector_store_example.py`](examples/vector_store_example.py) - Vector Store operations
- [`prompt_store_example.py`](examples/prompt_store_example.py) - Prompt Store management

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/gehealthcare/ids-sdk-python.git
cd ids-sdk-python

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black gehc_ids/
isort gehc_ids/
flake8 gehc_ids/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [https://gehealthcare.github.io/ids-sdk-python/](https://gehealthcare.github.io/ids-sdk-python/)
- **Issues**: [GitHub Issues](https://github.com/gehealthcare/ids-sdk-python/issues)
- **Support**: Contact AI Fabric team at ai-fabric@gehealthcare.com

## 🗺️ Roadmap

- [ ] Async client support
- [ ] Streaming responses for large queries
- [ ] Enhanced metadata filtering
- [ ] Integration with other AI Fabric services
- [ ] Performance optimization tools
- [ ] Advanced error recovery mechanisms

## 📊 Version History

### v1.0.0 (Current)
- Initial release
- Complete Vector Store and Prompt Store support
- IDAM authentication integration
- Comprehensive documentation and examples

---

**Note**: This SDK is designed for GE HealthCare's internal AI Fabric platform. External usage requires appropriate licensing and access permissions.
