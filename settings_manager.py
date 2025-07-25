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
    DEVELOPMENT = "development"
    STAGING = "staging"


class SettingsManager:
    """Centralized settings management with support for:
    - Local INI files (development)
    - Remote configurations (staging)
    - Environment variable overrides
     """
    def __init__(self):
        self._settings = None
        self.environment = self._detect_environment()
        self.project_dir = self._get_project_dir()
        
    def _detect_environment(self) -> str:
        """Detect current environment from ENVIRONMENT variable or CI/CD indicators.
        
        Returns:
            str: Environment name ('development', 'staging')
        """
        # Check for explicit environment variable
        env = os.getenv('ENVIRONMENT')
        if env:
            return env.lower()
        
        # Check for CI/CD environment variables
        if os.getenv('CI') or os.getenv('JENKINS_URL') or os.getenv('GITHUB_ACTIONS'):
            return Environments.STAGING
        
        return Environments.DEVELOPMENT
    
    def _get_project_dir(self) -> str:
        """Get project directory path for locating settings.ini.
        
        Returns:
            str: Absolute path to project directory
        """
        return os.path.dirname(os.path.abspath(__file__))
    
    def _read_settings_from_config(self, config, env_section):
        """Read [ALL] and environment-specific sections from configparser object."""
        settings = {}
        for section in ['ALL', env_section]:
            if config.has_section(section):
                for key, value in config.items(section):
                    settings[key] = self._parse_value(value)
        return settings
    
    def _load_local_settings(self) -> Dict[str, Any]:
        """Load settings from local settings.ini file.
        
        Loads [ALL] and environment-specific sections, converting values to proper types.
        
        Returns:
            Dict[str, Any]: Settings dictionary with proper types
        """
        ini_file = os.path.join(self.project_dir, "settings.ini")
        
        if not os.path.exists(ini_file):
            print(f"Warning: settings.ini not found at {ini_file}")
            return {}
        
        config = configparser.ConfigParser()
        config.read(ini_file, encoding='utf-8')
        
        return self._read_settings_from_config(config, self.environment)
    
    def _load_remote_settings(self) -> Dict[str, Any]:
        """Load settings from remote source (AWS S3)."""
        # Artık local_settings ile credential toplamaya gerek yok, S3Downloader env'den okuyor
        if not os.getenv('S3_BUCKET_NAME'):
            print("❌ S3_BUCKET_NAME not found in environment")
            return {}
        if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
            print("❌ AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
            return {}
        s3_downloader = S3Downloader()
        temp_file = s3_downloader.download_file_to_temp('s3_settings.ini')
        try:
            config = configparser.ConfigParser()
            config.read(temp_file.name, encoding='utf-8')
            settings = self._read_settings_from_config(config, self.environment)
            print(f"✅ Loaded settings from S3 for environment: {self.environment}")
            return settings
        finally:
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
            if self.environment in [Environments.DEVELOPMENT, Environments.STAGING]:
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