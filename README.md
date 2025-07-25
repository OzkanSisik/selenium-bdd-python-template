# Selenium BDD Framework

A Python-based test automation framework with Selenium, Behave, and AWS S3 integration. Designed for professional CI/CD pipelines. Easily adaptable for any web application testing needs. This is a framework template with basic test examples that demonstrates the structure and setup - you can extend it with your own comprehensive test scenarios.

## Project Structure

```
selenium-bdd-framework/
├── Base/                    # Base page object
├── Pages/                   # Page object models
├── features/                # Behave BDD features
│   ├── steps/              # Step definitions
│   └── environment.py      # Behave environment setup
├── utils/                   # Framework utilities
│   ├── s3_utils.py         # S3 integration utilities
│   ├── settings_manager.py # Configuration management
│   └── test_data.py        # Test data mapping
├── test_s3_integration.py  # S3 integration tests
├── Jenkinsfile             # CI/CD pipeline
├── Dockerfile              # Docker image definition
├── requirements.txt         # Python dependencies
└── settings.ini            # Local development config
```

## What's Included

- **BDD Testing**: Write tests using Gherkin syntax
- **Page Object Model**: Clean separation of test logic and UI interactions
- **Multi-Environment Support**: Development and staging environments
- **S3 Integration**: Remote configuration management
- **Jenkins CI/CD**: Docker-based pipeline
- **Security**: Credentials stored in environment variables, not in code

## Setup

### 1. Get Started

```bash
git clone <repo-url>
cd selenium-bdd-framework
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

#### For Local Development
```bash
# Uses local settings.ini file
ENVIRONMENT=development
```

#### For S3 Environments (Staging/CI)
```bash
# Configure AWS credentials
aws configure

# Set environment variables
export S3_BUCKET_NAME=your-bucket-name
export S3_REGION=eu-central-1
export ENVIRONMENT=staging
```

### 3. Run Tests

```bash
# All tests
behave

# Specific feature
behave features/demoblaze_authentication.feature

# With specific environment
ENVIRONMENT=staging behave
```

## How It Works

The framework automatically detects the environment and loads the appropriate configuration:

| Environment | Source | Use Case |
|-------------|--------|----------|
| `development` | Local `settings.ini` | Local development |
| `staging` | S3 `s3_settings.ini` | Staging testing and CI/CD |

## Configuration Files

### Local Development (`settings.ini`)

```ini
[ALL]
browser = chrome
headless = false
timeout = 30

[development]
base_url = https://your-application-url.com
```

### S3 Configuration (`s3_settings.ini`)

Upload this file to your S3 bucket:

```ini
[ALL]
browser = chrome
headless = false
timeout = 30

[staging]
base_url = https://your-staging-url.com
headless = true
```

## Running Tests

### All Tests
```bash
behave
```

### S3 Integration Test
```bash
python test_s3_integration.py
```

## Requirements

- Python 3.9+
- Chrome or Safari browser
- AWS CLI (for S3 environments)
- Docker (for CI/CD)
- Jenkins (for CI/CD)

---
