from Base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CategoryPage(BasePage):
    """
    Page Object for DemoBlaze Category/Product Listing Pages
    """
    
    # Product locators
    PRODUCT_CARDS = (By.CLASS_NAME, "card")
    PRODUCT_NAME = (By.CLASS_NAME, "card-title")
    PRODUCT_PRICE = (By.CLASS_NAME, "card-text")
    PRODUCT_IMAGE = (By.CLASS_NAME, "card-img-top")
    
    # Category header
    CATEGORY_HEADER = (By.CLASS_NAME, "page-header")
    
    # Navigation back to categories
    CATEGORIES_SECTION = (By.CLASS_NAME, "list-group")
    
    def __init__(self, driver):
        super().__init__(driver)
