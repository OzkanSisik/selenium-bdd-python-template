"""
Environment loader utility for loading .env files based on environment.
"""

import os
from pathlib import Path

def load_env_file(environment=None):
    """
    Loads environment variables from .env file based on environment.
    
    Args:
        environment (str): Environment name (development, staging, production)
                          If None, tries to detect from ENVIRONMENT variable
    """
    if environment is None:
        environment = os.getenv('ENVIRONMENT', 'production')  # Default to production
    
    env_file = f'.env.{environment}'
    
    if Path(env_file).exists():
        print(f"Loading environment from {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    else:
        print(f"Environment file {env_file} not found, using system environment variables")

# Auto-load environment file when module is imported
if __name__ != "__main__":
    load_env_file() 