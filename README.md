# BDD Selenium Test Automation Framework

A robust, scalable test automation framework built with Python, Selenium, and Behave for Behavior-Driven Development (BDD) testing.

## 🚀 Features

- **BDD Testing**: Uses Behave for Behavior-Driven Development
- **Page Object Model**: Clean separation of test logic and page interactions
- **Cross-browser Support**: Chrome and Safari support
- **Environment-driven Configuration**: Flexible configuration via environment variables
- **Modern Selenium**: Uses Selenium Manager for automatic driver management
- **Explicit Waits**: Reliable test execution with explicit wait strategies
- **Comprehensive Logging**: Structured logging for debugging and reporting
- **CI/CD Ready**: Designed for continuous integration and deployment

## 📋 Prerequisites

- Python 3.9+
- Chrome or Safari browser
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd otoframework
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

The framework uses environment variables for configuration. You can set these in your environment or create a `.env` file:

```bash
# Environment settings
BASE_URL=https://www.demoblaze.com
BROWSER=chrome
HEADLESS=false

# Timeout settings
EXPLICIT_WAIT=20
PAGE_LOAD_TIMEOUT=30

# Window settings
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080

# Test data
TEST_USERNAME=ozkanuser
TEST_PASSWORD=ozkanpass

# Screenshot settings
SCREENSHOT_ON_FAILURE=true
SCREENSHOT_DIR=screenshots

# Logging
LOG_LEVEL=INFO
LOG_FILE=test_execution.log
```

## 🧪 Running Tests

### Run all tests
```bash
behave
```

### Run specific feature
```bash
behave features/demoblaze_authentication.feature
```

### Run specific scenario
```bash
behave features/demoblaze_authentication.feature:9
```

### Run with verbose output
```bash
behave --no-capture
```

### Run in headless mode
```bash
HEADLESS=true behave
```

## 📁 Project Structure

```
otoframework/
├── Base/
│   └── base_page.py          # Base page object with common functionality
├── Pages/
│   ├── home_page.py          # Homepage page object
│   ├── login_page.py         # Login page object
│   ├── navigation_page.py    # Navigation page object
│   ├── cart_page.py          # Cart page object
│   ├── category_page.py      # Category page object
│   └── product_detail_page.py # Product detail page object
├── features/
│   ├── environment.py        # Behave environment setup
│   ├── steps/
│   │   ├── homepage_steps.py # Homepage step definitions
│   │   ├── login_steps.py    # Login step definitions
│   │   ├── navigation_steps.py # Navigation step definitions
│   │   ├── cart_steps.py     # Cart step definitions
│   │   ├── category_steps.py # Category step definitions
│   │   └── product_steps.py  # Product step definitions
│   ├── demoblaze_authentication.feature
│   ├── demoblaze_navigation.feature
│   └── demoblaze_shopping.feature
├── utils/
│   └── webdriver_utils.py    # WebDriver utility functions
├── config.py                 # Centralized configuration management
├── requirements.txt          # Python dependencies
├── behave.ini               # Behave configuration
└── README.md               # Project documentation
```

## 🏗️ Architecture

### Page Object Model (POM)
- **BasePage**: Common functionality for all page objects
- **Page Objects**: Encapsulate page-specific elements and actions
- **Step Definitions**: BDD steps that use page objects

### Configuration Management
- **Environment-driven**: All settings configurable via environment variables
- **Centralized**: Single configuration class for all settings
- **Type-safe**: Proper type hints and validation

### Browser Management
- **Selenium Manager**: Automatic driver management
- **Cross-browser**: Support for Chrome and Safari
- **Optimized**: Chrome flags for CI/CD compatibility

## 🧪 Test Examples

### Authentication Test
```gherkin
Feature: DemoBlaze User Authentication
  As a user
  I want to log in to DemoBlaze
  So that I can access personalized features

  Background:
    Given I am on the DemoBlaze homepage

  Scenario: Login with valid credentials
    When I click on the "Log in" link
    And I enter username "ozkanuser"
    And I enter password "ozkanpass"
    And I click the "Log in" button
    Then I should see "Welcome ozkanuser" message
```

## 🔧 Development

### Adding New Page Objects
1. Create a new page class in `Pages/` directory
2. Inherit from `BasePage`
3. Define locators and methods
4. Create corresponding step definitions

### Adding New Features
1. Create feature file in `features/` directory
2. Write Gherkin scenarios
3. Implement step definitions in `features/steps/`
4. Use page objects for element interactions

### Configuration
- Modify `config.py` for new configuration options
- Use environment variables for environment-specific settings
- Update `environment.py` for new browser support

## 🚀 CI/CD Integration

### GitHub Actions Example
```yaml
name: Test Automation
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: HEADLESS=true behave
```

## 📊 Best Practices

- **Explicit Waits**: Use explicit waits instead of implicit waits
- **Page Objects**: Keep page objects focused and reusable
- **Environment Variables**: Use environment variables for configuration
- **Logging**: Implement proper logging for debugging
- **Error Handling**: Handle exceptions gracefully
- **Clean Code**: Follow Python coding standards

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions or issues, please create an issue in the repository. 