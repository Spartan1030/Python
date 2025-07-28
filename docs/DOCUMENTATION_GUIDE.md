# Documentation Guide

## Overview

This guide provides comprehensive standards and best practices for documenting Python code in this project. Follow these guidelines to ensure consistent, high-quality documentation across all modules.

## Table of Contents

- [Docstring Standards](#docstring-standards)
- [Type Hints](#type-hints)
- [API Documentation](#api-documentation)
- [Examples and Usage](#examples-and-usage)
- [Documentation Tools](#documentation-tools)
- [Best Practices](#best-practices)

## Docstring Standards

### Format

We use the **Google Style** docstring format for consistency and readability.

#### Function Documentation

```python
def calculate_distance(point1: tuple[float, float], point2: tuple[float, float], 
                      metric: str = "euclidean") -> float:
    """Calculate the distance between two points.
    
    This function supports multiple distance metrics including Euclidean,
    Manhattan, and Chebyshev distances.
    
    Args:
        point1 (tuple[float, float]): First point as (x, y) coordinates
        point2 (tuple[float, float]): Second point as (x, y) coordinates
        metric (str, optional): Distance metric to use. Options are:
            - "euclidean": Standard Euclidean distance
            - "manhattan": Manhattan (L1) distance  
            - "chebyshev": Chebyshev (L∞) distance
            Defaults to "euclidean".
    
    Returns:
        float: The calculated distance between the two points
    
    Raises:
        ValueError: If metric is not one of the supported options
        TypeError: If points are not valid tuples of numbers
    
    Example:
        >>> p1 = (0, 0)
        >>> p2 = (3, 4)
        >>> calculate_distance(p1, p2)
        5.0
        >>> calculate_distance(p1, p2, metric="manhattan")
        7.0
    
    Note:
        For large datasets, consider using vectorized operations with NumPy
        for better performance.
    """
```

#### Class Documentation

```python
class DataProcessor:
    """A processor for handling and transforming data.
    
    This class provides methods for cleaning, validating, and transforming
    various types of data. It supports both batch and streaming processing
    modes.
    
    Attributes:
        config (dict): Configuration settings for the processor
        is_initialized (bool): Whether the processor has been initialized
        processing_mode (str): Current processing mode ("batch" or "stream")
    
    Example:
        >>> processor = DataProcessor({"mode": "batch", "validation": True})
        >>> processor.initialize()
        >>> result = processor.process(data)
    """
    
    def __init__(self, config: dict = None):
        """Initialize the DataProcessor.
        
        Args:
            config (dict, optional): Configuration dictionary containing:
                - mode (str): Processing mode ("batch" or "stream")
                - validation (bool): Whether to enable data validation
                - timeout (int): Timeout in seconds for operations
                Defaults to None, which uses default configuration.
        """
```

#### Module Documentation

```python
"""Data processing utilities for the application.

This module provides comprehensive data processing capabilities including
data cleaning, validation, transformation, and analysis functions.

Classes:
    DataProcessor: Main processor for handling data operations
    DataValidator: Validator for checking data integrity
    DataTransformer: Transformer for data format conversion

Functions:
    load_data: Load data from various sources
    save_data: Save data to various formats
    validate_schema: Validate data against a schema

Constants:
    DEFAULT_CONFIG: Default configuration for data processing
    SUPPORTED_FORMATS: List of supported data formats

Example:
    >>> from data_utils import DataProcessor, load_data
    >>> data = load_data("data.csv")
    >>> processor = DataProcessor()
    >>> processed_data = processor.process(data)
"""
```

### Required Sections

#### For Functions
- **Brief description**: One-line summary
- **Args**: All parameters with types and descriptions
- **Returns**: Return type and description
- **Raises**: All exceptions that can be raised
- **Example**: At least one usage example

#### For Classes
- **Brief description**: Purpose and overview
- **Attributes**: Public attributes with types
- **Example**: Basic usage example

#### For Modules
- **Brief description**: Module purpose
- **Classes**: List of main classes
- **Functions**: List of main functions
- **Constants**: Important constants
- **Example**: Import and basic usage

## Type Hints

### Basic Types

```python
from typing import List, Dict, Optional, Union, Tuple, Any, Callable

def process_items(items: List[str], 
                 metadata: Dict[str, Any],
                 callback: Optional[Callable[[str], None]] = None) -> Tuple[List[str], int]:
    """Process a list of items with metadata."""
```

### Complex Types

```python
from typing import TypeVar, Generic, Protocol
from dataclasses import dataclass

T = TypeVar('T')

class Processable(Protocol):
    """Protocol for objects that can be processed."""
    def process(self) -> Any: ...

@dataclass
class Result(Generic[T]):
    """Generic result container."""
    data: T
    success: bool
    error_message: Optional[str] = None

def process_data(items: List[Processable]) -> Result[List[Any]]:
    """Process items that implement the Processable protocol."""
```

### Union Types (Modern Python 3.10+)

```python
def parse_id(value: str | int) -> int:
    """Parse an ID from string or integer."""
    
def get_config() -> dict[str, str | int | bool]:
    """Get configuration dictionary."""
```

## API Documentation

### Public vs Private

#### Public APIs (document fully)
```python
def public_function(param: str) -> str:
    """This is a public function that external users can call.
    
    Full documentation required including examples.
    """

class PublicClass:
    """Public class for external use.
    
    Complete documentation with all methods documented.
    """
    
    def public_method(self) -> None:
        """Public method requiring full documentation."""
```

#### Private/Internal (minimal documentation)
```python
def _internal_helper(param: str) -> str:
    """Internal helper function.
    
    Brief description sufficient.
    """

class _InternalClass:
    """Internal class for implementation details."""
```

### Configuration Parameters

Document all configuration options clearly:

```python
def initialize_system(config: dict) -> bool:
    """Initialize the system with configuration.
    
    Args:
        config (dict): Configuration dictionary with the following keys:
            - database_url (str): Database connection URL
            - timeout (int, optional): Timeout in seconds (default: 30)
            - retries (int, optional): Number of retry attempts (default: 3)
            - debug (bool, optional): Enable debug mode (default: False)
            - cache_size (int, optional): Cache size in MB (default: 100)
            - log_level (str, optional): Logging level 
              ("DEBUG", "INFO", "WARNING", "ERROR") (default: "INFO")
    
    Returns:
        bool: True if initialization successful, False otherwise
    
    Example:
        >>> config = {
        ...     "database_url": "postgresql://localhost/db",
        ...     "timeout": 60,
        ...     "debug": True
        ... }
        >>> initialize_system(config)
        True
    """
```

## Examples and Usage

### Comprehensive Examples

Provide examples that cover:

1. **Basic usage**
2. **Advanced scenarios**
3. **Error handling**
4. **Integration with other components**

```python
def data_pipeline(source: str, transformations: List[str], 
                 destination: str) -> bool:
    """Execute a data pipeline with transformations.
    
    Args:
        source (str): Data source path or URL
        transformations (List[str]): List of transformation names to apply
        destination (str): Output destination path
    
    Returns:
        bool: True if pipeline executed successfully
    
    Raises:
        FileNotFoundError: If source file doesn't exist
        ValueError: If transformation is not supported
        PermissionError: If cannot write to destination
    
    Examples:
        Basic usage:
        >>> data_pipeline("input.csv", ["clean", "normalize"], "output.csv")
        True
        
        Advanced usage with error handling:
        >>> try:
        ...     result = data_pipeline(
        ...         source="https://api.example.com/data",
        ...         transformations=["validate", "clean", "aggregate"],
        ...         destination="s3://bucket/processed_data.parquet"
        ...     )
        ...     print(f"Pipeline completed: {result}")
        ... except ValueError as e:
        ...     print(f"Invalid transformation: {e}")
        ... except PermissionError as e:
        ...     print(f"Cannot write output: {e}")
        
        Using with configuration:
        >>> from config import get_pipeline_config
        >>> config = get_pipeline_config("production")
        >>> data_pipeline(
        ...     source=config["input_source"],
        ...     transformations=config["transformations"],
        ...     destination=config["output_destination"]
        ... )
        True
    """
```

### Interactive Examples

For complex APIs, provide step-by-step interactive examples:

```python
"""
Interactive Example: Building a Complete Data Pipeline

Step 1: Initialize the components
>>> from data_processor import DataProcessor, DataValidator
>>> from data_sources import CSVSource, DatabaseSource
>>> from data_sinks import S3Sink, DatabaseSink

Step 2: Set up data source
>>> source = CSVSource("input_data.csv")
>>> source.configure(delimiter=",", encoding="utf-8")

Step 3: Create processor with validation
>>> validator = DataValidator(schema="user_schema.json")
>>> processor = DataProcessor(validator=validator)

Step 4: Configure output destination  
>>> sink = S3Sink("s3://my-bucket/processed/")
>>> sink.configure(format="parquet", compression="snappy")

Step 5: Execute pipeline
>>> pipeline = processor.create_pipeline(source, sink)
>>> result = pipeline.execute()
>>> print(f"Processed {result.records_processed} records")
Processed 10000 records

Step 6: Check results
>>> print(f"Success rate: {result.success_rate:.2%}")
Success rate: 99.85%
>>> if result.errors:
...     print(f"Errors: {len(result.errors)}")
...     for error in result.errors[:5]:  # Show first 5 errors
...         print(f"  - {error}")
"""
```

## Documentation Tools

### Sphinx Configuration

```python
# docs/conf.py
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'Your Project Name'
copyright = '2024, Your Team'
author = 'Your Team'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
    'sphinx_rtd_theme',
]

# Napoleon settings (for Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
}
```

### Automated Documentation Generation

```bash
#!/bin/bash
# scripts/generate_docs.sh

echo "Generating API documentation..."

# Clean previous build
rm -rf docs/_build

# Generate API documentation from code
sphinx-apidoc -o docs/source src/

# Build HTML documentation
cd docs
make html

echo "Documentation generated in docs/_build/html"
```

### Documentation Testing

```python
# tests/test_documentation.py
import doctest
import importlib
import pkgutil
import src

def test_docstrings():
    """Test all docstring examples."""
    failure_count = 0
    test_count = 0
    
    # Test all modules in src package
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=src.__path__, prefix=src.__name__ + "."
    ):
        try:
            module = importlib.import_module(modname)
            result = doctest.testmod(module, verbose=True)
            failure_count += result.failed
            test_count += result.attempted
        except Exception as e:
            print(f"Error testing {modname}: {e}")
    
    print(f"Doctest results: {test_count - failure_count}/{test_count} passed")
    assert failure_count == 0, f"{failure_count} docstring tests failed"
```

## Best Practices

### 1. Write Documentation First

```python
# Good: Write docstring first, then implementation
def complex_algorithm(data: List[float], threshold: float) -> Dict[str, Any]:
    """Analyze data using a complex algorithm.
    
    Args:
        data: List of numerical values to analyze
        threshold: Cutoff value for analysis
    
    Returns:
        Dictionary containing analysis results with keys:
        - 'mean': Average value
        - 'outliers': List of outlier indices
        - 'summary': Text summary of results
    """
    # Implementation follows...
```

### 2. Keep Examples Current

```python
# Use automated testing to ensure examples work
def validate_email(email: str) -> bool:
    """Validate an email address format.
    
    Example:
        >>> validate_email("user@example.com")  # doctest: +SKIP
        True
        >>> validate_email("invalid-email")     # doctest: +SKIP  
        False
    
    Note: Examples marked with +SKIP to avoid doctest in CI
    """
```

### 3. Document Performance Characteristics

```python
def sort_large_dataset(data: List[int]) -> List[int]:
    """Sort a large dataset efficiently.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Performance Notes:
        - For datasets < 1000 items: ~1ms
        - For datasets < 100,000 items: ~100ms  
        - For datasets > 1,000,000 items: Consider using external sorting
    
    Args:
        data: List of integers to sort
    
    Returns:
        Sorted list of integers
    """
```

### 4. Include Migration Guides

```python
def new_api_function(param: str) -> str:
    """New improved API function.
    
    This function replaces the deprecated `old_api_function`.
    
    Migration Guide:
        Old usage:
        >>> result = old_api_function(param, extra_param=True)
        
        New usage:
        >>> result = new_api_function(param)
        
        The `extra_param` is no longer needed as it's handled automatically.
    """
```

### 5. Use Consistent Terminology

Maintain a glossary of terms:

```python
"""
Glossary:
    - Record: A single row of data
    - Dataset: A collection of records
    - Pipeline: A series of data processing steps
    - Transformer: A component that modifies data
    - Sink: A destination for processed data
    - Source: An origin of data
"""
```

### 6. Document Async Code Properly

```python
import asyncio
from typing import AsyncIterator

async def process_stream(data_stream: AsyncIterator[bytes]) -> AsyncIterator[dict]:
    """Process a stream of data asynchronously.
    
    This coroutine processes data as it arrives, yielding results
    incrementally for memory efficiency.
    
    Args:
        data_stream: Async iterator of raw byte data
    
    Yields:
        dict: Processed data records
    
    Example:
        >>> async def example():
        ...     async for record in process_stream(data_source):
        ...         print(f"Processed: {record['id']}")
        >>> asyncio.run(example())
    
    Note:
        This function should be called with `async for` in an async context.
    """
```

## Documentation Checklist

Before submitting code, ensure:

- [ ] All public functions have docstrings
- [ ] All public classes have docstrings  
- [ ] All parameters are documented with types
- [ ] Return values are documented
- [ ] All exceptions are documented
- [ ] At least one example is provided
- [ ] Examples are tested and working
- [ ] Type hints are present and accurate
- [ ] Performance notes included for expensive operations
- [ ] Migration guides provided for API changes
- [ ] Async functions properly documented

## Tools and Automation

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-docstrings
        name: Check docstrings
        entry: python scripts/check_docstrings.py
        language: system
        files: \.py$
```

### Documentation Coverage

```python
# scripts/doc_coverage.py
import ast
import os
from typing import List, Tuple

def check_docstring_coverage(directory: str) -> float:
    """Check what percentage of functions have docstrings."""
    total_functions = 0
    documented_functions = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                functions, documented = analyze_file(file_path)
                total_functions += functions
                documented_functions += documented
    
    return (documented_functions / total_functions) * 100 if total_functions > 0 else 0

def analyze_file(file_path: str) -> Tuple[int, int]:
    """Analyze a single Python file for docstring coverage."""
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    
    functions = 0
    documented = 0
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith('_'):  # Only check public functions
                functions += 1
                if ast.get_docstring(node):
                    documented += 1
    
    return functions, documented

if __name__ == "__main__":
    coverage = check_docstring_coverage("src/")
    print(f"Documentation coverage: {coverage:.1f}%")
```

---

This guide should be updated as the project evolves and new documentation needs arise.