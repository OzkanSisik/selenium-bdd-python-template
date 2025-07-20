"""
Settings Manager for Test Automation Framework
Supports both local INI files and remote configurations (AWS/CI)
"""
import configparser
import os
from pathlib import Path
from typing import Dict, Any, Optional
from utils.s3_utils import S3Downloader


class Environments:
    """Environment constants"""
    LOCAL = "LOCAL"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    JENKINS = "JENKINS"
    CI = "CI"


class SettingsManager:
    """Centralized settings management with support for:
    - Local INI files (development)
    - Remote configurations (staging/production)
    - Environment variable overrides
     """
    def __init__(self):
        self._settings = None
        self.environment = self._detect_environment()
        self.project_dir = self._get_project_dir()
        
    def _detect_environment(self) -> str:
        """Detect current environment from ENVIRONMENT variable or CI/CD indicators.
        
        Returns:
            str: Environment name ('development', 'staging', 'production', 'JENKINS')
        """
        # Check for explicit environment variable
        env = os.getenv('ENVIRONMENT')
        if env:
            return env.lower()
        
        # Check for CI/CD environment variables
        if os.getenv('CI') or os.getenv('JENKINS_URL') or os.getenv('GITHUB_ACTIONS'):
            return Environments.JENKINS
        
        return Environments.DEVELOPMENT
    
    def _get_project_dir(self) -> str:
        """Get project directory path for locating settings.ini.
        
        Returns:
            str: Absolute path to project directory
        """
        return os.path.dirname(os.path.abspath(__file__))
    
    def _load_local_settings(self) -> Dict[str, Any]:
        """Load settings from local settings.ini file.
        
        Loads [ALL] and environment-specific sections, converting values to proper types.
        
        Returns:
            Dict[str, Any]: Settings dictionary with proper types
        """
        settings = {}
        
        ini_file = os.path.join(self.project_dir, "settings.ini")
        
        if not os.path.exists(ini_file):
            print(f"Warning: settings.ini not found at {ini_file}")
            return settings
        
        config = configparser.ConfigParser()
        config.read(ini_file, encoding='utf-8')
        
        if config.has_section('ALL'):
            for key, value in config.items('ALL'):
                settings[key] = self._parse_value(value)
        
        env_section = self.environment
        if config.has_section(env_section):
            for key, value in config.items(env_section):
                settings[key] = self._parse_value(value)
        
        return settings
    
    def _load_remote_settings(self) -> Dict[str, Any]:
        """Load settings from remote source (AWS S3).
        
        Downloads settings.ini from S3 and loads it using the same parsing logic
        as local settings.
        
        Returns:
            Dict[str, Any]: Settings dictionary loaded from S3
        """
        # First load local settings to get AWS credentials
        local_settings = self._load_local_settings()
        
        # Get AWS credentials from local settings or environment
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID') or local_settings.get('aws_access_key_id')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY') or local_settings.get('aws_secret_access_key')
        bucket_name = os.getenv('S3_BUCKET_NAME') or local_settings.get('s3_bucket_name')
        region = os.getenv('S3_REGION') or local_settings.get('s3_region', 'eu-central-1')
        
        if not bucket_name:
            print("❌ S3_BUCKET_NAME not found in environment or settings.ini")
            return {}
        
        if not aws_access_key or not aws_secret_key:
            print("❌ AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
            return {}
        
        # Set environment variables for S3Downloader
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key
        os.environ['S3_BUCKET_NAME'] = bucket_name
        os.environ['S3_REGION'] = region
        
        # Initialize S3 downloader
        s3_downloader = S3Downloader()
        
        # Download settings file to temporary file
        temp_file = s3_downloader.download_file_to_temp('s3_settings.ini')
        
        try:
            # Load settings from temporary file
            config = configparser.ConfigParser()
            config.read(temp_file.name, encoding='utf-8')
            
            settings = {}
            
            # Load [ALL] section
            if config.has_section('ALL'):
                for key, value in config.items('ALL'):
                    settings[key] = self._parse_value(value)
            
            # Load environment-specific section
            env_section = self.environment
            if config.has_section(env_section):
                for key, value in config.items(env_section):
                    settings[key] = self._parse_value(value)
            
            print(f"✅ Loaded settings from S3 for environment: {self.environment}")
            return settings
            
        finally:
            # Clean up temporary file
            s3_downloader.cleanup_temp_file(temp_file)
            
    def _parse_value(self, value: str):
        """Parse string value to appropriate type (bool, int, str, None).
        
        Args:
            value (str): String value from settings.ini
            
        Returns:
            Any: Parsed value with proper type
        """
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.lower() == 'none':
            return None
        elif value.isdigit():
            return int(value)
        else:
            return value
    
    def _apply_environment_overrides(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to settings.
        
        Args:
            settings (Dict[str, Any]): Current settings dictionary
            
        Returns:
            Dict[str, Any]: Settings with environment variable overrides
        """
        for key, value in os.environ.items():
            if key.upper() in [k.upper() for k in settings.keys()]:
                original_key = next(k for k in settings.keys() if k.upper() == key.upper())
                settings[original_key] = self._parse_value(value)
        
        return settings
    
    def get_settings(self) -> Dict[str, Any]:
        """Get all settings for current environment with caching.
        
        Returns:
            Dict[str, Any]: Complete settings dictionary
        """
        if self._settings is None:
            if self.environment in [Environments.LOCAL, Environments.DEVELOPMENT]:
                # Load from local INI file
                self._settings = self._load_local_settings()
            else:
                # Load from remote source (staging, production, CI)
                self._settings = self._load_remote_settings()
            
            # Apply environment variable overrides
            self._settings = self._apply_environment_overrides(self._settings)
        
        return self._settings
    
    def get(self, key: str, default: Any = None):
        """Get specific setting value with optional default.
        
        Args:
            key (str): Setting key to retrieve
            default (Any): Default value if key not found
            
        Returns:
            Any: Setting value or default
        """
        settings = self.get_settings()
        return settings.get(key, default)
    
    def print_config(self):
        """Print configuration for debugging"""
        settings = self.get_settings()
        print("=== Settings Configuration ===")
        print(f"Environment: {self.environment}")
        print(f"Project Directory: {self.project_dir}")
        print("Settings:")
        for key, value in settings.items():
            print(f"  {key}: {value}")
        print("=======================")


# Global settings instance
settings_manager = SettingsManager() 