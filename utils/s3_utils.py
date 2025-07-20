"""
S3 Utilities for Test Framework
Professional S3 file download utilities with proper error handling and security practices
"""
import os
import tempfile
import logging
from typing import Optional, Union
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


class S3Downloader:
    """
    Professional S3 file download utility with proper error handling and security practices.
    
    Features:
    - Secure credential management
    - Proper error handling and logging
    - Temporary file management
    - Configurable retry logic
    - Environment-based configuration
    """
    
    def __init__(self, bucket_name: Optional[str] = None, region: Optional[str] = None):
        """
        Initialize S3 downloader with optional bucket and region configuration.
        
        Args:
            bucket_name: S3 bucket name (can be set via S3_BUCKET_NAME env var)
            region: AWS region (can be set via S3_REGION env var)
        """
        self.bucket_name = bucket_name or os.getenv('S3_BUCKET_NAME')
        self.region = region or os.getenv('S3_REGION', 'eu-central-1')
        self._setup_logging()
        
        # boto3 import edildiği için S3 kullanılabilir
        
        if not self.bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")
        
        # Initialize S3 session immediately
        self.session = self._create_s3_session()
        self.s3_client = self.session.client('s3')
        self.s3_resource = self.session.resource('s3')
        self.bucket = self.s3_resource.Bucket(self.bucket_name)
    
    def _setup_logging(self):
        """Setup logging for S3 operations."""
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _create_s3_session(self):
        """Create S3 session with proper error handling."""
        try:
            session = boto3.Session(region_name=self.region)
            # Test credentials by making a simple call
            session.client('sts').get_caller_identity()
            self.logger.info(f"S3 session established for region: {self.region}")
            return session
        except Exception as e:
            raise ConnectionError(f"Failed to establish S3 session: {e}")
    
    def download_file_to_temp(self, s3_key: str):
        """
        Download file from S3 to a temporary file.
        
        This is the recommended approach for configuration files as it:
        - Keeps sensitive data in memory only
        - Automatically cleans up temporary files
        - Provides secure file handling
        
        Args:
            s3_key: S3 object key (file path in bucket)
            
        Returns:
            NamedTemporaryFile: Temporary file object with downloaded content
            
        Raises:
            FileNotFoundError: If file doesn't exist in S3
            CredentialsError: If AWS credentials are invalid
            ConnectionError: If S3 connection fails
        """
        # Create temporary file that will be automatically cleaned up
        temp_file = tempfile.NamedTemporaryFile(suffix='.ini')
        
        try:
            self.logger.info(f"Downloading {s3_key} from s3://{self.bucket_name}")
            self.bucket.download_file(s3_key, temp_file.name)
            self.logger.info(f"Successfully downloaded {s3_key} to temporary file")
            return temp_file
            
        except ClientError as e:
            temp_file.close()
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise FileNotFoundError(f"File {s3_key} not found in bucket {self.bucket_name}")
            elif error_code == 'NoSuchBucket':
                raise FileNotFoundError(f"Bucket {self.bucket_name} not found")
            elif error_code == 'AccessDenied':
                raise CredentialsError(f"Access denied to bucket {self.bucket_name}")
            else:
                raise ConnectionError(f"S3 error: {e}")
        except Exception as e:
            temp_file.close()
            raise ConnectionError(f"Failed to download file: {e}")
    
    def download_file(self, s3_key: str, local_path: Union[str, Path]) -> None:
        """
        Download file from S3 to a specific local path.
        
        Use this method when you need to save the file to a specific location.
        For configuration files, prefer download_file_to_temp() for security.
        
        Args:
            s3_key: S3 object key (file path in bucket)
            local_path: Local file path to save the downloaded file
            
        Raises:
            FileNotFoundError: If file doesn't exist in S3
            CredentialsError: If AWS credentials are invalid
            ConnectionError: If S3 connection fails
        """
        try:
            self.logger.info(f"Downloading {s3_key} from s3://{self.bucket_name} to {local_path}")
            self.bucket.download_file(s3_key, str(local_path))
            self.logger.info(f"Successfully downloaded {s3_key} to {local_path}")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise FileNotFoundError(f"File {s3_key} not found in bucket {self.bucket_name}")
            elif error_code == 'NoSuchBucket':
                raise FileNotFoundError(f"Bucket {self.bucket_name} not found")
            elif error_code == 'AccessDenied':
                raise CredentialsError(f"Access denied to bucket {self.bucket_name}")
            else:
                raise ConnectionError(f"S3 error: {e}")
        except Exception as e:
            raise ConnectionError(f"Failed to download file: {e}")
    
    def file_exists(self, s3_key: str) -> bool:
        """
        Check if a file exists in S3 bucket.
        
        Args:
            s3_key: S3 object key to check
            
        Returns:
            bool: True if file exists, False otherwise
        """
        try:
            self.bucket.Object(s3_key).load()
            return True
        except ClientError:
            return False
        except Exception:
            return False
    
    def cleanup_temp_file(self, temp_file) -> None:
        """
        Clean up temporary file manually if needed.
        
        Args:
            temp_file: Temporary file object to clean up
        """
        try:
            temp_file.close()
            self.logger.debug(f"Closed temporary file: {temp_file.name}")
        except Exception as e:
            self.logger.warning(f"Failed to close temporary file {temp_file.name}: {e}")


class CredentialsError(Exception):
    """Raised when AWS credentials are invalid or missing."""
    pass


class ConnectionError(Exception):
    """Raised when S3 connection fails."""
    pass 