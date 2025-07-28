#!/usr/bin/env python3
"""Comprehensive API usage examples.

This module provides complete examples demonstrating how to use all
the public APIs, functions, and components in the project.

Examples include:
    - Basic data processing workflows
    - Advanced configuration scenarios
    - Error handling patterns
    - File I/O operations
    - Validation and schema checking
    - Custom processors and validators
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any

# Import the documented APIs
from data_processor import (
    DataProcessor, 
    DataValidator, 
    ProcessingResult,
    load_data,
    save_data,
    validate_schema,
    SUPPORTED_FORMATS,
    DEFAULT_CONFIG
)

# Configure logging for examples
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_basic_usage():
    """Demonstrate basic API usage patterns.
    
    This example shows the simplest way to use the DataProcessor
    for basic data processing tasks.
    """
    print("🔥 Basic Usage Example")
    print("-" * 40)
    
    # Sample data
    sample_data = [
        {"name": "Alice Johnson", "age": 28, "email": "alice@example.com", "city": "New York"},
        {"name": "Bob Smith", "age": 32, "email": "bob@example.com", "city": "Los Angeles"},
        {"name": "Carol Brown", "age": 25, "email": "", "city": "Chicago"},  # Missing email
        {"name": "", "age": 29, "email": "dave@example.com", "city": ""},    # Missing name and city
    ]
    
    # Initialize processor with default settings
    processor = DataProcessor()
    success = processor.initialize()
    
    if not success:
        print("❌ Failed to initialize processor")
        return
    
    print(f"✅ Processor initialized successfully")
    print(f"📊 Status: {processor.get_status()}")
    
    # Process data with basic transformations
    result = processor.process(sample_data, transformations=["clean", "normalize"])
    
    # Display results
    print(f"\n📈 Processing Results:")
    print(f"   Records processed: {result.records_processed}")
    print(f"   Records failed: {result.records_failed}")
    print(f"   Success rate: {result.success_rate:.1%}")
    print(f"   Processing time: {result.processing_time:.3f}s")
    
    if result.data:
        print(f"\n📋 Sample processed records:")
        for i, record in enumerate(result.data[:2]):  # Show first 2 records
            print(f"   {i+1}. {record}")
    
    if result.errors:
        print(f"\n⚠️  Errors encountered:")
        for error in result.errors[:3]:  # Show first 3 errors
            print(f"   - {error}")


def example_advanced_configuration():
    """Demonstrate advanced configuration options.
    
    This example shows how to use custom configurations,
    validators, and error handling strategies.
    """
    print("\n🚀 Advanced Configuration Example")
    print("-" * 40)
    
    # Define a custom schema for validation
    user_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "age": {"type": "integer", "minimum": 0, "maximum": 150},
            "email": {"type": "string"},
            "city": {"type": "string"}
        },
        "required": ["name", "age"]
    }
    
    # Advanced configuration
    config = {
        "validation_enabled": True,
        "error_handling": "continue",  # Continue processing even with errors
        "batch_size": 2,  # Small batch size for demonstration
        "timeout": 60,
        "debug": True
    }
    
    # Create processor with custom configuration
    processor = DataProcessor(config)
    
    # Set up custom validator
    validator = DataValidator(schema=user_schema, strict_mode=False)
    processor.set_validator(validator)
    
    # Initialize
    if not processor.initialize():
        print("❌ Failed to initialize processor")
        return
    
    print(f"✅ Advanced processor initialized")
    print(f"📊 Configuration: {processor.config}")
    
    # Test data with various validation scenarios
    test_data = [
        {"name": "Valid User", "age": 30, "email": "valid@example.com", "city": "Boston"},
        {"name": "", "age": 25, "email": "invalid1@example.com"},  # Missing name
        {"name": "User2", "age": -5, "email": "invalid2@example.com"},  # Invalid age
        {"name": "User3", "age": 200, "email": "invalid3@example.com"},  # Age too high
        {"name": "Valid User 2", "age": 22, "email": "valid2@example.com", "city": "Seattle"},
    ]
    
    # Process with all transformations
    result = processor.process(test_data, transformations=["validate", "clean", "normalize"])
    
    print(f"\n📈 Advanced Processing Results:")
    print(f"   Total input records: {len(test_data)}")
    print(f"   Records processed: {result.records_processed}")
    print(f"   Records failed: {result.records_failed}")
    print(f"   Success rate: {result.success_rate:.1%}")
    
    # Show processed data
    if result.data:
        print(f"\n✅ Successfully processed records:")
        for i, record in enumerate(result.data):
            print(f"   {i+1}. {record}")
    
    # Show validation errors
    if result.errors:
        print(f"\n❌ Validation errors:")
        for error in result.errors:
            print(f"   - {error}")


def example_file_operations():
    """Demonstrate file I/O operations.
    
    This example shows how to load data from files,
    process it, and save the results in different formats.
    """
    print("\n📁 File Operations Example")
    print("-" * 40)
    
    # Create sample data files for demonstration
    sample_csv_data = [
        {"product_id": "P001", "product_name": "Laptop", "price": 999.99, "category": "Electronics"},
        {"product_id": "P002", "product_name": "Mouse", "price": 29.99, "category": "Electronics"},
        {"product_id": "P003", "product_name": "", "price": 15.50, "category": "Office"},  # Missing name
        {"product_id": "", "product_name": "Keyboard", "price": 79.99, "category": ""},   # Missing ID and category
    ]
    
    sample_json_data = [
        {"user_id": 1, "username": "john_doe", "status": "active", "last_login": "2024-01-15"},
        {"user_id": 2, "username": "jane_smith", "status": "inactive", "last_login": "2024-01-10"},
        {"user_id": 3, "username": "", "status": "active", "last_login": ""},  # Missing data
    ]
    
    # Create example directory
    example_dir = Path("temp_examples")
    example_dir.mkdir(exist_ok=True)
    
    try:
        # Save sample data to files
        save_data(sample_csv_data, str(example_dir / "products.csv"))
        save_data(sample_json_data, str(example_dir / "users.json"))
        
        print(f"✅ Created sample files:")
        print(f"   - {example_dir / 'products.csv'}")
        print(f"   - {example_dir / 'users.json'}")
        
        # Initialize processor for file operations
        processor = DataProcessor({
            "validation_enabled": True,
            "error_handling": "continue"
        })
        processor.initialize()
        
        # Process CSV file
        print(f"\n📊 Processing CSV file...")
        csv_result = processor.process_file(
            str(example_dir / "products.csv"),
            str(example_dir / "processed_products.json"),
            transformations=["clean", "normalize"]
        )
        
        print(f"   CSV processing: {csv_result.records_processed} records processed")
        
        # Process JSON file
        print(f"\n📊 Processing JSON file...")
        json_result = processor.process_file(
            str(example_dir / "users.json"),
            str(example_dir / "processed_users.csv"),
            transformations=["clean"]
        )
        
        print(f"   JSON processing: {json_result.records_processed} records processed")
        
        # Demonstrate loading data directly
        print(f"\n📖 Loading data directly:")
        loaded_csv = load_data(str(example_dir / "products.csv"))
        loaded_json = load_data(str(example_dir / "users.json"))
        
        print(f"   Loaded {len(loaded_csv)} records from CSV")
        print(f"   Loaded {len(loaded_json)} records from JSON")
        
        # Show supported formats
        print(f"\n📋 Supported formats: {SUPPORTED_FORMATS}")
        
    except Exception as e:
        print(f"❌ Error in file operations: {e}")
    
    finally:
        # Cleanup
        import shutil
        if example_dir.exists():
            shutil.rmtree(example_dir)
            print(f"🧹 Cleaned up temporary files")


def example_schema_validation():
    """Demonstrate schema validation capabilities.
    
    This example shows how to validate data against
    JSON schemas and handle validation errors.
    """
    print("\n🔍 Schema Validation Example")
    print("-" * 40)
    
    # Define comprehensive schema
    product_schema = {
        "type": "object",
        "properties": {
            "product_id": {"type": "string", "pattern": "^P\\d{3}$"},
            "product_name": {"type": "string", "minLength": 1},
            "price": {"type": "number", "minimum": 0},
            "category": {"type": "string", "enum": ["Electronics", "Office", "Home", "Sports"]},
            "in_stock": {"type": "boolean"}
        },
        "required": ["product_id", "product_name", "price", "category"]
    }
    
    # Test data with various validation scenarios
    test_products = [
        # Valid products
        {"product_id": "P001", "product_name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
        {"product_id": "P002", "product_name": "Mouse", "price": 29.99, "category": "Electronics", "in_stock": False},
        
        # Invalid products
        {"product_id": "INVALID", "product_name": "Bad ID", "price": 50.0, "category": "Electronics"},  # Bad ID format
        {"product_id": "P003", "product_name": "", "price": 15.50, "category": "Office"},  # Empty name
        {"product_id": "P004", "product_name": "Negative Price", "price": -10.0, "category": "Home"},  # Negative price
        {"product_id": "P005", "product_name": "Bad Category", "price": 25.0, "category": "InvalidCategory"},  # Invalid category
        {"product_name": "Missing ID", "price": 40.0, "category": "Sports"},  # Missing required field
    ]
    
    print(f"🧪 Testing {len(test_products)} products against schema...")
    
    # Validate using the utility function
    is_valid, errors = validate_schema(test_products, product_schema)
    
    print(f"\n📊 Validation Results:")
    print(f"   Overall valid: {is_valid}")
    print(f"   Error count: {len(errors)}")
    
    if errors:
        print(f"\n❌ Validation errors:")
        for error in errors:
            print(f"   - {error}")
    
    # Test individual validation
    print(f"\n🔬 Individual validation tests:")
    validator = DataValidator(product_schema, strict_mode=False)
    
    for i, product in enumerate(test_products):
        is_product_valid = validator.validate(product)
        status = "✅" if is_product_valid else "❌"
        print(f"   {status} Product {i+1}: {product.get('product_name', 'Unknown')} - Valid: {is_product_valid}")
        
        if not is_product_valid and validator.validation_errors:
            for error in validator.validation_errors:
                print(f"      - {error}")


def example_error_handling():
    """Demonstrate comprehensive error handling patterns.
    
    This example shows different error handling strategies
    and how to recover from various error conditions.
    """
    print("\n⚠️ Error Handling Example")
    print("-" * 40)
    
    # Problematic data that will cause various errors
    problematic_data = [
        {"valid": "record", "type": "good"},
        None,  # This will cause a processing error
        {"incomplete": "record"},  # Missing expected fields
        {"type": "string", "number": "not_a_number"},  # Type mismatch
        {},  # Empty record
    ]
    
    print(f"🧪 Testing different error handling strategies...")
    
    # Test 1: Strict error handling (stops on first error)
    print(f"\n1️⃣ Strict Error Handling:")
    try:
        strict_processor = DataProcessor({
            "validation_enabled": True,
            "error_handling": "strict",
            "batch_size": 1
        })
        strict_processor.initialize()
        
        result = strict_processor.process(problematic_data, transformations=["validate"])
        print(f"   Unexpected success: {result.records_processed} records processed")
        
    except Exception as e:
        print(f"   ❌ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 2: Continue error handling (skip errors and continue)
    print(f"\n2️⃣ Continue Error Handling:")
    continue_processor = DataProcessor({
        "validation_enabled": True,
        "error_handling": "continue",
        "batch_size": 10
    })
    continue_processor.initialize()
    
    result = continue_processor.process(problematic_data, transformations=["clean"])
    print(f"   Records processed: {result.records_processed}")
    print(f"   Records failed: {result.records_failed}")
    print(f"   Success rate: {result.success_rate:.1%}")
    
    if result.errors:
        print(f"   Errors (showing first 3):")
        for error in result.errors[:3]:
            print(f"   - {error}")
    
    # Test 3: File operation errors
    print(f"\n3️⃣ File Operation Error Handling:")
    try:
        # Try to load non-existent file
        load_data("non_existent_file.csv")
    except FileNotFoundError as e:
        print(f"   ❌ File not found (expected): {e}")
    
    try:
        # Try to load unsupported format
        load_data("test.unsupported_format")
    except ValueError as e:
        print(f"   ❌ Unsupported format (expected): {e}")
    
    # Test 4: Schema validation errors
    print(f"\n4️⃣ Schema Validation Error Handling:")
    invalid_schema = {"invalid": "schema", "type": "unknown_type"}
    
    try:
        validator = DataValidator(invalid_schema, strict_mode=True)
        validator.validate({"test": "data"})
    except Exception as e:
        print(f"   ❌ Schema validation error: {type(e).__name__}: {e}")


def example_custom_processor():
    """Demonstrate creating custom processors and validators.
    
    This example shows how to extend the base functionality
    with custom processing logic and validation rules.
    """
    print("\n🔧 Custom Processor Example")
    print("-" * 40)
    
    class CustomDataProcessor(DataProcessor):
        """Custom processor with additional transformations."""
        
        def _process_record(self, record: Dict[str, Any], 
                           transformations: List[str]) -> Dict[str, Any]:
            """Override to add custom transformations."""
            # Call parent implementation first
            processed = super()._process_record(record, transformations)
            
            if processed is None:
                return None
            
            # Add custom transformations
            for transformation in transformations:
                if transformation == "add_metadata":
                    processed["_processed_at"] = "2024-01-15T10:00:00Z"
                    processed["_processor_version"] = "1.0.0"
                elif transformation == "calculate_score":
                    # Example: calculate a score based on age
                    age = processed.get("age", 0)
                    processed["score"] = min(100, max(0, age * 2))
                elif transformation == "format_name":
                    # Example: format name to title case
                    name = processed.get("name", "")
                    if name:
                        processed["name"] = name.title()
            
            return processed
    
    # Test custom processor
    custom_data = [
        {"name": "alice johnson", "age": 25, "department": "engineering"},
        {"name": "bob smith", "age": 30, "department": "marketing"},
        {"name": "carol brown", "age": 28, "department": "sales"},
    ]
    
    print(f"🔄 Testing custom processor with {len(custom_data)} records...")
    
    # Initialize custom processor
    custom_processor = CustomDataProcessor({
        "validation_enabled": False,
        "error_handling": "continue"
    })
    custom_processor.initialize()
    
    # Process with custom transformations
    result = custom_processor.process(
        custom_data, 
        transformations=["format_name", "add_metadata", "calculate_score"]
    )
    
    print(f"📊 Custom processing results:")
    print(f"   Records processed: {result.records_processed}")
    print(f"   Processing time: {result.processing_time:.3f}s")
    
    if result.data:
        print(f"\n📋 Processed records with custom fields:")
        for i, record in enumerate(result.data):
            print(f"   {i+1}. {record}")


def example_performance_testing():
    """Demonstrate performance testing and optimization.
    
    This example shows how to test processing performance
    with different batch sizes and configurations.
    """
    print("\n⚡ Performance Testing Example")
    print("-" * 40)
    
    # Generate larger dataset for performance testing
    large_dataset = []
    for i in range(1000):
        large_dataset.append({
            "id": f"ID{i:04d}",
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "age": 20 + (i % 50),
            "department": ["Engineering", "Marketing", "Sales", "HR"][i % 4]
        })
    
    print(f"📊 Testing performance with {len(large_dataset)} records...")
    
    # Test different batch sizes
    batch_sizes = [100, 500, 1000]
    
    for batch_size in batch_sizes:
        print(f"\n🔄 Testing batch size: {batch_size}")
        
        processor = DataProcessor({
            "validation_enabled": True,
            "error_handling": "continue",
            "batch_size": batch_size
        })
        processor.initialize()
        
        result = processor.process(large_dataset, transformations=["clean", "normalize"])
        
        print(f"   Records processed: {result.records_processed}")
        print(f"   Processing time: {result.processing_time:.3f}s")
        print(f"   Records per second: {result.records_processed / result.processing_time:.1f}")
        print(f"   Memory usage: {len(str(result.data)) / 1024:.1f} KB")


def main():
    """Run all API usage examples."""
    print("🎯 Comprehensive API Usage Examples")
    print("=" * 50)
    print("This demonstration covers all documented APIs and features.")
    print()
    
    try:
        # Run all examples
        example_basic_usage()
        example_advanced_configuration()
        example_file_operations()
        example_schema_validation()
        example_error_handling()
        example_custom_processor()
        example_performance_testing()
        
        print("\n" + "=" * 50)
        print("✅ All examples completed successfully!")
        print("📚 Check the documentation for more details on each feature.")
        
    except Exception as e:
        print(f"\n❌ Example execution failed: {e}")
        logger.exception("Error running examples")


if __name__ == "__main__":
    main()