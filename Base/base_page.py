from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    ElementNotVisibleException, ElementNotSelectableException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver.remote.webelement import WebElement
import logging
from functools import wraps
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from utils.webdriver_utils import WebDriverUtils
import time


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        #self.utils = WebDriverUtils(driver)
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to(self, url):
        """
        Navigate to a specific URL.
        """
        self.driver.get(url)

    def get_page_title(self):
        """
        Get the current page title.
        """
        return self.driver.title

    def get_element(self, locator):
        """
        Get element for a provided locator
        :param locator: locator of the element to find
        :return: Element Object
        :rtype: WrapWebElement

        """
        try:
            element = self.driver.find_element(*locator)
        except (NoSuchElementException, StaleElementReferenceException):
            raise Exception("There is no such element or its" + str(locator) + " has changed ")
        return WrapWebElement(self.driver, element, locator)

    @staticmethod
    def wait_until(function, params=None, equals=None, not_equals=None, timeout=None, interval=None, list_check=None):
        """
        Checked to wait until the specified timeout time of the specified function.
        :param function: Function name to wait
        :param params: Function name to parameters
        :param equals: Wait until match value with equals parameter
        :param not_equals: Wait until match value with not equals parameter
        :param timeout: Time to wait
        :param interval: Interval seconds to retry
        :param list_check: Use true if you are waiting list
        :return: Function value, if is timeout finish returns False
        """
        end = time.time() + timeout

        while time.time() < end:
            if isinstance(params, tuple):
                val = function(*params)
            elif isinstance(params, list):
                val = function(*tuple(params))
            elif isinstance(params, dict):
                val = function(**params)
            else:
                val = function()

            if list_check is not None and len(val) >= equals:
                return val
            elif equals is not None and val == equals:
                return val
            elif not_equals is not None and val != not_equals:
                return val
            else:
                time.sleep(interval)
        return False

    def get_element_list(self, locator, list_length=1):
        """
        Get elements list for a provided locator
        :param locator:  of the element list to find
        :param int list_length: Expected count of list
        :return: List of web elements or empty list
        :rtype: list

        """
        elements = BasePage.wait_until(self.driver.find_elements, params=locator, equals=list_length, timeout=10,
                                       interval=0.5, list_check=True)
        if elements is False:
            return []
        return list(map(lambda el: WrapWebElement(self.driver, el, locator=locator), elements))

    def wait_for_element(self, locator, wait_type=ec.presence_of_element_located, timeout=20):
        """
        Wait for element to present
        :param wait_type: which condition of the element you are waiting for
        :param locator: locator of the element to find
        :param int timeout: Maximum time you want to wait for the element
        :rtype: WrapWebElement

        """
        start_time = int(round(time.time() * 1000))
        element = None
        try:
            logging.info("Waiting for maximum :: " + str(timeout) +
                         " :: seconds for element to be visible and clickable")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1.5,
                                 ignored_exceptions=[NoSuchElementException, ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(wait_type(locator))
            end_time = int(round(time.time() * 1000))
            duration = (end_time - start_time) / 1000.00
            logging.info("Element '"
                         "' appeared on the web pages after :: " + "{0:.2f}".format(duration) + " :: seconds")
        except ElementNotVisibleException:
            logging.error("Element '"
                          "' not appeared on the web pages after :: " + str(timeout) + " :: seconds")
        if isinstance(element, WebElement):
            return WrapWebElement(self.driver, element, locator)
        else:
            return element

    def wait_for_element_clickable(self, locator, timeout=20):
        """
        Wait for element to be clickable
        :param locator: locator of the element to find
        :param int timeout: Maximum time you want to wait for the element
        :rtype: WrapWebElement

        """
        return self.wait_for_element(locator, ec.element_to_be_clickable, timeout)

    def wait_for_element_visible(self, locator, timeout=20):
        """
        Wait for element to be visible
        :param locator: locator of the element to find
        :param int timeout: Maximum time you want to wait for the element
        :rtype: WrapWebElement

        """
        return self.wait_for_element(locator, ec.visibility_of_element_located, timeout)

    def is_element_visible(self, locator, timeout=30):
        """
        Return True if element visible and False if element not visible
        :param locator: locator of the element to find
        :param int timeout: Desired waiting amount, default is 30 seconds

        """
        try:
            self.wait_for_element_visible(locator, timeout=timeout)
        except (NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException,
                ElementClickInterceptedException, TimeoutException):
            return False
        return True


class WrapWebElement(WebElement):
    """
    This class defines the generic interceptor for the methods of wrapped web element references.It also provides
    implementations for methods that acquire web element references

    """
    element = None
    driver = None
    locator = None

    def __init__(self, driver, element, locator=None):
        super().__init__(element.parent, element._id)
        self.element = element
        self.driver = driver
        self.locator = locator

    def send_keys(self, value, delay=0):
        """
        Sends keys to current focused element.
        :param str value: A string for typing
        :param float delay: Requested wait time between typing each character
        :rtype: WrapWebElement

        """
        if delay:
            for char in list(value):
                self.element.send_keys(char)
                time.sleep(delay)
        else:
            self.element.send_keys(value)
        return self

    def find_element(self, *locator):
        """
        Find an element given a By strategy and locator.
        :param locator: locator of the element to find
        :rtype: WrapWebElement

        """
        if isinstance(locator[0], tuple):
            element = self.element.find_element(*locator[0])
            used_locator = locator[0]
        else:
            element = self.element.find_element(*locator)
            used_locator = locator
        return WrapWebElement(self.driver, element, locator=used_locator)

    def clear(self):
        self.element.clear()
        return self  # zincirleme için

    def find_elements(self, *locator):
        """
        Find elements given locator.
        :param locator: locator of the elements to find
        :rtype: list of elements

        """
        if isinstance(locator[0], tuple):
            elements = self.element.find_elements(*locator[0])
            used_locator = locator[0]
        else:
            elements = self.element.find_elements(*locator)
            used_locator = locator
        return list(map(lambda el: WrapWebElement(self.driver, el, locator=used_locator), elements))

    def wait_visible(self, timeout=20):
        """
        Wait for element to be visible
        :param int timeout: Desired wait time before visibility of element
        :return: Desired visible element
        :rtype: WrapWebElement

        """
        wait = WebDriverWait(self.driver, timeout, poll_frequency=1.5)
        wait.until(lambda _: self.element.is_displayed(), "{} element not visible".format(str(self.locator)))
        return self

    def wait_clickable(self, timeout=20):
        """
        Wait for element to be clickable
        :param int timeout: Desired wait time before visibility of element
        :return: Desired visible element
        :rtype: WrapWebElement

        """
        self.wait_visible(timeout=timeout)
        return self

    def click(self, delay=0):
        """
        Clicks the web element.
        :param float delay: Wait seconds before click
        :return: Desired visible element
        :rtype: WrapWebElement

        """
        if delay:
            time.sleep(delay)
        self.element.click()
        return self

    def js_click(self):
        """
        Clicks given element with execute script

        """
        self.driver.execute_script("arguments[0].click();", self.element)
        return self







