from Base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CartPage(BasePage):
    """
    Page Object for DemoBlaze Shopping Cart
    """
    
    # Cart table locators
    CART_TABLE = (By.CLASS_NAME, "table")
    CART_ITEMS = (By.XPATH, "//tbody/tr")
    CART_ITEM_NAME = (By.XPATH, ".//td[2]")
    CART_ITEM_PRICE = (By.XPATH, ".//td[3]")
    
    # Action buttons
    DELETE_BUTTON = (By.XPATH, "//a[contains(text(),'Delete')]")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(),'Place Order')]")
    
    # Cart summary
    TOTAL_PRICE = (By.ID, "totalp")
    
    # Order form locators
    ORDER_NAME_FIELD = (By.ID, "name")
    ORDER_COUNTRY_FIELD = (By.ID, "country")
    ORDER_CITY_FIELD = (By.ID, "city")
    ORDER_CARD_FIELD = (By.ID, "card")
    ORDER_MONTH_FIELD = (By.ID, "month")
    ORDER_YEAR_FIELD = (By.ID, "year")
    PURCHASE_BUTTON = (By.XPATH, "//button[contains(text(),'Purchase')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(),'Cancel')]")
    
    # Navigation
    CART_LINK = (By.XPATH, "//a[contains(text(),'Cart')]")
    
    def __init__(self, driver):
        super().__init__(driver)

