#!/usr/bin/env python3
"""
Test suite for the refactored Compstat Dashboard
Demonstrates how the new architecture enables comprehensive testing
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass

# Import the classes from the refactored script
from compstat_dashboard_refactored import (
    DatabaseConfig,
    ProcessingConfig,
    DatabaseManager,
    CredentialManager,
    DataProcessor,
    CompstatDashboard
)


class TestDatabaseConfig:
    """Test DatabaseConfig dataclass."""
    
    def test_database_config_creation(self):
        """Test that DatabaseConfig can be created with required fields."""
        config = DatabaseConfig(
            user="test_user",
            password="test_password",
            host="test_host"
        )
        
        assert config.user == "test_user"
        assert config.password == "test_password"
        assert config.host == "test_host"


class TestProcessingConfig:
    """Test ProcessingConfig dataclass."""
    
    def test_processing_config_defaults(self):
        """Test that ProcessingConfig sets appropriate defaults."""
        config = ProcessingConfig(start_year=2020, end_year=2025)
        
        assert config.start_year == 2020
        assert config.end_year == 2025
        assert config.target_currency == "USD"
        assert config.target_scale == 1000000
        assert config.template_name == "GLOBAL CORPORATES"
        assert config.regions == ['LATAM', 'APAC', 'EMEA', 'NorthAmerica']
    
    def test_processing_config_custom_regions(self):
        """Test ProcessingConfig with custom regions."""
        custom_regions = ['REGION1', 'REGION2']
        config = ProcessingConfig(
            start_year=2020,
            end_year=2025,
            regions=custom_regions
        )
        
        assert config.regions == custom_regions


class TestCredentialManager:
    """Test CredentialManager class."""
    
    @patch('boto3.Session')
    def test_credential_manager_initialization(self, mock_session):
        """Test CredentialManager initialization."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_ssm = Mock()
        mock_session_instance.client.return_value = mock_ssm
        
        cred_manager = CredentialManager()
        
        mock_session.assert_called_once_with(region_name='us-east-1')
        assert cred_manager.ssm == mock_ssm
    
    @patch('boto3.Session')
    def test_get_parameter_success(self, mock_session):
        """Test successful parameter retrieval."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_ssm = Mock()
        mock_session_instance.client.return_value = mock_ssm
        
        # Mock successful response
        mock_ssm.get_parameter.return_value = {
            'Parameter': {'Value': 'test_value'}
        }
        
        cred_manager = CredentialManager()
        result = cred_manager.get_parameter('test_param')
        
        assert result == 'test_value'
        mock_ssm.get_parameter.assert_called_once_with(
            Name='test_param', WithDecryption=True
        )
    
    @patch('boto3.Session')
    @patch('base64.b64decode')
    def test_get_decoded_parameter(self, mock_b64decode, mock_session):
        """Test base64 parameter decoding."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_ssm = Mock()
        mock_session_instance.client.return_value = mock_ssm
        
        # Mock parameter retrieval and decoding
        mock_ssm.get_parameter.return_value = {
            'Parameter': {'Value': 'encoded_value'}
        }
        mock_b64decode.return_value = b'decoded_value'
        
        cred_manager = CredentialManager()
        result = cred_manager.get_decoded_parameter('test_param')
        
        assert result == 'decoded_value'
        mock_b64decode.assert_called_once_with('encoded_value')


class TestDataProcessor:
    """Test DataProcessor class methods."""
    
    def test_identify_outliers_basic(self):
        """Test basic outlier identification."""
        # Create test data with clear outliers
        data = {
            'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]  # 100 is clear outlier
        }
        df = pd.DataFrame(data)
        
        result = DataProcessor.identify_outliers(df, 'value', 'outlier_flag')
        
        # Check that outlier column was added
        assert 'outlier_flag' in result.columns
        
        # Check that the extreme value is marked as an outlier
        extreme_row = result[result['value'] == 100]
        assert not extreme_row.empty
        assert '95th percentile' in extreme_row['outlier_flag'].iloc[0]
        
        # Check that middle values are not outliers
        middle_rows = result[result['value'].isin([4, 5, 6])]
        assert all(middle_rows['outlier_flag'] == 'Not an Outlier')
    
    def test_identify_outliers_empty_dataframe(self):
        """Test outlier identification with empty DataFrame."""
        df = pd.DataFrame({'value': []})
        
        # Should handle empty DataFrame gracefully
        result = DataProcessor.identify_outliers(df, 'value', 'outlier_flag')
        
        assert 'outlier_flag' in result.columns
        assert len(result) == 0
    
    def test_clean_rating_data(self):
        """Test rating data cleaning."""
        # Create test data with various rating scenarios
        data = {
            'LT_FC_IDR': ['AAA', 'BB+', 'NR', 'A-(Stable)', 'WD'],
            'LT_LC_IDR': ['AA', 'B', 'NR', 'BBB+(Positive)', 'WD'],
            'analistReviewed': [True, False, True, False, True],
            'pblshFlg': [True, True, False, False, True]
        }
        df = pd.DataFrame(data)
        
        result = DataProcessor.clean_rating_data(df)
        
        # Check rating cleaning
        assert result['LT_FC_IDR'].iloc[0] == 'AAA'  # Should remain unchanged
        assert result['LT_FC_IDR'].iloc[2] == 'NA'   # NR should become NA
        assert result['LT_FC_IDR'].iloc[3] == 'A-'   # Should remove (Stable)
        assert result['LT_FC_IDR'].iloc[4] == 'NA'   # WD should become NA
        
        # Check grade assignment
        assert result['GRADE'].iloc[0] == 'Investment Grade'  # AAA
        assert result['GRADE'].iloc[1] == 'Speculative Grade'  # BB+
        
        # Check boolean flag conversion
        assert result['analistReviewed'].iloc[0] == 'Reviewed'
        assert result['analistReviewed'].iloc[1] == 'Not Reviewed'
        assert result['pblshFlg'].iloc[0] == 'Published'
        assert result['pblshFlg'].iloc[2] == 'Not Published'
    
    def test_process_credit_master_data(self):
        """Test credit master data processing."""
        # Create simplified test data
        data = {
            'AGNT_ID': ['1', '2', '3'],
            'NCKNM': ['Company A', 'Company B', 'Company C'],
            'CFIN_PRNT_NCKNM': ['Company A', 'Company A', 'Company D'],
            'ULT_AGNT_ID': ['10', '20', '30'],
            'ULT_AGNT_NM': ['Ultimate A', 'Ultimate B', 'Ultimate C']
        }
        df = pd.DataFrame(data)
        
        result = DataProcessor.process_credit_master_data(df)
        
        # Check that AGNT_ID was converted to float
        assert result['AGNT_ID'].dtype == 'float64'
        
        # Check that unnecessary columns were dropped
        assert 'ULT_AGNT_ID' not in result.columns
        assert 'ULT_AGNT_NM' not in result.columns
        
        # Check that FDR_NCKNM column was added
        assert 'FDR_NCKNM' in result.columns
        
        # Check that non-null FDR_NCKNM values exist
        assert result['FDR_NCKNM'].notna().any()


class TestCompstatDashboard:
    """Test CompstatDashboard main class."""
    
    @patch('compstat_dashboard_refactored.CredentialManager')
    @patch('compstat_dashboard_refactored.DataProcessor')
    def test_dashboard_initialization(self, mock_data_processor, mock_cred_manager):
        """Test CompstatDashboard initialization."""
        dashboard = CompstatDashboard()
        
        # Check that components were initialized
        assert dashboard.credential_manager is not None
        assert dashboard.data_processor is not None
        assert hasattr(dashboard, 'logger')
    
    @patch('os.environ.get')
    @patch('compstat_dashboard_refactored.CredentialManager')
    def test_get_database_configs(self, mock_cred_manager, mock_env_get):
        """Test database configuration retrieval."""
        # Mock environment variables
        mock_env_get.side_effect = lambda key: {
            'CC_DB_USER': 'cc_user',
            'CC_DB_HOST': 'cc_host',
            'DM_CORP_DB_USER': 'dm_user',
            'DM_CORP_DB_HOST': 'dm_host'
        }.get(key)
        
        # Mock credential manager
        mock_cred_instance = Mock()
        mock_cred_manager.return_value = mock_cred_instance
        mock_cred_instance.get_decoded_parameter.side_effect = lambda param: {
            'oracloud-corpcredit-db-password': 'cc_password',
            'oracloud-dmcorp-db-password': 'dm_password'
        }.get(param)
        
        dashboard = CompstatDashboard()
        configs = dashboard.get_database_configs()
        
        # Check that configs were created correctly
        assert 'corpcredit' in configs
        assert 'dmcorp' in configs
        
        cc_config = configs['corpcredit']
        assert cc_config.user == 'cc_user'
        assert cc_config.password == 'cc_password'
        assert cc_config.host == 'cc_host'
        
        dm_config = configs['dmcorp']
        assert dm_config.user == 'dm_user'
        assert dm_config.password == 'dm_password'
        assert dm_config.host == 'dm_host'


class TestDatabaseManager:
    """Test DatabaseManager context manager."""
    
    @patch('cx_Oracle.connect')
    def test_database_manager_context(self, mock_connect):
        """Test DatabaseManager context manager behavior."""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        config = DatabaseConfig(
            user="test_user",
            password="test_password", 
            host="test_host"
        )
        
        # Test context manager
        with DatabaseManager(config) as db_manager:
            assert db_manager._connection == mock_connection
            mock_connect.assert_called_once_with(
                "test_user", "test_password", "test_host"
            )
        
        # Check that connection was closed
        mock_connection.close.assert_called_once()
    
    @patch('cx_Oracle.connect')
    @patch('pandas.read_sql')
    def test_execute_query(self, mock_read_sql, mock_connect):
        """Test query execution."""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        mock_read_sql.return_value = mock_df
        
        config = DatabaseConfig(
            user="test_user",
            password="test_password",
            host="test_host"
        )
        
        with DatabaseManager(config) as db_manager:
            result = db_manager.execute_query("SELECT * FROM test_table")
            
            mock_read_sql.assert_called_once_with("SELECT * FROM test_table", mock_connection)
            pd.testing.assert_frame_equal(result, mock_df)


# Integration test example
class TestIntegration:
    """Integration tests for the complete pipeline."""
    
    @patch('compstat_dashboard_refactored.DatabaseManager')
    @patch('compstat_dashboard_refactored.CredentialManager')
    @patch('os.environ.get')
    def test_extract_portfolio_data_integration(self, mock_env_get, mock_cred_manager, mock_db_manager):
        """Test portfolio data extraction with mocked dependencies."""
        # Mock environment variables
        mock_env_get.side_effect = lambda key: f"mock_{key.lower()}"
        
        # Mock credential manager
        mock_cred_instance = Mock()
        mock_cred_manager.return_value = mock_cred_instance
        mock_cred_instance.get_decoded_parameter.return_value = "mock_password"
        
        # Mock database results
        mock_credit_df = pd.DataFrame({
            'AGNT_ID': ['1', '2'],
            'NCKNM': ['Company A', 'Company B'],
            'CFIN_PRNT_NCKNM': ['Company A', 'Company A']
        })
        
        mock_dm_df = pd.DataFrame({
            'AGNT_ID': [1.0, 2.0],
            'ULT_AGNT_ID': [10, 20],
            'ULT_AGNT_NM': ['Ultimate A', 'Ultimate B']
        })
        
        # Mock database manager context
        mock_db_instance = Mock()
        mock_db_manager.return_value.__enter__.return_value = mock_db_instance
        mock_db_instance.execute_query.side_effect = [mock_credit_df, mock_dm_df]
        
        dashboard = CompstatDashboard()
        
        # Mock the database configs method to avoid actual AWS calls
        mock_configs = {
            'corpcredit': DatabaseConfig('user', 'pass', 'host'),
            'dmcorp': DatabaseConfig('user', 'pass', 'host')
        }
        
        with patch.object(dashboard, 'get_database_configs', return_value=mock_configs):
            result = dashboard.extract_portfolio_data(mock_configs)
        
        # Verify the result has expected structure
        assert isinstance(result, pd.DataFrame)
        assert 'FDR_NCKNM' in result.columns
        assert len(result) > 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])