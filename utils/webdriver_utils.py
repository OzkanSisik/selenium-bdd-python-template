"""
Simple WebDriver utilities for common operations.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class WebDriverUtils:
    """Utility class for common WebDriver operations."""
    
    def __init__(self, driver):
        self.driver = driver
    
    def send_keys_to_element(self, locator, text, timeout=10):
        """
        Send keys to an element after waiting for it to be present.
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)
    
    def click_element(self, locator, timeout=10):
        """
        Click on an element after waiting for it to be clickable.
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    
    def get_element_text(self, locator, timeout=10):
        """
        Get text from an element after waiting for it to be present.
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element.text
    
    def is_element_present(self, locator, timeout=5):
        """
        Check if an element is present on the page.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False 