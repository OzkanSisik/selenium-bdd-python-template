import os
from typing import Optional

class TestConfig:
    """
    Centralized configuration management for test automation framework.
    Handles environment variables, default values, and configuration settings.
    """
    
    def __init__(self):
        # Environment settings
        self.base_url = os.getenv('BASE_URL', 'https://www.demoblaze.com')
        self.browser = os.getenv('BROWSER', 'chrome').lower()
        self.headless = os.getenv('HEADLESS', 'false').lower() == 'true'
        
        # Timeout settings
        self.explicit_wait = int(os.getenv('EXPLICIT_WAIT', '20'))
        self.page_load_timeout = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
        
        # Window settings
        self.window_width = int(os.getenv('WINDOW_WIDTH', '1920'))
        self.window_height = int(os.getenv('WINDOW_HEIGHT', '1080'))
        
        # Test data
        self.test_username = os.getenv('TEST_USERNAME', 'ozkanuser')
        self.test_password = os.getenv('TEST_PASSWORD', 'ozkanpass')
        
        # Screenshot settings
        self.screenshot_on_failure = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
        self.screenshot_dir = os.getenv('SCREENSHOT_DIR', 'screenshots')
        
        # Logging
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'test_execution.log')
    
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
    

# Global configuration instance
config = TestConfig() 