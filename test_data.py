"""
Test data mapping system for environment-specific values.
Maps feature variables to actual values based on current environment.
"""

from settings_manager import settings_manager

class TestData:
    """
    Maps feature variables to environment-specific test data.
    """
    
    def __init__(self):
        self.environment = settings_manager.environment
    
    def get_username(self, feature_username):
        """
        Maps feature username to environment-specific username.
        
        Args:
            feature_username (str): Username from feature file (e.g., "testuser")
            
        Returns:
            str: Environment-specific username
        """
        # Map feature usernames to environment-specific usernames
        username_mapping = {
            'testuser': settings_manager.get("test_username"),
            'admin': self.get_test_user_credentials('admin')['username'],
            'guest': self.get_test_user_credentials('guest')['username'],
        }
        
        return username_mapping.get(feature_username, feature_username)
    
    def get_password(self, feature_password):
        """
        Maps feature password to environment-specific password.
        
        Args:
            feature_password (str): Password from feature file (e.g., "testpass")
            
        Returns:
            str: Environment-specific password
        """
        # Map feature passwords to environment-specific passwords
        password_mapping = {
            'testpass': settings_manager.get("test_password"),
            'admin': self.get_test_user_credentials('admin')['password'],
            'guest': self.get_test_user_credentials('guest')['password'],
        }
        
        return password_mapping.get(feature_password, feature_password)
    
    def get_url(self, feature_url):
        """
        Maps feature URL to environment-specific URL.
        
        Args:
            feature_url (str): URL from feature file (e.g., "homepage")
            
        Returns:
            str: Environment-specific URL
        """
        # Map feature URLs to environment-specific URLs
        base_url = settings_manager.get("base_url", "https://www.demoblaze.com")
        url_mapping = {
            'homepage': base_url,
            'login': f"{base_url}/login"
        }
        
        return url_mapping.get(feature_url, feature_url)
    
    def get_test_user_credentials(self, user_type: str = 'default') -> dict:
        """Get test user credentials based on type"""
        import os
        credentials = {
            'default': {
                'username': settings_manager.get("test_username"),
                'password': settings_manager.get("test_password")
            },
            'admin': {
                'username': os.getenv('ADMIN_USERNAME'),
                'password': os.getenv('ADMIN_PASSWORD')
            }
        }
        return credentials.get(user_type, credentials['default'])

# Global test data instance
test_data = TestData() 