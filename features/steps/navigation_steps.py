from behave import given, when, then
from utils.test_data import test_data

from Pages.navigation_page import NavigationPage


@when('I click on the "Log in" link')
def step_click_login_link(context):
    """ Click Login button on navigation bar"""
    context.navigation = NavigationPage(context.driver)
    context.login_page = context.navigation.click_login()


@when('I click on the "Sign up" link')
def step_click_signup_link(context):
    """
    Clicks Signup button on navigation bar
    """
    context.navigation = NavigationPage(context.driver)
    context.login_page = context.navigation.click_signup()


@then('I should see "Welcome {username}" message')
def step_check_welcome_message_with_username(context, username):
    """Verify that the welcome message matches the expected text"""
    mapped_username = test_data.get_username(username)
    expected_message = f"Welcome {mapped_username}" 
    welcome_text = context.navigation.get_welcome_message_text()
    assert expected_message == welcome_text, f"Expected '{expected_message}' but found '{welcome_text}'"
    


