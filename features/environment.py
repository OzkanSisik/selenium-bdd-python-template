"""
Behave environment configuration for browser setup and teardown.
This file handles the lifecycle of the WebDriver instance for behave tests.
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from utils.settings_manager import settings_manager
from selenium.webdriver.chrome.service import Service as ChromeService
import shutil
import tempfile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



def before_scenario(context, scenario):
    """
    Sets up browser before each scenario.
    This runs before every test scenario in behave.
    """
    browser = settings_manager.get("browser", "chrome")
    logger.info(f"Setting up {browser} browser for scenario: {scenario.name}")
    
    
    try:
        if browser == "chrome":
            options = ChromeOptions()
            headless = settings_manager.get("headless", False)
            window_width = settings_manager.get("window_width", 1920)
            window_height = settings_manager.get("window_height", 1080)
            
            browser_options = {
                '--no-sandbox': True,
                '--disable-dev-shm-usage': True,
                '--disable-gpu': True,
                '--window-size': f'{window_width},{window_height}',
                '--disable-extensions': True,
                '--disable-plugins': True
            }
            
            if headless:
                browser_options['--headless'] = True
            
            for option, value in browser_options.items():
                if value is True:
                    options.add_argument(option)
                else:
                    options.add_argument(f"{option}={value}")
            
            user_data_dir = tempfile.mkdtemp()
            logger.info(f"Using user data dir: {user_data_dir}")
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument('--enable-logging')
            options.add_argument('--v=1')
            context._chrome_user_data_dir = user_data_dir
            service = ChromeService(
                executable_path='/usr/local/bin/chromedriver',
                log_path='chromedriver.log'
            )
            service.log_level = "ALL"
            context.driver = webdriver.Chrome(service=service, options=options)
            logger.info("Chrome browser initialized successfully with custom ChromeDriver")
            
        elif browser == "safari":
            context.driver = webdriver.Safari()
            logger.info("Safari browser initialized successfully")
            
        else:
            raise ValueError(f"Unsupported browser: {browser}")   
        
        logger.info("Browser setup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize browser: {str(e)}")
        raise


def after_scenario(context, scenario):
    """
    Cleans up browser after each scenario.
    This runs after every test scenario in behave.
    """
    if hasattr(context, 'driver'):
        try:
            context.driver.quit()
            logger.info(f"Browser closed successfully after scenario: {scenario.name}")
        except Exception as e:
            logger.warning(f"Error closing browser: {str(e)}")
    # Clear user data directory
    if hasattr(context, '_chrome_user_data_dir'):
        try:
            shutil.rmtree(context._chrome_user_data_dir)
        except Exception as e:
            logger.warning(f"User data directory silinemedi: {e}")
    