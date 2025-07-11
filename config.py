import os
from typing import Optional

# Load environment file if available
try:
    from env_loader import load_env_file
    load_env_file()
except ImportError:
    pass  # env_loader not available, use system environment variables

class TestConfig:
    """
    Centralized configuration management for test automation framework.
    Supports multiple environments: development, staging, production
    """
    
    def __init__(self):
        # Environment detection
        self.environment = os.getenv('ENVIRONMENT', 'production').lower()
        
        # Environment-specific settings
        self._load_environment_config()
        
        # Common settings (same across environments)
        self.browser = os.getenv('BROWSER', 'chrome').lower()
        self.explicit_wait = int(os.getenv('EXPLICIT_WAIT', '20'))
        self.page_load_timeout = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
        self.window_width = int(os.getenv('WINDOW_WIDTH', '1920'))
        self.window_height = int(os.getenv('WINDOW_HEIGHT', '1080'))
        self.screenshot_on_failure = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
        self.screenshot_dir = os.getenv('SCREENSHOT_DIR', 'screenshots')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'test_execution.log')
    
    def _load_environment_config(self):
        """Load environment-specific configuration"""
        if self.environment == 'development':
            self.base_url = os.getenv('BASE_URL', 'http://localhost:3000')
            self.headless = os.getenv('HEADLESS', 'false').lower() == 'true'
            self.test_username = os.getenv('TEST_USERNAME', 'dev_user')
            self.test_password = os.getenv('TEST_PASSWORD', 'dev_pass')
            
        elif self.environment == 'staging':
            self.base_url = os.getenv('BASE_URL', 'https://staging.example.com')
            self.headless = os.getenv('HEADLESS', 'true').lower() == 'true'
            self.test_username = os.getenv('TEST_USERNAME', 'staging_user')
            self.test_password = os.getenv('TEST_PASSWORD', 'staging_pass')
            
        elif self.environment == 'production':
            self.base_url = os.getenv('BASE_URL', 'https://www.demoblaze.com')
            self.headless = os.getenv('HEADLESS', 'true').lower() == 'true'
            self.test_username = os.getenv('TEST_USERNAME', 'prod_user')
            self.test_password = os.getenv('TEST_PASSWORD', 'prod_pass')
            
        else:
            raise ValueError(f"Unsupported environment: {self.environment}")
    
    def get_browser_options(self) -> dict:
        """Get browser-specific options based on configuration"""
        options = {
            'chrome': {
                '--no-sandbox': True,
                '--disable-dev-shm-usage': True,
                '--disable-gpu': True,
                '--window-size': f'{self.window_width},{self.window_height}',
                '--disable-extensions': True,
                '--disable-plugins': True
            }
        }
        
        if self.headless:
            options['chrome']['--headless'] = True
            
        return options.get(self.browser, {})
    
    def get_test_user_credentials(self, user_type: str = 'default') -> dict:
        """Get test user credentials based on type"""
        credentials = {
            'default': {
                'username': self.test_username,
                'password': self.test_password
            },
            'admin': {
                'username': os.getenv('ADMIN_USERNAME', 'admin'),
                'password': os.getenv('ADMIN_PASSWORD', 'adminpass')
            },
            'guest': {
                'username': os.getenv('GUEST_USERNAME', 'guest'),
                'password': os.getenv('GUEST_PASSWORD', 'guestpass')
            }
        }
        return credentials.get(user_type, credentials['default'])
    
    def print_config(self):
        """Print current configuration for debugging"""
        print("=== Test Configuration ===")
        print(f"Environment: {self.environment}")
        print(f"Base URL: {self.base_url}")
        print(f"Browser: {self.browser}")
        print(f"Headless: {self.headless}")
        print(f"Explicit Wait: {self.explicit_wait}s")
        print(f"Window Size: {self.window_width}x{self.window_height}")
        print(f"Test Username: {self.test_username}")
        print("==========================")

# Global configuration instance
config = TestConfig() 