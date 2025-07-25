
from behave import given, when, then
from utils.test_data import test_data


@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username in the login form"""

    actual_username = test_data.get_username(username)
    context.login_page.enter_username(actual_username)
    

@when('I enter password "{password}"')
def step_enter_password(context, password):
    """Enter password in the login form"""

    actual_password = test_data.get_password(password)
    context.login_page.enter_password(actual_password)


@when('I click the "Log in" button')
def step_click_login_button(context):
    """Click the login button to submit the form"""
    context.login_page.click_login_button()
