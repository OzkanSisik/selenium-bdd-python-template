from Base.base_page import BasePage
from Pages.login_page import LoginPage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import config


class HomePage(BasePage):
    """
    Page Object for Homepage
    """
    
    # URL
    BASE_URL = "https://www.demoblaze.com/"
    
    # Locators
    HEADER = (By.CLASS_NAME, "navbar-brand")
    NAVIGATION_MENU = (By.CLASS_NAME, "navbar-nav")
    CAROUSEL = (By.ID, "carouselExampleIndicators")
    CATEGORIES_SECTION = (By.CLASS_NAME, "list-group")
    
    # Category links
    PHONES_CATEGORY = (By.XPATH, "//a[contains(text(),'Phones')]")
    LAPTOPS_CATEGORY = (By.XPATH, "//a[contains(text(),'Laptops')]")
    MONITORS_CATEGORY = (By.XPATH, "//a[contains(text(),'Monitors')]")
    
    # Modal locators
    MODAL_DIALOG = (By.CLASS_NAME, "modal-dialog")
    MODAL_CLOSE_BUTTON = (By.CLASS_NAME, "close")
    
    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_homepage(self):
        """Navigate to DemoBlaze homepage"""
        self.driver.get(config.base_url)
        self.wait_for_page_load()
        return HomePage(self.driver)

    def wait_for_page_load(self):
        """Wait for the page to fully load"""
        self.wait.until(EC.presence_of_element_located(self.HEADER))
    
    def click_category(self, category):
        """Click on a specific category"""
        category_map = {
            "Phones": self.PHONES_CATEGORY,
            "Laptops": self.LAPTOPS_CATEGORY,
            "Monitors": self.MONITORS_CATEGORY
        }
        
        if category in category_map:
            self.utils.click_element(category_map[category])
            time.sleep(2)  # Wait for products to load
    
    def is_company_info_visible(self):
        """Check if company information is visible in About Us modal"""
        try:
            # Look for company info text in modal
            modal_text = self.driver.find_element(*self.MODAL_DIALOG).text
            return "performance" in modal_text.lower() or "software" in modal_text.lower()
        except:
            return False
    
    def is_on_homepage(self):
        """Check if currently on homepage"""
        return self.driver.current_url == self.BASE_URL
