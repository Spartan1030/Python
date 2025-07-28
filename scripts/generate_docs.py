#!/usr/bin/env python3
"""Documentation generation and validation script.

This script provides tools for generating, validating, and maintaining
comprehensive documentation for Python projects.

Functions:
    generate_api_docs: Generate API documentation from source code
    validate_examples: Validate code examples in documentation
    check_coverage: Check documentation coverage
    generate_readme: Generate README from templates
"""

import ast
import os
import sys
import json
import doctest
import importlib
import pkgutil
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import re


@dataclass
class DocStats:
    """Statistics about documentation coverage."""
    total_functions: int = 0
    documented_functions: int = 0
    total_classes: int = 0
    documented_classes: int = 0
    total_modules: int = 0
    documented_modules: int = 0
    
    @property
    def function_coverage(self) -> float:
        """Calculate function documentation coverage."""
        return (self.documented_functions / self.total_functions * 100) if self.total_functions > 0 else 0
    
    @property
    def class_coverage(self) -> float:
        """Calculate class documentation coverage."""
        return (self.documented_classes / self.total_classes * 100) if self.total_classes > 0 else 0
    
    @property
    def module_coverage(self) -> float:
        """Calculate module documentation coverage."""
        return (self.documented_modules / self.total_modules * 100) if self.total_modules > 0 else 0
    
    @property
    def overall_coverage(self) -> float:
        """Calculate overall documentation coverage."""
        total_items = self.total_functions + self.total_classes + self.total_modules
        documented_items = self.documented_functions + self.documented_classes + self.documented_modules
        return (documented_items / total_items * 100) if total_items > 0 else 0


def analyze_file(file_path: Path) -> Tuple[Dict[str, Any], DocStats]:
    """Analyze a Python file for documentation coverage.
    
    Args:
        file_path: Path to the Python file to analyze
    
    Returns:
        Tuple containing file analysis and documentation statistics
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        stats = DocStats()
        analysis = {
            'file_path': str(file_path),
            'functions': [],
            'classes': [],
            'module_docstring': ast.get_docstring(tree) is not None
        }
        
        # Check module docstring
        stats.total_modules = 1
        if analysis['module_docstring']:
            stats.documented_modules = 1
        
        # Analyze functions and classes
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith('_'):  # Only check public functions
                    stats.total_functions += 1
                    has_docstring = ast.get_docstring(node) is not None
                    if has_docstring:
                        stats.documented_functions += 1
                    
                    analysis['functions'].append({
                        'name': node.name,
                        'line': node.lineno,
                        'has_docstring': has_docstring,
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    })
            
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith('_'):  # Only check public classes
                    stats.total_classes += 1
                    has_docstring = ast.get_docstring(node) is not None
                    if has_docstring:
                        stats.documented_classes += 1
                    
                    analysis['classes'].append({
                        'name': node.name,
                        'line': node.lineno,
                        'has_docstring': has_docstring
                    })
        
        return analysis, stats
    
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return {}, DocStats()


def check_documentation_coverage(source_dir: str) -> DocStats:
    """Check documentation coverage for all Python files in a directory.
    
    Args:
        source_dir: Directory containing Python source files
    
    Returns:
        Overall documentation statistics
    """
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"Source directory not found: {source_dir}")
        return DocStats()
    
    total_stats = DocStats()
    undocumented_items = []
    
    print(f"Checking documentation coverage in {source_dir}...")
    print("-" * 60)
    
    for py_file in source_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        analysis, file_stats = analyze_file(py_file)
        
        # Accumulate statistics
        total_stats.total_functions += file_stats.total_functions
        total_stats.documented_functions += file_stats.documented_functions
        total_stats.total_classes += file_stats.total_classes
        total_stats.documented_classes += file_stats.documented_classes
        total_stats.total_modules += file_stats.total_modules
        total_stats.documented_modules += file_stats.documented_modules
        
        # Collect undocumented items
        relative_path = py_file.relative_to(source_path)
        
        if not analysis.get('module_docstring', False):
            undocumented_items.append(f"Module: {relative_path}")
        
        for func in analysis.get('functions', []):
            if not func['has_docstring']:
                undocumented_items.append(f"Function: {relative_path}:{func['line']} {func['name']}()")
        
        for cls in analysis.get('classes', []):
            if not cls['has_docstring']:
                undocumented_items.append(f"Class: {relative_path}:{cls['line']} {cls['name']}")
        
        # Print file summary
        file_coverage = (
            (file_stats.documented_functions + file_stats.documented_classes + file_stats.documented_modules) /
            (file_stats.total_functions + file_stats.total_classes + file_stats.total_modules) * 100
        ) if (file_stats.total_functions + file_stats.total_classes + file_stats.total_modules) > 0 else 0
        
        print(f"{relative_path}: {file_coverage:.1f}% coverage")
    
    print("-" * 60)
    print(f"Overall Coverage Report:")
    print(f"  Functions: {total_stats.documented_functions}/{total_stats.total_functions} ({total_stats.function_coverage:.1f}%)")
    print(f"  Classes:   {total_stats.documented_classes}/{total_stats.total_classes} ({total_stats.class_coverage:.1f}%)")
    print(f"  Modules:   {total_stats.documented_modules}/{total_stats.total_modules} ({total_stats.module_coverage:.1f}%)")
    print(f"  Overall:   {total_stats.overall_coverage:.1f}%")
    
    if undocumented_items:
        print(f"\nUndocumented items ({len(undocumented_items)}):")
        for item in undocumented_items[:20]:  # Show first 20
            print(f"  - {item}")
        if len(undocumented_items) > 20:
            print(f"  ... and {len(undocumented_items) - 20} more")
    
    return total_stats


def validate_docstring_examples(source_dir: str) -> bool:
    """Validate all docstring examples using doctest.
    
    Args:
        source_dir: Directory containing Python source files
    
    Returns:
        True if all examples pass, False otherwise
    """
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"Source directory not found: {source_dir}")
        return False
    
    print(f"Validating docstring examples in {source_dir}...")
    print("-" * 60)
    
    total_failures = 0
    total_tests = 0
    
    # Add source directory to Python path
    sys.path.insert(0, str(source_path.parent))
    
    try:
        # Find and test all Python modules
        for py_file in source_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            
            # Convert file path to module name
            relative_path = py_file.relative_to(source_path.parent)
            module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')
            
            try:
                module = importlib.import_module(module_name)
                result = doctest.testmod(module, verbose=False)
                
                total_failures += result.failed
                total_tests += result.attempted
                
                if result.failed > 0:
                    print(f"❌ {module_name}: {result.failed}/{result.attempted} failed")
                elif result.attempted > 0:
                    print(f"✅ {module_name}: {result.attempted} tests passed")
                
            except Exception as e:
                print(f"❌ Error testing {module_name}: {e}")
                total_failures += 1
    
    finally:
        # Remove from path
        if str(source_path.parent) in sys.path:
            sys.path.remove(str(source_path.parent))
    
    print("-" * 60)
    success_rate = ((total_tests - total_failures) / total_tests * 100) if total_tests > 0 else 0
    print(f"Doctest Results: {total_tests - total_failures}/{total_tests} passed ({success_rate:.1f}%)")
    
    return total_failures == 0


def extract_api_info(source_dir: str) -> Dict[str, Any]:
    """Extract API information from source code for documentation generation.
    
    Args:
        source_dir: Directory containing Python source files
    
    Returns:
        Dictionary containing extracted API information
    """
    source_path = Path(source_dir)
    api_info = {
        'modules': {},
        'classes': {},
        'functions': {},
        'constants': {}
    }
    
    print(f"Extracting API information from {source_dir}...")
    
    for py_file in source_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            relative_path = py_file.relative_to(source_path)
            module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')
            
            # Extract module info
            module_doc = ast.get_docstring(tree)
            api_info['modules'][module_name] = {
                'file_path': str(relative_path),
                'docstring': module_doc,
                'classes': [],
                'functions': [],
                'constants': []
            }
            
            # Extract classes, functions, and constants
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and not node.name.startswith('_'):
                    class_doc = ast.get_docstring(node)
                    class_info = {
                        'name': node.name,
                        'module': module_name,
                        'line': node.lineno,
                        'docstring': class_doc,
                        'methods': []
                    }
                    
                    # Extract methods
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if not item.name.startswith('_') or item.name in ['__init__', '__str__', '__repr__']:
                                method_doc = ast.get_docstring(item)
                                class_info['methods'].append({
                                    'name': item.name,
                                    'line': item.lineno,
                                    'docstring': method_doc,
                                    'is_async': isinstance(item, ast.AsyncFunctionDef)
                                })
                    
                    api_info['classes'][f"{module_name}.{node.name}"] = class_info
                    api_info['modules'][module_name]['classes'].append(node.name)
                
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith('_'):
                    func_doc = ast.get_docstring(node)
                    func_info = {
                        'name': node.name,
                        'module': module_name,
                        'line': node.lineno,
                        'docstring': func_doc,
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    }
                    
                    api_info['functions'][f"{module_name}.{node.name}"] = func_info
                    api_info['modules'][module_name]['functions'].append(node.name)
                
                elif isinstance(node, ast.Assign):
                    # Extract constants (uppercase variables)
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            api_info['constants'][f"{module_name}.{target.id}"] = {
                                'name': target.id,
                                'module': module_name,
                                'line': node.lineno
                            }
                            api_info['modules'][module_name]['constants'].append(target.id)
        
        except Exception as e:
            print(f"Error processing {py_file}: {e}")
    
    return api_info


def generate_markdown_docs(api_info: Dict[str, Any], output_dir: str) -> None:
    """Generate Markdown documentation from extracted API information.
    
    Args:
        api_info: API information extracted from source code
        output_dir: Directory to save generated documentation
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Markdown documentation in {output_dir}...")
    
    # Generate main API reference
    with open(output_path / "API_REFERENCE.md", 'w', encoding='utf-8') as f:
        f.write("# API Reference\n\n")
        f.write("This document provides a comprehensive reference for all public APIs.\n\n")
        
        # Table of contents
        f.write("## Table of Contents\n\n")
        f.write("- [Modules](#modules)\n")
        f.write("- [Classes](#classes)\n")
        f.write("- [Functions](#functions)\n")
        f.write("- [Constants](#constants)\n\n")
        
        # Modules section
        f.write("## Modules\n\n")
        for module_name, module_info in api_info['modules'].items():
            f.write(f"### `{module_name}`\n\n")
            if module_info['docstring']:
                f.write(f"{module_info['docstring']}\n\n")
            else:
                f.write("*No module documentation available.*\n\n")
            
            if module_info['classes']:
                f.write("**Classes:**\n")
                for class_name in module_info['classes']:
                    f.write(f"- [`{class_name}`](#{module_name.replace('.', '').lower()}{class_name.lower()})\n")
                f.write("\n")
            
            if module_info['functions']:
                f.write("**Functions:**\n")
                for func_name in module_info['functions']:
                    f.write(f"- [`{func_name}()`](#{module_name.replace('.', '').lower()}{func_name.lower()})\n")
                f.write("\n")
        
        # Classes section
        f.write("## Classes\n\n")
        for class_full_name, class_info in api_info['classes'].items():
            f.write(f"### `{class_info['name']}`\n\n")
            f.write(f"**Module:** `{class_info['module']}`  \n")
            f.write(f"**Line:** {class_info['line']}\n\n")
            
            if class_info['docstring']:
                f.write(f"{class_info['docstring']}\n\n")
            else:
                f.write("*No class documentation available.*\n\n")
            
            if class_info['methods']:
                f.write("**Methods:**\n\n")
                for method in class_info['methods']:
                    async_marker = "async " if method['is_async'] else ""
                    f.write(f"#### `{async_marker}{method['name']}()`\n\n")
                    if method['docstring']:
                        f.write(f"{method['docstring']}\n\n")
                    else:
                        f.write("*No method documentation available.*\n\n")
        
        # Functions section
        f.write("## Functions\n\n")
        for func_full_name, func_info in api_info['functions'].items():
            async_marker = "async " if func_info['is_async'] else ""
            f.write(f"### `{async_marker}{func_info['name']}()`\n\n")
            f.write(f"**Module:** `{func_info['module']}`  \n")
            f.write(f"**Line:** {func_info['line']}\n\n")
            
            if func_info['docstring']:
                f.write(f"{func_info['docstring']}\n\n")
            else:
                f.write("*No function documentation available.*\n\n")
        
        # Constants section
        f.write("## Constants\n\n")
        for const_full_name, const_info in api_info['constants'].items():
            f.write(f"### `{const_info['name']}`\n\n")
            f.write(f"**Module:** `{const_info['module']}`  \n")
            f.write(f"**Line:** {const_info['line']}\n\n")
    
    print(f"✅ Generated API_REFERENCE.md")


def generate_readme(template_path: Optional[str] = None, output_path: str = "README.md") -> None:
    """Generate README file from template or create a comprehensive default.
    
    Args:
        template_path: Path to README template (optional)
        output_path: Output path for generated README
    """
    print(f"Generating README file: {output_path}")
    
    if template_path and Path(template_path).exists():
        # Use template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # Generate default comprehensive README
        content = """# Python Project

## Overview

This project contains Python programs with comprehensive documentation and examples.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
# Basic usage example
from src.core import DataProcessor

# Initialize processor
processor = DataProcessor()
processor.initialize()

# Process data
data = [{"name": "John", "age": 30}]
result = processor.process(data)
print(f"Processed {result.records_processed} records")
```

## Documentation

- [API Documentation](docs/API_DOCUMENTATION.md) - Comprehensive API reference
- [Documentation Guide](docs/DOCUMENTATION_GUIDE.md) - Guidelines for writing documentation
- [Examples](examples/) - Code examples and usage demonstrations

## Project Structure

```
project/
├── docs/               # Documentation files
├── examples/           # Example code and usage
├── scripts/            # Utility scripts
├── src/               # Source code
├── tests/             # Test files
└── README.md          # This file
```

## Features

- Comprehensive data processing capabilities
- Extensive documentation with examples
- Type hints and proper error handling
- Configurable processing options
- Support for multiple data formats

## API Reference

### Core Classes

- `DataProcessor` - Main data processing class
- `DataValidator` - Data validation utilities
- `ProcessingResult` - Result container

### Utility Functions

- `load_data()` - Load data from various formats
- `save_data()` - Save data to various formats
- `validate_schema()` - Schema validation

## Examples

### Basic Processing

```python
from src.data_processor import DataProcessor

processor = DataProcessor()
processor.initialize()

data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]

result = processor.process(data, transformations=["clean", "normalize"])
print(f"Success: {result.success}")
```

### File Processing

```python
# Process data from file
result = processor.process_file("input.csv", "output.json")
print(f"Processed {result.records_processed} records")
```

### Advanced Configuration

```python
config = {
    "validation_enabled": True,
    "error_handling": "continue",
    "batch_size": 500
}

processor = DataProcessor(config)
processor.initialize()
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src

# Run doctests
python scripts/generate_docs.py --validate-examples
```

## Documentation Coverage

Check documentation coverage:

```bash
python scripts/generate_docs.py --check-coverage src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

### Documentation Standards

- All public functions must have docstrings
- Include type hints for all parameters
- Provide usage examples
- Follow the Google docstring format

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support, please open an issue on GitHub.
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Generated {output_path}")


def main():
    """Main function for the documentation generation script."""
    parser = argparse.ArgumentParser(description="Generate and validate project documentation")
    parser.add_argument("--source-dir", default="src", help="Source code directory")
    parser.add_argument("--output-dir", default="docs", help="Output directory for generated docs")
    parser.add_argument("--check-coverage", action="store_true", help="Check documentation coverage")
    parser.add_argument("--validate-examples", action="store_true", help="Validate docstring examples")
    parser.add_argument("--generate-api", action="store_true", help="Generate API documentation")
    parser.add_argument("--generate-readme", action="store_true", help="Generate README file")
    parser.add_argument("--all", action="store_true", help="Run all operations")
    
    args = parser.parse_args()
    
    if args.all:
        args.check_coverage = True
        args.validate_examples = True
        args.generate_api = True
        args.generate_readme = True
    
    if not any([args.check_coverage, args.validate_examples, args.generate_api, args.generate_readme]):
        args.check_coverage = True  # Default action
    
    print("🔍 Documentation Tools")
    print("=" * 50)
    
    success = True
    
    if args.check_coverage:
        print("\n📊 Checking Documentation Coverage...")
        stats = check_documentation_coverage(args.source_dir)
        if stats.overall_coverage < 80:
            print(f"⚠️  Warning: Documentation coverage is below 80% ({stats.overall_coverage:.1f}%)")
            success = False
    
    if args.validate_examples:
        print("\n🧪 Validating Docstring Examples...")
        if not validate_docstring_examples(args.source_dir):
            print("❌ Some docstring examples failed validation")
            success = False
        else:
            print("✅ All docstring examples passed validation")
    
    if args.generate_api:
        print("\n📚 Generating API Documentation...")
        api_info = extract_api_info(args.source_dir)
        generate_markdown_docs(api_info, args.output_dir)
    
    if args.generate_readme:
        print("\n📝 Generating README...")
        generate_readme()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All documentation checks passed!")
    else:
        print("❌ Some documentation issues found. Please review and fix.")
        sys.exit(1)


if __name__ == "__main__":
    main()