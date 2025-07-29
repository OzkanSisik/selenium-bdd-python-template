from Base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    """
    Page Object for Login Page
    """
    LOGIN_USERNAME_FIELD = (By.ID, "loginusername")
    LOGIN_PASSWORD_FIELD = (By.ID, "loginpassword")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_username(self, username):
        """Enters username in authentication form"""
        self.wait_for_element_visible(self.LOGIN_USERNAME_FIELD).clear().send_keys(username)
    
    def enter_password(self, password):
        """Enters password in authentication form"""
        self.wait_for_element_visible(self.LOGIN_PASSWORD_FIELD).clear().send_keys(password)
    
    def click_login_button(self):
        """Clicks the login button"""
        self.wait_for_element_clickable(self.LOGIN_BUTTON).click()

    def login(self, username, password):
        """Completes login process"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
