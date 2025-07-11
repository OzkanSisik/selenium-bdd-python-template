
from behave import given, when, then


@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username in the login form"""
    context.login_page.enter_username(username)
    

@when('I enter password "{password}"')
def step_enter_password(context, password):
    """Enter password in the login form"""
    context.login_page.enter_password(password)


@when('I click the "Log in" button')
def step_click_login_button(context):
    """Click the login button to submit the form"""
    context.login_page.click_login_button()


@then('I should see the "Log out" link')
def step_should_see_logout_link(context):
    """Verify that the logout link is visible after successful login"""
    assert context.login_page.is_logout_link_visible(), "Logout link not visible after login"


@then('the login modal should close')
def step_login_modal_should_close(context):
    """Verify that the login modal is no longer visible"""
    # Wait a moment for modal to close
    assert not context.login_page.is_modal_visible("login"), "Login modal is still visible"
