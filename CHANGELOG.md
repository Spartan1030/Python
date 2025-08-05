# Changelog

All notable changes to the GE HealthCare Intelligent Data Store SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Added

#### Core SDK Features
- **Unified IDSClient** - Single client interface for all IDS services
- **IDAM Authentication** - OAuth2 client credentials flow with automatic token refresh
- **Environment Configuration** - Support for environment variable configuration
- **Comprehensive Error Handling** - Custom exception hierarchy with detailed error information

#### Vector Store Client
- **Collection Management**
  - Create collections with validation and metadata
  - List all collections for authenticated application
  - Delete collections with soft/hard delete options
- **Document Management**
  - Bulk document upload with pre-signed S3 URLs
  - Batch processing with status monitoring
  - Custom text chunk ingestion with metadata
  - Document listing with pagination
  - Individual document deletion
- **Querying Capabilities**
  - Semantic search with similarity scoring
  - RAG (Retrieval-Augmented Generation) queries
  - Metadata filtering for targeted searches
  - Configurable result limits
- **Administrative Features**
  - Record counting for collections
  - Health checks for all Vector Store services
  - Batch status monitoring and management

#### Prompt Store Client
- **Template Management**
  - Create prompt templates with required {context} and {question} variables
  - Template validation and content checking
  - Support for multiple providers (OpenAI, Amazon, Anthropic)
  - Categorization and tagging system
- **Version Control**
  - Create new versions of existing templates
  - Set default versions with justification
  - Version history tracking
  - Version deletion capabilities
- **Advanced Querying**
  - Filter by category, provider, type, and tags
  - Pagination support for large result sets
  - Search across client or application scope
  - Version-specific retrieval (latest, default, specific)
- **Template Operations**
  - Clone existing templates with modifications
  - Bulk template management
  - Template lifecycle management

#### Data Models
- **Pydantic Models** - Type-safe request/response models with validation
- **Collection Model** - Complete collection representation with metadata
- **Document Model** - Document structure with file information and status
- **Batch Model** - Batch processing information with file tracking
- **PromptTemplate Model** - Comprehensive prompt template structure
- **Search Models** - Search results and RAG response structures

#### Examples and Documentation
- **Basic Usage Example** - Complete workflow demonstration
- **Vector Store Example** - Focused document management scenarios
- **Prompt Store Example** - Template management and versioning workflows
- **Comprehensive README** - Detailed API documentation and usage guides
- **Type Hints** - Full type annotation support for better IDE experience

### Technical Implementation
- **Python 3.8+ Support** - Compatible with modern Python versions
- **Async Ready Architecture** - Foundation for future async support
- **Configurable Endpoints** - Support for different deployment environments
- **SSL Configuration** - Configurable SSL verification for security
- **Request Timeout Management** - Configurable timeouts for all operations
- **Robust Error Recovery** - Detailed exception handling with retry capabilities

### Security Features
- **Secure Credential Management** - Environment variable support
- **Token Caching** - Automatic token refresh with expiry management
- **SSL/TLS Support** - Secure communication with configurable verification
- **Request Signing** - Proper OAuth2 authentication headers

### Developer Experience
- **Type Safety** - Complete type annotations and Pydantic models
- **IDE Support** - Full IntelliSense and auto-completion
- **Error Messages** - Clear, actionable error messages
- **Logging Integration** - Ready for application logging frameworks
- **Testing Support** - Mock-friendly architecture for unit testing

[1.0.0]: https://github.com/gehealthcare/ids-sdk-python/releases/tag/v1.0.0