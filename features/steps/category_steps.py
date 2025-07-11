from behave import when, then
from Pages.home_page import HomePage
from Pages.category_page import CategoryPage

@when('I click on the "{category}" category')
def step_impl(context, category):
    if not hasattr(context, 'home_page'):
        context.home_page = HomePage(context.driver)
    context.home_page.click_category(category)

@when('I click on the first product')
def step_impl(context):
    if not hasattr(context, 'category_page'):
        context.category_page = CategoryPage(context.driver)
    context.category_page.click_first_product()

@then('I should see {category} products')
def step_impl(context, category):
    if not hasattr(context, 'category_page'):
        context.category_page = CategoryPage(context.driver)
    assert context.category_page.are_products_visible(category)

@then('each product should have a name and price')
def step_impl(context):
    if not hasattr(context, 'category_page'):
        context.category_page = CategoryPage(context.driver)
    assert context.category_page.do_products_have_name_and_price() 