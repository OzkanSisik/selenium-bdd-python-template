from behave import given, when, then

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


@then('I should see "{expected_message}" message')
def step_check_welcome_message_with_username(context, expected_message):
    """Verify that the welcome message matches the expected text"""
    welcome_text = context.navigation.get_welcome_message_text()
    assert expected_message == welcome_text, f"Expected '{expected_message}' but found '{welcome_text}'"



