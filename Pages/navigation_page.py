from Base.base_page import BasePage
from Pages.home_page import HomePage
from Pages.login_page import LoginPage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NavigationPage(BasePage):
    """
    Page Object for Navigation Bar
    """

    NAVIGATION_ITEM = "//*[contains(@class, 'navbar-nav')]//a[contains(text(),'{}')]"

    def __init__(self, driver):
        super().__init__(driver)

    def click_login(self):
        """Clicks login link and returns LoginPage"""
        self.wait_for_element_clickable((By.XPATH, self.NAVIGATION_ITEM.format("Log in"))).click()
        return LoginPage(self.driver)
    
    def click_signup(self):
        """Clicks signup link and returns LoginPage"""
        self.wait_for_element_clickable((By.XPATH, self.NAVIGATION_ITEM.format("Sign up"))).click()
        return LoginPage(self.driver)

    def get_welcome_message_text(self):
        """Gets the welcome message text from the navigation bar"""
        welcome_text = self.wait_for_element_visible((By.XPATH, self.NAVIGATION_ITEM.format("Welcome"))).text
        return welcome_text
