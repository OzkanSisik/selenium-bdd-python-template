from behave import given, when, then
from Pages.home_page import HomePage
from Pages.category_page import CategoryPage
from Pages.product_detail_page import ProductDetailPage
from Pages.cart_page import CartPage


@given('I have added a product to my cart')
def step_impl(context):
    if not hasattr(context, 'home_page'):
        context.home_page = HomePage(context.driver)
    if not hasattr(context, 'category_page'):
        context.category_page = CategoryPage(context.driver)
    if not hasattr(context, 'product_detail_page'):
        context.product_detail_page = ProductDetailPage(context.driver)
    
    context.home_page.click_category("Phones")
    context.category_page.click_first_product()
    context.product_detail_page.add_to_cart()

@given('I have a product in my cart')
def step_impl(context):
    if not hasattr(context, 'home_page'):
        context.home_page = HomePage(context.driver)
    if not hasattr(context, 'category_page'):
        context.category_page = CategoryPage(context.driver)
    if not hasattr(context, 'product_detail_page'):
        context.product_detail_page = ProductDetailPage(context.driver)
    
    context.home_page.click_category("Phones")
    context.category_page.click_first_product()
    context.product_detail_page.add_to_cart()

@when('I click the "Delete" button for the product')
def step_impl(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    context.cart_page.delete_product_from_cart()

@when('I click the "Place Order" button')
def step_impl(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    context.cart_page.click_place_order()

@then('I should see the shopping cart page')
def step_impl(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_cart_page_visible()

@then('I should see the added product')
def step_impl(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_product_in_cart()

@then('I should see the total price')
def step_impl(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_total_price_visible()

@then('the product should be removed from my cart')
def step_impl(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert not context.cart_page.is_product_in_cart()

@then('I should see an empty cart message')
def step_impl(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_empty_cart_message_visible()

@then('I should see the order form')
def step_impl(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_order_form_visible()

@then('I should see fields for name, country, city, credit card, month, and year')
def step_impl(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert context.cart_page.are_order_form_fields_visible() 