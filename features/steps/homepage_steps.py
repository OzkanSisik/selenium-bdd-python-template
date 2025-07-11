from behave import given, when, then
from Pages.home_page import HomePage


@given('I am on the DemoBlaze homepage')
def step_am_on_demoblaze_homepage(context):
    """Navigate to DemoBlaze homepage"""
    context.home_page = HomePage(context.driver)
    context.home_page.navigate_to_homepage()






