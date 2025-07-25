from Base.base_page import BasePage
from Pages.login_page import LoginPage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.settings_manager import settings_manager


class HomePage(BasePage):
    """
    Page Object for Homepage
    """
    
    HEADER = (By.CLASS_NAME, "navbar-brand")


    def __init__(self, driver):
        super().__init__(driver)
        self.BASE_URL = settings_manager.get("base_url")

    def navigate_to_homepage(self):
        """Navigate to DemoBlaze homepage"""
        self.driver.get(self.BASE_URL)
        self.wait_for_page_load()
        return HomePage(self.driver)

    def wait_for_page_load(self):
        """Waits for the page to fully load"""
        self.wait.until(EC.presence_of_element_located(self.HEADER))
    
    
    def is_on_homepage(self):
        """Check if currently on homepage"""
        return self.driver.current_url == self.BASE_URL
