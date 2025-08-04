"""
Behave environment configuration for browser setup and teardown.
This file handles the lifecycle of the WebDriver instance for behave tests.
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from utils.settings_manager import settings_manager, Environments
from utils.screenshot_utils import ScreenshotUtils
from selenium.webdriver.chrome.service import Service as ChromeService
import shutil
import tempfile
import os
import traceback

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
            
            user_data_dir = tempfile.mkdtemp(dir="/var/tmp")
            options.add_argument(f'--user-data-dir={user_data_dir}')
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument(f'--window-size={window_width},{window_height}')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            context._chrome_user_data_dir = user_data_dir
            
            # Use Selenium Manager for development, fixed ChromeDriver for staging/AWS
            if settings_manager.environment == Environments.DEVELOPMENT:
                # Use Selenium Manager (default behavior)
                context.driver = webdriver.Chrome(options=options)
                logger.info("Chrome browser initialized successfully with Selenium Manager")
            else:
                # Use fixed ChromeDriver for AWS/staging environments
                service = ChromeService(
                    executable_path='/usr/local/bin/chromedriver',
                    log_path='chromedriver.log'
                )
                context.driver = webdriver.Chrome(service=service, options=options)
                logger.info("Chrome browser initialized successfully with custom ChromeDriver")
            
        elif browser == "safari":
            context.driver = webdriver.Safari()
            logger.info("Safari browser initialized successfully")
            
        else:
            raise ValueError(f"Unsupported browser: {browser}")   
        
        # Initialize screenshot utilities
        context.screenshot_utils = ScreenshotUtils(context.driver)
        logger.info("Screenshot utilities initialized")
        
        logger.info("Browser setup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize browser: {str(e)}")
        raise


def after_scenario(context, scenario):
    """
    Cleans up browser after each scenario and captures screenshot on failure.
    This runs after every test scenario in behave.
    """
    # Capture screenshot if scenario failed
    if scenario.status == "failed":
        logger.error(f"Scenario failed: {scenario.name}")
        
        try:
            # Capture screenshot
            if hasattr(context, 'screenshot_utils'):
                screenshot_path = context.screenshot_utils.capture_screenshot_on_failure(
                    scenario.name, "scenario_failure"
                )
                if screenshot_path:
                    logger.info(f"Screenshot captured: {screenshot_path}")
                    print(f"\n📸 Screenshot saved: {screenshot_path}")
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")
            # Fallback: try to capture screenshot without utility
            try:
                if hasattr(context, 'driver'):
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"failure_{scenario.name}_{timestamp}.png"
                    filepath = os.path.join("screenshots", filename)
                    os.makedirs("screenshots", exist_ok=True)
                    context.driver.save_screenshot(filepath)
                    logger.info(f"Fallback screenshot saved: {filepath}")
                    print(f"\n📸 Fallback screenshot: {filepath}")
            except Exception as fallback_error:
                logger.error(f"Fallback screenshot also failed: {str(fallback_error)}")
    
    # Clean up browser
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