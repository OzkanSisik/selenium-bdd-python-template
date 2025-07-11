from Base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class ProductDetailPage(BasePage):
    """
    Page Object for DemoBlaze Product Detail Pages
    """
    
    # Product detail locators
    PRODUCT_NAME = (By.CLASS_NAME, "name")
    PRODUCT_PRICE = (By.CLASS_NAME, "price-container")
    PRODUCT_DESCRIPTION = (By.CLASS_NAME, "description")
    PRODUCT_IMAGE = (By.CLASS_NAME, "product-image")
    
    # Action buttons
    ADD_TO_CART_BUTTON = (By.XPATH, "//a[contains(text(),'Add to cart')]")
    BACK_TO_PRODUCTS_BUTTON = (By.XPATH, "//a[contains(text(),'Add to cart')]/following-sibling::a")
    
    # Product specifications
    PRODUCT_SPECS = (By.CLASS_NAME, "product-specs")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)
    
