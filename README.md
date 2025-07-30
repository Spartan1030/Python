# Compstat Dashboard - Refactored Version

A enterprise-grade Python data pipeline for querying financial actuals and forecasts from CreditMaster, completely refactored for improved maintainability, security, and performance.

## Overview

This project extracts financial data from Oracle databases and external APIs, processes it through various transformations, and uploads the results to AWS S3. The original monolithic script has been completely refactored into a modular, object-oriented architecture.

## Key Improvements

### 🛡️ Security Enhancements
- **Removed hardcoded passwords** - All credentials now properly retrieved from AWS SSM
- **Secure parameter handling** - Base64 decoding and proper secret management
- **No sensitive data in logs** - Structured logging without credential exposure

### 🏗️ Architecture Improvements
- **Modular design** - Separated concerns into dedicated classes
- **Type safety** - Comprehensive type hints and dataclass usage
- **Resource management** - Context managers for database connections
- **Error handling** - Comprehensive exception handling and logging

### 🚀 Performance & Reliability
- **Modern pandas operations** - Replaced deprecated `DataFrame.append()` with `pd.concat()`
- **Connection management** - Proper database connection lifecycle
- **Memory optimization** - Reduced data copies and improved operations
- **Configurable processing** - Environment-driven configuration

### 🧪 Testability
- **Unit testable** - Isolated components with dependency injection
- **Mock-friendly** - Clean interfaces for testing with mocks
- **Integration tests** - End-to-end pipeline testing capabilities

## Project Structure

```
.
├── compstat_dashboard.py              # Original monolithic script
├── compstat_dashboard_refactored.py   # Refactored modular version
├── test_compstat_dashboard.py         # Comprehensive test suite
├── requirements.txt                   # Python dependencies
├── ANALYSIS_AND_IMPROVEMENTS.md       # Detailed analysis document
└── README.md                          # This file
```

## Classes and Components

### Core Classes

- **`DatabaseConfig`** - Configuration dataclass for database connections
- **`ProcessingConfig`** - Configuration for data processing parameters
- **`DatabaseManager`** - Context manager for Oracle database connections
- **`CredentialManager`** - AWS SSM parameter and S3 operations
- **`DataProcessor`** - Data transformation and cleaning operations
- **`CompstatDashboard`** - Main orchestration class

### Key Features

- **Configuration-driven**: All settings managed through environment variables and dataclasses
- **Secure credentials**: AWS SSM integration with base64 decoding
- **Proper resource management**: Context managers ensure cleanup
- **Comprehensive logging**: Structured logging with configurable levels
- **Type safety**: Full type hints for better IDE support and error detection

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd compstat-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export CC_DB_USER="your_corp_credit_user"
   export CC_DB_HOST="your_corp_credit_host"
   export DM_CORP_DB_USER="your_dm_corp_user"
   export DM_CORP_DB_HOST="your_dm_corp_host"
   export S3_BUCKET_NAME="your_s3_bucket"
   export FDR_LINK="your_fdr_wsdl_url"
   export FDR_URL="your_fdr_api_url"
   export USERNAME="your_fdr_username"
   export LOG_LEVEL="INFO"  # Optional: DEBUG, INFO, WARNING, ERROR
   ```

4. **Configure AWS credentials** (for SSM and S3 access)
   ```bash
   aws configure
   # or use IAM roles if running on EC2/ECS
   ```

## Usage

### Running the Pipeline

```bash
python compstat_dashboard_refactored.py
```

### Configuration Options

The pipeline behavior can be customized through environment variables:

- **`LOG_LEVEL`**: Set logging level (DEBUG, INFO, WARNING, ERROR)
- **`S3_BUCKET_NAME`**: Target S3 bucket for output files
- Database connection parameters (see installation section)

### Processing Configuration

Modify the `ProcessingConfig` in the script to adjust:
- **Date ranges**: `start_year`, `end_year`
- **Currency settings**: `target_currency`, `target_scale`
- **Regions**: `regions` list
- **Template**: `template_name`

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest test_compstat_dashboard.py -v

# Run specific test classes
pytest test_compstat_dashboard.py::TestDataProcessor -v

# Run with coverage
pytest test_compstat_dashboard.py --cov=compstat_dashboard_refactored
```

### Test Coverage

The test suite includes:
- **Unit tests** for all major components
- **Integration tests** for database operations
- **Mock-based testing** for AWS services
- **Data processing validation** tests

## Architecture Details

### Data Flow

1. **Configuration Setup**: Load database configs and processing parameters
2. **Portfolio Extraction**: Query Oracle databases for credit master data
3. **Data Processing**: Apply business logic and FDR nickname transformations
4. **FDR Integration**: Extract financial data from external APIs (when implemented)
5. **Data Merging**: Combine and transform all datasets
6. **Outlier Analysis**: Identify statistical outliers in financial metrics
7. **Final Processing**: Clean ratings, apply business rules
8. **Output**: Save to files and upload to S3

### Security Model

- **No hardcoded secrets**: All sensitive data retrieved from AWS SSM
- **Principle of least privilege**: Each component has minimal required permissions
- **Audit logging**: All operations logged for security monitoring
- **Input validation**: Type checking and parameter validation throughout

### Error Handling Strategy

- **Graceful degradation**: Continue processing when possible
- **Comprehensive logging**: Detailed error information for debugging
- **Resource cleanup**: Proper cleanup even when errors occur
- **Notification system**: Email alerts on critical failures (when configured)

## Performance Considerations

### Optimizations

- **Vectorized operations**: Use pandas efficiently
- **Memory management**: Avoid unnecessary data copies
- **Connection pooling**: Reuse database connections where possible
- **Async processing**: Opportunity for future async improvements

### Monitoring

- **Execution timing**: Logged for performance analysis
- **Resource usage**: Memory and connection monitoring
- **Data quality metrics**: Row counts and validation checks

## Migration from Original Script

### Compatibility

The refactored version maintains compatibility with:
- Same input data sources
- Same output format and structure
- Same business logic and calculations
- Same AWS infrastructure requirements

### Migration Steps

1. **Phase 1**: Deploy alongside existing script for validation
2. **Phase 2**: Run both versions and compare outputs
3. **Phase 3**: Switch to refactored version after validation
4. **Phase 4**: Remove original script after monitoring period

## Contributing

### Development Setup

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run tests before committing:
   ```bash
   pytest test_compstat_dashboard.py
   ```

### Code Style

- **Type hints**: Required for all function signatures
- **Docstrings**: Google-style docstrings for all classes and methods
- **Formatting**: Use Black for code formatting
- **Linting**: Use flake8 and mypy for code quality

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "compstat_dashboard_refactored.py"]
```

### AWS ECS/Fargate

The application is designed for containerized deployment:
- **Environment variables**: All configuration through env vars
- **IAM roles**: Use task roles for AWS permissions
- **Logging**: CloudWatch integration ready
- **Health checks**: Built-in logging for monitoring

## Troubleshooting

### Common Issues

1. **Database Connection Failures**
   - Check network connectivity to Oracle databases
   - Verify credentials in AWS SSM
   - Ensure proper VPC/security group configuration

2. **AWS Permission Issues**
   - Verify IAM roles have SSM and S3 permissions
   - Check parameter names match exactly
   - Ensure KMS permissions for encrypted parameters

3. **Memory Issues**
   - Monitor memory usage for large datasets
   - Consider processing in chunks for very large data
   - Optimize pandas operations

### Debugging

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python compstat_dashboard_refactored.py
```

Check logs in `/tmp/compstat_dashboard.log` for detailed execution information.

## License

[Add your license information here]

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review logs for error details
3. Create an issue in the repository
4. Contact the development team

---

**Note**: This refactored version represents a significant improvement in code quality, security, and maintainability compared to the original script. The modular architecture makes it much easier to maintain, test, and extend the functionality.
