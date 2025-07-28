# API Documentation

## Overview

This document provides comprehensive documentation for all public APIs, functions, and components in this Python project.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Modules](#core-modules)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Contributing](#contributing)

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
# Basic usage example
from your_module import YourClass

# Initialize the class
instance = YourClass()

# Use the API
result = instance.your_method()
print(result)
```

## Core Modules

### Module Structure

```
project/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   └── utils.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── data_models.py
│   └── services/
│       ├── __init__.py
│       └── business_logic.py
├── tests/
├── docs/
└── examples/
```

## API Reference

### Core API Classes

#### `BaseAPI`

The foundation class for all API operations.

**Constructor:**
```python
BaseAPI(config: dict = None, debug: bool = False)
```

**Parameters:**
- `config` (dict, optional): Configuration dictionary
- `debug` (bool, default=False): Enable debug mode

**Methods:**

##### `initialize()`

Initialize the API with default settings.

**Returns:**
- `bool`: True if initialization successful

**Example:**
```python
api = BaseAPI()
if api.initialize():
    print("API initialized successfully")
```

##### `get_status()`

Get the current API status.

**Returns:**
- `dict`: Status information containing:
  - `status` (str): Current status ("active", "inactive", "error")
  - `version` (str): API version
  - `uptime` (float): Uptime in seconds

**Example:**
```python
status = api.get_status()
print(f"API Status: {status['status']}")
print(f"Version: {status['version']}")
```

##### `process_data(data: Any, options: dict = None)`

Process input data according to specified options.

**Parameters:**
- `data` (Any): Input data to process
- `options` (dict, optional): Processing options

**Returns:**
- `ProcessResult`: Result object containing processed data

**Raises:**
- `ValueError`: If data format is invalid
- `ProcessingError`: If processing fails

**Example:**
```python
try:
    result = api.process_data(
        data={"key": "value"},
        options={"format": "json", "validate": True}
    )
    print(f"Processed: {result.data}")
except ValueError as e:
    print(f"Invalid data: {e}")
```

### Utility Functions

#### `validate_input(data: Any, schema: dict) -> bool`

Validate input data against a schema.

**Parameters:**
- `data` (Any): Data to validate
- `schema` (dict): Validation schema

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**
```python
from src.core.utils import validate_input

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["name", "age"]
}

data = {"name": "John", "age": 30}
is_valid = validate_input(data, schema)
print(f"Data is valid: {is_valid}")
```

#### `format_response(data: Any, format_type: str = "json") -> str`

Format response data in the specified format.

**Parameters:**
- `data` (Any): Data to format
- `format_type` (str): Output format ("json", "xml", "yaml")

**Returns:**
- `str`: Formatted data string

**Example:**
```python
from src.core.utils import format_response

data = {"message": "Hello, World!", "status": "success"}
json_response = format_response(data, "json")
xml_response = format_response(data, "xml")
```

### Data Models

#### `DataModel`

Base class for all data models.

**Attributes:**
- `id` (str): Unique identifier
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

**Methods:**

##### `to_dict() -> dict`

Convert model instance to dictionary.

**Returns:**
- `dict`: Dictionary representation of the model

##### `from_dict(data: dict) -> DataModel`

Create model instance from dictionary.

**Parameters:**
- `data` (dict): Dictionary containing model data

**Returns:**
- `DataModel`: New model instance

**Example:**
```python
from src.models.data_models import DataModel

# Create from dictionary
data = {
    "id": "123",
    "name": "Example",
    "value": 42
}
model = DataModel.from_dict(data)

# Convert back to dictionary
model_dict = model.to_dict()
```

### Service Classes

#### `BusinessService`

Service class for core business logic operations.

**Methods:**

##### `execute_operation(operation: str, params: dict = None) -> OperationResult`

Execute a business operation.

**Parameters:**
- `operation` (str): Operation name
- `params` (dict, optional): Operation parameters

**Returns:**
- `OperationResult`: Result of the operation

**Available Operations:**
- `"create"`: Create new resource
- `"read"`: Read existing resource
- `"update"`: Update existing resource
- `"delete"`: Delete resource

**Example:**
```python
from src.services.business_logic import BusinessService

service = BusinessService()

# Create operation
result = service.execute_operation(
    operation="create",
    params={"name": "New Item", "type": "example"}
)

if result.success:
    print(f"Created item with ID: {result.data['id']}")
else:
    print(f"Error: {result.error}")
```

## Examples

### Basic Usage

```python
#!/usr/bin/env python3
"""
Basic usage example demonstrating core API functionality.
"""

from src.core.api import BaseAPI
from src.models.data_models import DataModel
from src.services.business_logic import BusinessService

def main():
    # Initialize API
    api = BaseAPI(debug=True)
    api.initialize()
    
    # Check status
    status = api.get_status()
    print(f"API Status: {status}")
    
    # Process some data
    input_data = {
        "users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
    }
    
    result = api.process_data(input_data)
    print(f"Processed data: {result.data}")
    
    # Use business service
    service = BusinessService()
    operation_result = service.execute_operation(
        "create",
        {"name": "Example Item", "description": "Test item"}
    )
    
    if operation_result.success:
        print(f"Successfully created: {operation_result.data}")

if __name__ == "__main__":
    main()
```

### Advanced Usage

```python
#!/usr/bin/env python3
"""
Advanced usage example with error handling and configuration.
"""

import logging
from typing import Optional, Dict, Any

from src.core.api import BaseAPI
from src.core.utils import validate_input, format_response
from src.models.data_models import DataModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIManager:
    """Advanced API manager with configuration and error handling."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.api = BaseAPI(config=self.config, debug=self.config.get('debug', False))
        
    def _default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'timeout': 30,
            'retry_attempts': 3,
            'debug': False,
            'validation_enabled': True
        }
    
    def setup(self) -> bool:
        """Setup the API manager."""
        try:
            if not self.api.initialize():
                logger.error("Failed to initialize API")
                return False
                
            status = self.api.get_status()
            logger.info(f"API initialized with status: {status['status']}")
            return True
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            return False
    
    def process_with_validation(self, data: Any, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process data with validation."""
        try:
            # Validate input if enabled
            if self.config.get('validation_enabled', True):
                if not validate_input(data, schema):
                    logger.error("Data validation failed")
                    return None
            
            # Process data
            result = self.api.process_data(data)
            
            # Format response
            formatted = format_response(result.data, "json")
            logger.info(f"Successfully processed data: {len(str(formatted))} chars")
            
            return result.data
            
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            return None

def main():
    """Main function demonstrating advanced usage."""
    
    # Custom configuration
    config = {
        'timeout': 60,
        'retry_attempts': 5,
        'debug': True,
        'validation_enabled': True
    }
    
    # Initialize manager
    manager = APIManager(config)
    
    if not manager.setup():
        logger.error("Failed to setup API manager")
        return
    
    # Define validation schema
    schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "value": {"type": "number"}
                    },
                    "required": ["id", "name"]
                }
            }
        },
        "required": ["items"]
    }
    
    # Test data
    test_data = {
        "items": [
            {"id": "1", "name": "Item 1", "value": 100},
            {"id": "2", "name": "Item 2", "value": 200},
            {"id": "3", "name": "Item 3", "value": 300}
        ]
    }
    
    # Process with validation
    result = manager.process_with_validation(test_data, schema)
    
    if result:
        logger.info("Data processed successfully")
        print(f"Result: {result}")
    else:
        logger.error("Failed to process data")

if __name__ == "__main__":
    main()
```

### Error Handling Example

```python
#!/usr/bin/env python3
"""
Comprehensive error handling example.
"""

from src.core.api import BaseAPI
from src.core.exceptions import ProcessingError, ValidationError, APIError

def handle_api_errors():
    """Demonstrate proper error handling."""
    
    api = BaseAPI()
    
    try:
        # This might raise various exceptions
        api.initialize()
        
        # Invalid data that will cause ProcessingError
        invalid_data = None
        result = api.process_data(invalid_data)
        
    except ValidationError as e:
        print(f"Validation Error: {e}")
        print(f"Error details: {e.details}")
        
    except ProcessingError as e:
        print(f"Processing Error: {e}")
        print(f"Error code: {e.error_code}")
        
    except APIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.status_code}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        
    finally:
        # Cleanup
        if hasattr(api, 'cleanup'):
            api.cleanup()

if __name__ == "__main__":
    handle_api_errors()
```

## Error Handling

### Exception Hierarchy

```
Exception
└── APIError (base exception for all API errors)
    ├── ValidationError (data validation failures)
    ├── ProcessingError (data processing failures)
    ├── ConfigurationError (configuration issues)
    └── NetworkError (network-related errors)
```

### Common Error Codes

| Error Code | Description | Resolution |
|------------|-------------|------------|
| `VAL001` | Invalid input format | Check data format and schema |
| `VAL002` | Missing required field | Ensure all required fields are provided |
| `PROC001` | Processing timeout | Reduce data size or increase timeout |
| `PROC002` | Resource unavailable | Retry after some time |
| `API001` | Authentication failed | Check API credentials |
| `API002` | Rate limit exceeded | Implement rate limiting in client |

### Error Handling Best Practices

1. **Always handle specific exceptions first:**
   ```python
   try:
       result = api.process_data(data)
   except ValidationError as e:
       # Handle validation errors
       pass
   except ProcessingError as e:
       # Handle processing errors
       pass
   except APIError as e:
       # Handle general API errors
       pass
   ```

2. **Use logging for error tracking:**
   ```python
   import logging
   
   logger = logging.getLogger(__name__)
   
   try:
       result = api.process_data(data)
   except APIError as e:
       logger.error(f"API error occurred: {e}", exc_info=True)
   ```

3. **Implement retry logic for transient errors:**
   ```python
   import time
   from typing import Any, Optional
   
   def retry_api_call(func, max_retries: int = 3, delay: float = 1.0) -> Optional[Any]:
       for attempt in range(max_retries):
           try:
               return func()
           except NetworkError as e:
               if attempt == max_retries - 1:
                   raise
               logger.warning(f"Attempt {attempt + 1} failed: {e}")
               time.sleep(delay * (2 ** attempt))  # Exponential backoff
       return None
   ```

## Contributing

### Documentation Standards

1. **Docstring Format:**
   ```python
   def function_name(param1: type, param2: type = default) -> return_type:
       """
       Brief description of the function.
       
       Longer description if needed, explaining the purpose,
       behavior, and any important details.
       
       Args:
           param1 (type): Description of param1
           param2 (type, optional): Description of param2. Defaults to default.
           
       Returns:
           return_type: Description of return value
           
       Raises:
           ExceptionType: Description of when this exception is raised
           
       Example:
           >>> result = function_name("value1", param2="value2")
           >>> print(result)
           expected_output
       """
   ```

2. **API Documentation Requirements:**
   - All public functions must have docstrings
   - Include type hints for all parameters and return values
   - Provide usage examples for complex functions
   - Document all exceptions that can be raised
   - Include performance considerations for expensive operations

3. **Code Examples:**
   - All examples must be runnable
   - Include imports and setup code
   - Show both success and error cases
   - Use realistic data in examples

### Updating Documentation

When adding new APIs or modifying existing ones:

1. Update the relevant section in this document
2. Add or update examples
3. Update the Table of Contents if needed
4. Run documentation tests to ensure examples work
5. Update version information and changelog

### Documentation Testing

```bash
# Run documentation tests
python -m doctest docs/API_DOCUMENTATION.md

# Validate examples
python docs/validate_examples.py

# Generate API documentation from code
python docs/generate_api_docs.py
```

---

**Last Updated:** $(date)  
**Version:** 1.0.0  
**Maintainer:** Development Team