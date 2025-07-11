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

The framework uses environment-specific `.env` files for configuration:

- `.env.production` (default if nothing is set)
- `.env.development`
- `.env.staging`

**How it works:**
- If you do NOT set the `ENVIRONMENT` variable, the project loads `.env.production` and uses production settings.
- If you set `ENVIRONMENT=development` or `ENVIRONMENT=staging`, it loads the corresponding file.

**To override the environment:**
```bash
ENVIRONMENT=development behave
ENVIRONMENT=staging behave
ENVIRONMENT=production behave
```

**Important:**
- The default `BASE_URL` in `.env.development` is a placeholder (`*`). You must set it to a real URL to run tests in development mode.
- Production config points to the live DemoBlaze site by default.

### Environment Defaults:
- **Production (default):** `https://www.demoblaze.com`, headless=true
- **Development:** `*` (placeholder, must be changed), headless=false
- **Staging:** `https://staging.example.com` (example), headless=true

> **Note:** Replace placeholder URLs with your actual application URLs.

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