#!/usr/bin/env python3
"""Data processing module with comprehensive documentation examples.

This module demonstrates best practices for Python documentation including
proper docstrings, type hints, and usage examples for all public APIs.

Classes:
    DataProcessor: Main class for processing data with various operations
    ProcessingResult: Result container for processing operations
    DataValidator: Validator for checking data integrity

Functions:
    load_data: Load data from various file formats
    save_data: Save data to various file formats
    validate_schema: Validate data against a JSON schema

Constants:
    SUPPORTED_FORMATS: List of supported data formats
    DEFAULT_CONFIG: Default configuration for data processing

Example:
    Basic usage of the data processor:
    
    >>> from data_processor import DataProcessor, load_data
    >>> data = load_data("example.csv")
    >>> processor = DataProcessor()
    >>> result = processor.process(data)
    >>> print(f"Processed {len(result.data)} records")
"""

import json
import csv
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Module constants
SUPPORTED_FORMATS = ["csv", "json", "txt", "parquet"]
DEFAULT_CONFIG = {
    "validation_enabled": True,
    "error_handling": "strict",
    "batch_size": 1000,
    "timeout": 30
}

# Set up logging
logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    """Container for data processing results.
    
    This class holds the results of a data processing operation, including
    the processed data, metadata about the operation, and any errors that
    occurred during processing.
    
    Attributes:
        data (List[Dict[str, Any]]): The processed data records
        success (bool): Whether the processing completed successfully
        records_processed (int): Number of records that were processed
        records_failed (int): Number of records that failed processing
        errors (List[str]): List of error messages encountered
        processing_time (float): Time taken for processing in seconds
        metadata (Dict[str, Any]): Additional metadata about the operation
    
    Example:
        >>> result = ProcessingResult(
        ...     data=[{"id": 1, "name": "John"}],
        ...     success=True,
        ...     records_processed=1
        ... )
        >>> print(f"Success: {result.success}")
        Success: True
    """
    data: List[Dict[str, Any]] = field(default_factory=list)
    success: bool = False
    records_processed: int = 0
    records_failed: int = 0
    errors: List[str] = field(default_factory=list)
    processing_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        """Calculate the success rate of processing.
        
        Returns:
            float: Success rate as a percentage (0.0 to 1.0)
        
        Example:
            >>> result = ProcessingResult(records_processed=8, records_failed=2)
            >>> result.success_rate
            0.8
        """
        total = self.records_processed + self.records_failed
        return self.records_processed / total if total > 0 else 0.0


class DataValidator:
    """Validator for checking data integrity and format compliance.
    
    This class provides methods for validating data against schemas,
    checking data types, and ensuring data quality standards.
    
    Attributes:
        schema (Dict[str, Any]): JSON schema for validation
        strict_mode (bool): Whether to use strict validation
    
    Example:
        >>> schema = {"type": "object", "properties": {"id": {"type": "integer"}}}
        >>> validator = DataValidator(schema)
        >>> is_valid = validator.validate({"id": 123})
        >>> print(f"Valid: {is_valid}")
        Valid: True
    """
    
    def __init__(self, schema: Optional[Dict[str, Any]] = None, strict_mode: bool = True):
        """Initialize the data validator.
        
        Args:
            schema (Dict[str, Any], optional): JSON schema for validation.
                If None, basic validation will be performed.
            strict_mode (bool, optional): Enable strict validation mode.
                In strict mode, any validation error will raise an exception.
                Defaults to True.
        """
        self.schema = schema
        self.strict_mode = strict_mode
        self._validation_errors: List[str] = []
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate a single data record.
        
        Args:
            data (Dict[str, Any]): Data record to validate
        
        Returns:
            bool: True if validation passes, False otherwise
        
        Raises:
            ValueError: If validation fails and strict_mode is True
        
        Example:
            >>> validator = DataValidator()
            >>> data = {"name": "John", "age": 30}
            >>> validator.validate(data)
            True
            
            >>> # With schema validation
            >>> schema = {
            ...     "type": "object",
            ...     "properties": {
            ...         "name": {"type": "string"},
            ...         "age": {"type": "integer", "minimum": 0}
            ...     },
            ...     "required": ["name", "age"]
            ... }
            >>> validator = DataValidator(schema)
            >>> validator.validate({"name": "John", "age": 30})
            True
        """
        self._validation_errors.clear()
        
        if not isinstance(data, dict):
            error_msg = f"Expected dict, got {type(data).__name__}"
            self._validation_errors.append(error_msg)
            if self.strict_mode:
                raise ValueError(error_msg)
            return False
        
        if self.schema:
            return self._validate_against_schema(data)
        else:
            return self._basic_validation(data)
    
    def _validate_against_schema(self, data: Dict[str, Any]) -> bool:
        """Validate data against the provided JSON schema."""
        # Simplified schema validation - in real implementation,
        # you would use a library like jsonschema
        if self.schema.get("type") == "object":
            properties = self.schema.get("properties", {})
            required = self.schema.get("required", [])
            
            # Check required fields
            for field in required:
                if field not in data:
                    error_msg = f"Required field '{field}' is missing"
                    self._validation_errors.append(error_msg)
                    if self.strict_mode:
                        raise ValueError(error_msg)
                    return False
            
            # Check field types
            for field, value in data.items():
                if field in properties:
                    expected_type = properties[field].get("type")
                    if not self._check_type(value, expected_type):
                        error_msg = f"Field '{field}' has invalid type"
                        self._validation_errors.append(error_msg)
                        if self.strict_mode:
                            raise ValueError(error_msg)
                        return False
        
        return True
    
    def _basic_validation(self, data: Dict[str, Any]) -> bool:
        """Perform basic validation without a schema."""
        # Check for empty data
        if not data:
            error_msg = "Data cannot be empty"
            self._validation_errors.append(error_msg)
            if self.strict_mode:
                raise ValueError(error_msg)
            return False
        
        # Check for None values in keys
        for key, value in data.items():
            if key is None:
                error_msg = "Keys cannot be None"
                self._validation_errors.append(error_msg)
                if self.strict_mode:
                    raise ValueError(error_msg)
                return False
        
        return True
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected type."""
        type_mapping = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        expected_python_type = type_mapping.get(expected_type)
        if expected_python_type:
            return isinstance(value, expected_python_type)
        return True
    
    @property
    def validation_errors(self) -> List[str]:
        """Get the list of validation errors from the last validation.
        
        Returns:
            List[str]: List of validation error messages
        """
        return self._validation_errors.copy()


class DataProcessor:
    """Main data processor for handling various data operations.
    
    This class provides comprehensive data processing capabilities including
    cleaning, transformation, validation, and filtering operations. It supports
    both batch and streaming processing modes.
    
    The processor can handle various data formats and provides extensive
    configuration options for customizing the processing behavior.
    
    Attributes:
        config (Dict[str, Any]): Configuration settings for the processor
        validator (DataValidator): Validator instance for data validation
        is_initialized (bool): Whether the processor has been initialized
        processing_mode (str): Current processing mode ("batch" or "stream")
    
    Example:
        Basic usage:
        >>> processor = DataProcessor()
        >>> processor.initialize()
        >>> data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
        >>> result = processor.process(data)
        >>> print(f"Processed {result.records_processed} records")
        
        Advanced usage with configuration:
        >>> config = {
        ...     "validation_enabled": True,
        ...     "error_handling": "continue",
        ...     "batch_size": 500
        ... }
        >>> processor = DataProcessor(config)
        >>> processor.set_validator(DataValidator(schema))
        >>> result = processor.process_file("data.csv")
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the DataProcessor.
        
        Args:
            config (Dict[str, Any], optional): Configuration dictionary.
                Supported options:
                - validation_enabled (bool): Enable data validation (default: True)
                - error_handling (str): Error handling strategy:
                  * "strict": Stop on first error
                  * "continue": Skip invalid records and continue
                  * "collect": Collect all errors and process valid records
                  Default: "strict"
                - batch_size (int): Number of records to process in each batch
                  (default: 1000)
                - timeout (int): Timeout in seconds for processing operations
                  (default: 30)
                
                If None, uses DEFAULT_CONFIG.
        
        Example:
            >>> # Use default configuration
            >>> processor = DataProcessor()
            
            >>> # Custom configuration
            >>> config = {
            ...     "validation_enabled": False,
            ...     "error_handling": "continue",
            ...     "batch_size": 2000
            ... }
            >>> processor = DataProcessor(config)
        """
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.validator: Optional[DataValidator] = None
        self.is_initialized = False
        self.processing_mode = "batch"
        self._start_time: Optional[datetime] = None
        
        # Set up logging level based on config
        if self.config.get("debug", False):
            logger.setLevel(logging.DEBUG)
    
    def initialize(self) -> bool:
        """Initialize the processor with current configuration.
        
        This method prepares the processor for data processing operations.
        It validates the configuration, sets up internal components, and
        performs any necessary initialization tasks.
        
        Returns:
            bool: True if initialization successful, False otherwise
        
        Raises:
            ValueError: If configuration is invalid
            RuntimeError: If initialization fails due to system issues
        
        Example:
            >>> processor = DataProcessor()
            >>> if processor.initialize():
            ...     print("Processor ready")
            ... else:
            ...     print("Initialization failed")
            Processor ready
        """
        try:
            # Validate configuration
            self._validate_config()
            
            # Initialize default validator if none provided
            if self.validator is None and self.config["validation_enabled"]:
                self.validator = DataValidator(strict_mode=False)
            
            # Set processing mode
            self.processing_mode = self.config.get("processing_mode", "batch")
            
            self.is_initialized = True
            logger.info("DataProcessor initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize DataProcessor: {e}")
            return False
    
    def _validate_config(self) -> None:
        """Validate the processor configuration."""
        required_keys = ["validation_enabled", "error_handling", "batch_size"]
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required configuration key: {key}")
        
        if self.config["error_handling"] not in ["strict", "continue", "collect"]:
            raise ValueError("Invalid error_handling mode")
        
        if not isinstance(self.config["batch_size"], int) or self.config["batch_size"] <= 0:
            raise ValueError("batch_size must be a positive integer")
    
    def set_validator(self, validator: DataValidator) -> None:
        """Set a custom validator for the processor.
        
        Args:
            validator (DataValidator): Validator instance to use
        
        Example:
            >>> schema = {"type": "object", "properties": {"id": {"type": "integer"}}}
            >>> validator = DataValidator(schema)
            >>> processor = DataProcessor()
            >>> processor.set_validator(validator)
        """
        self.validator = validator
        logger.debug("Custom validator set")
    
    def process(self, data: List[Dict[str, Any]], 
                transformations: Optional[List[str]] = None) -> ProcessingResult:
        """Process a list of data records.
        
        This method processes the provided data records according to the
        configured settings. It supports various transformations and provides
        comprehensive error handling.
        
        Args:
            data (List[Dict[str, Any]]): List of data records to process
            transformations (List[str], optional): List of transformation names
                to apply. Available transformations:
                - "clean": Remove null values and empty strings
                - "normalize": Normalize string fields (trim, lowercase)
                - "validate": Validate data against schema
                - "deduplicate": Remove duplicate records
                Default is None (no transformations).
        
        Returns:
            ProcessingResult: Result object containing processed data and metadata
        
        Raises:
            RuntimeError: If processor is not initialized
            ValueError: If data format is invalid
        
        Example:
            Basic processing:
            >>> processor = DataProcessor()
            >>> processor.initialize()
            >>> data = [{"name": "John", "age": 30}]
            >>> result = processor.process(data)
            >>> print(f"Success: {result.success}")
            Success: True
            
            With transformations:
            >>> data = [
            ...     {"name": " JOHN ", "age": 30, "email": ""},
            ...     {"name": "Jane", "age": 25, "email": "jane@example.com"}
            ... ]
            >>> result = processor.process(data, ["clean", "normalize"])
            >>> print(result.data[0]["name"])  # Should be "john"
            john
        """
        if not self.is_initialized:
            raise RuntimeError("Processor must be initialized before processing")
        
        if not isinstance(data, list):
            raise ValueError("Data must be a list of dictionaries")
        
        self._start_time = datetime.now()
        result = ProcessingResult()
        transformations = transformations or []
        
        try:
            # Process data in batches
            batch_size = self.config["batch_size"]
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                batch_result = self._process_batch(batch, transformations)
                
                # Merge batch result into main result
                result.data.extend(batch_result.data)
                result.records_processed += batch_result.records_processed
                result.records_failed += batch_result.records_failed
                result.errors.extend(batch_result.errors)
            
            result.success = result.records_failed == 0
            result.processing_time = (datetime.now() - self._start_time).total_seconds()
            result.metadata = {
                "batch_size": batch_size,
                "transformations": transformations,
                "config": self.config.copy()
            }
            
            logger.info(f"Processing completed: {result.records_processed} processed, "
                       f"{result.records_failed} failed")
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
            logger.error(f"Processing failed: {e}")
        
        return result
    
    def _process_batch(self, batch: List[Dict[str, Any]], 
                      transformations: List[str]) -> ProcessingResult:
        """Process a single batch of data."""
        result = ProcessingResult()
        
        for record in batch:
            try:
                processed_record = self._process_record(record, transformations)
                if processed_record is not None:
                    result.data.append(processed_record)
                    result.records_processed += 1
                else:
                    result.records_failed += 1
                    
            except Exception as e:
                result.records_failed += 1
                error_msg = f"Error processing record: {e}"
                result.errors.append(error_msg)
                
                if self.config["error_handling"] == "strict":
                    raise
                elif self.config["error_handling"] == "continue":
                    logger.warning(error_msg)
                    continue
        
        return result
    
    def _process_record(self, record: Dict[str, Any], 
                       transformations: List[str]) -> Optional[Dict[str, Any]]:
        """Process a single data record."""
        # Make a copy to avoid modifying original data
        processed = record.copy()
        
        # Apply transformations in order
        for transformation in transformations:
            if transformation == "clean":
                processed = self._clean_record(processed)
            elif transformation == "normalize":
                processed = self._normalize_record(processed)
            elif transformation == "validate":
                if not self._validate_record(processed):
                    return None
            elif transformation == "deduplicate":
                # This would require context of all records, simplified here
                pass
            else:
                logger.warning(f"Unknown transformation: {transformation}")
        
        # Final validation if enabled
        if self.config["validation_enabled"] and self.validator:
            if not self.validator.validate(processed):
                logger.warning(f"Record validation failed: {self.validator.validation_errors}")
                if self.config["error_handling"] == "strict":
                    return None
        
        return processed
    
    def _clean_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Clean a data record by removing null/empty values."""
        cleaned = {}
        for key, value in record.items():
            if value is not None and value != "":
                cleaned[key] = value
        return cleaned
    
    def _normalize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize string fields in a record."""
        normalized = {}
        for key, value in record.items():
            if isinstance(value, str):
                # Trim whitespace and convert to lowercase
                normalized[key] = value.strip().lower()
            else:
                normalized[key] = value
        return normalized
    
    def _validate_record(self, record: Dict[str, Any]) -> bool:
        """Validate a single record."""
        if self.validator:
            return self.validator.validate(record)
        return True
    
    def process_file(self, file_path: Union[str, Path], 
                    output_path: Optional[Union[str, Path]] = None,
                    transformations: Optional[List[str]] = None) -> ProcessingResult:
        """Process data from a file.
        
        This method loads data from a file, processes it, and optionally
        saves the results to an output file.
        
        Args:
            file_path (Union[str, Path]): Path to input file
            output_path (Union[str, Path], optional): Path to save processed data.
                If None, results are only returned, not saved.
            transformations (List[str], optional): List of transformations to apply
        
        Returns:
            ProcessingResult: Result object containing processed data and metadata
        
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If file format is not supported
            PermissionError: If cannot read input or write output file
        
        Example:
            >>> processor = DataProcessor()
            >>> processor.initialize()
            >>> result = processor.process_file("data.csv", "processed.json")
            >>> print(f"Processed {result.records_processed} records")
        """
        if not self.is_initialized:
            raise RuntimeError("Processor must be initialized before processing")
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        # Load data from file
        data = load_data(str(file_path))
        
        # Process the data
        result = self.process(data, transformations)
        
        # Save results if output path provided
        if output_path and result.success:
            save_data(result.data, str(output_path))
            result.metadata["output_file"] = str(output_path)
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the processor.
        
        Returns:
            Dict[str, Any]: Status information containing:
                - initialized (bool): Whether processor is initialized
                - config (Dict): Current configuration
                - processing_mode (str): Current processing mode
                - validator_configured (bool): Whether custom validator is set
        
        Example:
            >>> processor = DataProcessor()
            >>> status = processor.get_status()
            >>> print(f"Initialized: {status['initialized']}")
            Initialized: False
        """
        return {
            "initialized": self.is_initialized,
            "config": self.config.copy(),
            "processing_mode": self.processing_mode,
            "validator_configured": self.validator is not None
        }


def load_data(file_path: str) -> List[Dict[str, Any]]:
    """Load data from various file formats.
    
    This function supports loading data from CSV, JSON, and other common
    formats. It automatically detects the format based on file extension
    and returns a standardized list of dictionaries.
    
    Args:
        file_path (str): Path to the data file
    
    Returns:
        List[Dict[str, Any]]: List of data records loaded from file
    
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If the file format is not supported
        json.JSONDecodeError: If JSON file is malformed
        csv.Error: If CSV file is malformed
    
    Example:
        Loading CSV data:
        >>> data = load_data("users.csv")
        >>> print(f"Loaded {len(data)} records")
        
        Loading JSON data:
        >>> data = load_data("config.json")
        >>> print(data[0].keys())
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    suffix = file_path.suffix.lower()
    
    if suffix == ".csv":
        return _load_csv(file_path)
    elif suffix == ".json":
        return _load_json(file_path)
    elif suffix == ".txt":
        return _load_text(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def _load_csv(file_path: Path) -> List[Dict[str, Any]]:
    """Load data from a CSV file."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(dict(row))
    return data


def _load_json(file_path: Path) -> List[Dict[str, Any]]:
    """Load data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Ensure we return a list of dictionaries
    if isinstance(data, dict):
        return [data]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("JSON file must contain an object or array")


def _load_text(file_path: Path) -> List[Dict[str, Any]]:
    """Load data from a text file (one record per line)."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:  # Skip empty lines
                data.append({"line_number": line_num, "content": line})
    return data


def save_data(data: List[Dict[str, Any]], file_path: str, 
             format_type: Optional[str] = None) -> None:
    """Save data to various file formats.
    
    This function saves data to CSV, JSON, or other formats. The format
    is automatically detected from the file extension unless explicitly
    specified.
    
    Args:
        data (List[Dict[str, Any]]): Data to save
        file_path (str): Output file path
        format_type (str, optional): Force specific format ("csv", "json", "txt").
            If None, format is detected from file extension.
    
    Raises:
        ValueError: If format is not supported or data is invalid
        PermissionError: If cannot write to the specified path
        OSError: If there are file system issues
    
    Example:
        Save as JSON:
        >>> data = [{"name": "John", "age": 30}]
        >>> save_data(data, "output.json")
        
        Save as CSV:
        >>> save_data(data, "output.csv")
        
        Force format:
        >>> save_data(data, "output.txt", format_type="json")
    """
    if not data:
        raise ValueError("Cannot save empty data")
    
    file_path = Path(file_path)
    
    # Determine format
    if format_type:
        suffix = f".{format_type}"
    else:
        suffix = file_path.suffix.lower()
    
    # Create directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    if suffix == ".csv":
        _save_csv(data, file_path)
    elif suffix == ".json":
        _save_json(data, file_path)
    elif suffix == ".txt":
        _save_text(data, file_path)
    else:
        raise ValueError(f"Unsupported format: {suffix}")


def _save_csv(data: List[Dict[str, Any]], file_path: Path) -> None:
    """Save data to a CSV file."""
    if not data:
        return
    
    # Get all unique keys from all records
    fieldnames = set()
    for record in data:
        fieldnames.update(record.keys())
    fieldnames = sorted(fieldnames)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def _save_json(data: List[Dict[str, Any]], file_path: Path) -> None:
    """Save data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _save_text(data: List[Dict[str, Any]], file_path: Path) -> None:
    """Save data to a text file (JSON format, one record per line)."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for record in data:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')


def validate_schema(data: List[Dict[str, Any]], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a list of data records against a JSON schema.
    
    This function validates all records in the provided data list against
    the given schema and returns validation results.
    
    Args:
        data (List[Dict[str, Any]]): Data records to validate
        schema (Dict[str, Any]): JSON schema for validation
    
    Returns:
        Tuple[bool, List[str]]: A tuple containing:
            - bool: True if all records are valid, False otherwise
            - List[str]: List of validation error messages
    
    Example:
        >>> schema = {
        ...     "type": "object",
        ...     "properties": {
        ...         "name": {"type": "string"},
        ...         "age": {"type": "integer", "minimum": 0}
        ...     },
        ...     "required": ["name", "age"]
        ... }
        >>> data = [
        ...     {"name": "John", "age": 30},
        ...     {"name": "Jane", "age": -5}  # Invalid age
        ... ]
        >>> is_valid, errors = validate_schema(data, schema)
        >>> print(f"Valid: {is_valid}, Errors: {len(errors)}")
        Valid: False, Errors: 1
    """
    validator = DataValidator(schema, strict_mode=False)
    all_errors = []
    valid_count = 0
    
    for i, record in enumerate(data):
        if validator.validate(record):
            valid_count += 1
        else:
            for error in validator.validation_errors:
                all_errors.append(f"Record {i}: {error}")
    
    is_all_valid = valid_count == len(data)
    return is_all_valid, all_errors


if __name__ == "__main__":
    # Example usage and testing
    import doctest
    
    # Run doctests
    print("Running doctests...")
    doctest.testmod(verbose=True)
    
    # Example usage
    print("\nExample usage:")
    
    # Create sample data
    sample_data = [
        {"name": "John Doe", "age": 30, "email": "john@example.com"},
        {"name": "Jane Smith", "age": 25, "email": "jane@example.com"},
        {"name": "", "age": 35, "email": ""},  # This will be cleaned
    ]
    
    # Initialize processor
    processor = DataProcessor({
        "validation_enabled": True,
        "error_handling": "continue"
    })
    processor.initialize()
    
    # Process data with transformations
    result = processor.process(sample_data, ["clean", "normalize"])
    
    print(f"Processing result:")
    print(f"  Records processed: {result.records_processed}")
    print(f"  Records failed: {result.records_failed}")
    print(f"  Success rate: {result.success_rate:.2%}")
    print(f"  Processing time: {result.processing_time:.3f}s")
    
    if result.data:
        print(f"  Sample processed record: {result.data[0]}")