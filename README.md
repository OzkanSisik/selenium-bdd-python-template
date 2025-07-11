# Selenium BDD Framework

A Python test automation framework using Selenium and Behave for BDD testing. Built for the DemoBlaze demo site but easily adaptable for other projects.

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd otoframework
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run tests
behave
```

## What's Included

- **Page Object Model** - Clean separation of test logic and UI interactions
- **Behave BDD** - Write tests in Gherkin syntax
- **Cross-browser support** - Chrome and Safari
- **Environment config** - Easy setup for different environments
- **Selenium Manager** - No manual driver downloads needed

## Configuration

Set environment variables or create a `.env` file:

```bash
BASE_URL=https://www.demoblaze.com
BROWSER=chrome
HEADLESS=false
EXPLICIT_WAIT=20
TEST_USERNAME=ozkanuser
TEST_PASSWORD=ozkanpass
```

## Running Tests

```bash
# All tests
behave

# Specific feature
behave features/demoblaze_authentication.feature

# Headless mode
HEADLESS=true behave
```

## Requirements

- Python 3.9+
- Chrome or Safari browser
- Git 