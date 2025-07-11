# DemoBlaze E-commerce Test Suite

This test suite provides comprehensive automated testing for the [DemoBlaze](https://www.demoblaze.com/) e-commerce website using Selenium WebDriver and Behave (Cucumber for Python).

## 🎯 Overview

DemoBlaze is a demo e-commerce website specifically designed for testing automation. It provides a realistic e-commerce experience with:

- **Product Categories**: Phones, Laptops, Monitors
- **User Authentication**: Sign up, Login, Logout
- **Shopping Cart**: Add/remove products, view cart
- **Checkout Process**: Order placement with form validation
- **Responsive Design**: Works across different browsers

## 📁 Project Structure

```
otoframework/
├── features/
│   ├── demoblaze_navigation.feature      # Basic navigation tests
│   ├── demoblaze_authentication.feature  # User auth tests
│   ├── demoblaze_shopping.feature        # Shopping cart tests
│   └── steps/
│       ├── homepage_steps.py             # Homepage step definitions
│       ├── category_steps.py             # Category navigation steps
│       ├── product_steps.py              # Product interaction steps
│       ├── login_steps.py                # Authentication steps
│       └── cart_steps.py                 # Shopping cart steps
├── Pages/
│   ├── home_page.py                      # Homepage functionality
│   ├── category_page.py                  # Product listing pages
│   ├── product_detail_page.py            # Individual product pages
│   ├── login_page.py                     # Authentication modals
│   └── cart_page.py                      # Shopping cart functionality
├── Base/
│   └── base_page.py                      # Base page class
├── utils/
│   └── webdriver_utils.py                # WebDriver utilities
├── features/
│   └── environment.py                    # Browser setup/teardown
└── run_demoblaze_tests.py                # Test runner script
```

## 🚀 Getting Started

### Prerequisites

1. **Python 3.9+** installed
2. **Chrome Browser** (for Chrome testing)
3. **Safari Browser** (for Safari testing, macOS only)

### Installation

1. **Activate virtual environment**:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Enable Safari WebDriver** (for Safari testing):
   ```bash
   # On macOS, enable the Developer menu in Safari
   # Safari > Preferences > Advanced > Show Develop menu
   # Then enable remote automation:
   # Develop > Allow Remote Automation
   ```

## 🧪 Running Tests

### Quick Start

Run all DemoBlaze tests with Chrome:
```bash
python run_demoblaze_tests.py
```

### Advanced Usage

**Run with specific browser**:
```bash
python run_demoblaze_tests.py --browser chrome
python run_demoblaze_tests.py --browser safari
```

**Run specific feature files**:
```bash
python run_demoblaze_tests.py --features features/demoblaze_navigation.feature
```

**Run with behave directly**:
```bash
# Run all DemoBlaze features
behave features/demoblaze_navigation.feature features/demoblaze_authentication.feature features/demoblaze_shopping.feature

# Run with specific browser
BROWSER=safari behave features/demoblaze_navigation.feature
```

## 📋 Test Scenarios

### 1. Navigation Tests (`demoblaze_navigation.feature`)

- ✅ **Homepage Loading**: Verify all homepage elements load correctly
- ✅ **Category Navigation**: Browse through Phones, Laptops, Monitors
- ✅ **Modal Navigation**: About Us and Contact modals
- ✅ **Responsive Elements**: Carousel, navigation menu, categories

### 2. Authentication Tests (`demoblaze_authentication.feature`)

- ✅ **Sign Up Flow**: Create new user account
- ✅ **Login Flow**: Authenticate existing user
- ✅ **Logout Flow**: Sign out from account
- ✅ **Modal Management**: Open/close auth modals
- ✅ **Form Validation**: Username/password fields

### 3. Shopping Tests (`demoblaze_shopping.feature`)

- ✅ **Product Browsing**: View products in different categories
- ✅ **Product Details**: View individual product information
- ✅ **Add to Cart**: Add products to shopping cart
- ✅ **Cart Management**: View cart, remove items
- ✅ **Checkout Process**: Order form and placement

## 🔧 Page Object Model & Step Definitions

The test suite uses the **Page Object Model (POM)** pattern with separate page classes for different functionalities, and **modular step definitions** for better organization:

### 📝 Step Definitions Structure

#### Homepage Steps (`homepage_steps.py`)
```python
# Homepage navigation and basic functionality
@given('I am on the DemoBlaze homepage')
@when('I click on the "{link_text}" link')
@then('I should see the navigation menu')
@then('I should see the carousel with slides')
```

#### Category Steps (`category_steps.py`)
```python
# Product browsing and category navigation
@when('I click on the "{category}" category')
@when('I click on the first product')
@then('I should see {category} products')
@then('each product should have a name and price')
```

#### Product Steps (`product_steps.py`)
```python
# Product detail page interactions
@when('I click the "{button_text}" button')
@then('I should see the product details page')
@then('I should see an "Add to cart" button')
@then('the product should be added to my cart')
```

#### Login Steps (`login_steps.py`)
```python
# Authentication functionality
@given('I am logged in as "{username}"')
@when('I enter username "{username}"')
@when('I enter password "{password}"')
@then('I should see a welcome message')
```

#### Cart Steps (`cart_steps.py`)
```python
# Shopping cart and checkout
@given('I have a product in my cart')
@when('I click the "Delete" button for the product')
@then('I should see the shopping cart page')
@then('I should see the order form')
```

### Key Benefits of Modular Step Definitions

- **Separation of Concerns**: Each file handles specific functionality
- **Maintainability**: Easy to find and update specific step definitions
- **Direct Page Object Access**: Each step file works directly with its corresponding page object
- **Team Collaboration**: Multiple developers can work on different step files
- **Clear Organization**: Logical grouping of related steps
- **Reduced Conflicts**: Less chance of merge conflicts in version control

### Page Classes

#### HomePage (`home_page.py`)
```python
class HomePage(BasePage):
    # Homepage navigation, carousel, categories
    def navigate_to_homepage(self)
    def click_category(self, category)
    def click_navigation_link(self, link_text)
    def is_header_visible(self, header_text)
```

#### CategoryPage (`category_page.py`)
```python
class CategoryPage(BasePage):
    # Product listing functionality
    def are_products_visible(self, category)
    def click_first_product(self)
    def get_product_names(self)
    def get_product_prices(self)
```

#### ProductDetailPage (`product_detail_page.py`)
```python
class ProductDetailPage(BasePage):
    # Individual product pages
    def add_to_cart(self)
    def get_product_details(self)
    def is_add_to_cart_button_visible(self)
```

#### LoginPage (`login_page.py`)
```python
class LoginPage(BasePage):
    # Authentication functionality
    def login(self, username, password)
    def signup(self, username, password)
    def logout(self)
    def is_welcome_message_visible(self)
```

#### CartPage (`cart_page.py`)
```python
class CartPage(BasePage):
    # Shopping cart functionality
    def is_product_in_cart(self)
    def delete_product_from_cart(self)
    def click_place_order(self)
    def fill_order_form(self, name, country, city, card, month, year)
```

# Note: Each step file works directly with its corresponding page object
# No page manager is needed - this keeps the structure simple and clear

### Key Features

- **Separation of Concerns**: Each page has its own dedicated class
- **Single Responsibility**: Each class handles specific functionality
- **Maintainability**: Easy to update individual page elements
- **Reusability**: Page objects can be used across different test scenarios
- **Page Manager**: Unified interface for step definitions
- **Error Handling**: Graceful handling of missing elements
- **Wait Strategies**: Explicit waits for dynamic content

## 🛠️ Utilities

### WebDriverUtils

Provides common WebDriver operations:

```python
# Click elements with wait
self.utils.click_element(locator, timeout=10)

# Send keys to elements
self.utils.send_keys_to_element(locator, text, timeout=10)

# Check element presence
self.utils.is_element_present(locator, timeout=5)
```

## 🎨 Test Reports

The test runner generates multiple report formats:

- **Console Output**: Pretty-printed test results
- **JSON Reports**: Machine-readable test data
- **Behave Reports**: Standard behave reporting

## 🔍 Debugging

### Common Issues

1. **Element Not Found**: Check if DemoBlaze site structure changed
2. **Timeout Errors**: Increase wait times in WebDriverUtils
3. **Browser Issues**: Verify browser and WebDriver compatibility

### Debug Mode

Run tests with verbose output:
```bash
behave --verbose features/demoblaze_navigation.feature
```

### Screenshot on Failure

The framework automatically captures screenshots on test failures.

## 📊 Test Data

### Sample Credentials

The tests use these sample credentials:
- **Username**: `testuser123`
- **Password**: `testpass123`

⚠️ **Note**: These are test credentials for DemoBlaze only.

## 🌐 Browser Support

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome  | ✅ Full | Recommended browser |
| Safari  | ✅ Full | macOS only, requires safaridriver |

## 🔄 Continuous Integration

The test suite is designed for CI/CD integration:

```yaml
# Example GitHub Actions workflow
- name: Run DemoBlaze Tests
  run: |
    python run_demoblaze_tests.py --browser chrome
```

## 📈 Best Practices

### Page Object Model
1. **Separation of Concerns**: Each page has its own dedicated class
2. **Single Responsibility**: Each class handles specific functionality
3. **Maintainability**: Easy to update individual page elements
4. **Reusability**: Page objects can be used across different test scenarios

### Step Definitions
1. **Modular Organization**: Group related steps in separate files
2. **Context-Specific**: Each step file handles specific functionality
3. **Direct Page Object Access**: Each step file works directly with its page object
4. **Clear Naming**: Descriptive step names that match feature scenarios
5. **Simple Structure**: No complex coordination layer needed

### Test Execution
1. **Explicit Waits**: Use WebDriverWait for dynamic content
2. **Error Handling**: Graceful degradation for missing elements
3. **Test Isolation**: Each test is independent
4. **Descriptive Names**: Clear scenario and step names

## 🤝 Contributing

To add new test scenarios:

1. **Add Feature File**: Create new `.feature` file
2. **Implement Steps**: Add step definitions in `demoblaze_steps.py`
3. **Extend Page Object**: Add methods to `DemoBlazePage` class
4. **Update Runner**: Include new features in test runner

## 📞 Support

For issues or questions:

1. Check the [DemoBlaze website](https://www.demoblaze.com/) for site changes
2. Review Selenium WebDriver documentation
3. Check behave documentation for Cucumber syntax

---

**Happy Testing! 🚀** 