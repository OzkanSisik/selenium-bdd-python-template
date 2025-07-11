"""
Behave environment configuration for browser setup and teardown.
This file handles the lifecycle of the WebDriver instance for behave tests.
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def before_scenario(context, scenario):
    """
    Set up browser before each scenario.
    This runs before every test scenario in behave.
    """
    logger.info(f"Setting up {config.browser} browser for scenario: {scenario.name}")
    
    
    try:
        if config.browser == "chrome":
            options = ChromeOptions()
            browser_options = config.get_browser_options()
            
            for option, value in browser_options.items():
                if value is True:
                    options.add_argument(option)
                else:
                    options.add_argument(f"{option}={value}")
            
            context.driver = webdriver.Chrome(options=options)
            logger.info("Chrome browser initialized successfully with Selenium Manager")
            
        elif config.browser == "safari":
            context.driver = webdriver.Safari()
            logger.info("Safari browser initialized successfully")
            
        else:
            raise ValueError(f"Unsupported browser: {config.browser}")   
        
        context.driver.set_page_load_timeout(config.page_load_timeout)
        
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