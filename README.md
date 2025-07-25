# Selenium BDD Framework

A Python-based test automation framework with Selenium, Behave, and AWS S3 integration. Designed for professional CI/CD pipelines. Easily adaptable for any web application testing needs. This is a framework template with basic test examples that demonstrates the structure and setup - you can extend it with your own comprehensive test scenarios.

## What's Included

- **BDD Testing**: Write tests using Gherkin syntax
- **Page Object Model**: Clean separation of test logic and UI interactions
- **Multi-Environment Support**: Development, staging, production environments
- **S3 Integration**: Remote configuration management
- **Jenkins CI/CD**: Docker-based pipeline
- **Security**: Credentials stored in environment variables, not in code

## Setup

### 1. Get Started

```bash
git clone <repo-url>
cd otoframework
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

#### For S3 Environments (Staging/Production)
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
| `staging` | S3 `s3_settings.ini` | Staging testing |
| `production` | S3 `s3_settings.ini` | Production testing |
| `JENKINS` | S3 `s3_settings.ini` | CI/CD pipelines |

## Configuration Files

### Local Development (`settings.ini`)

```ini
[ALL]
browser = chrome
headless = false
timeout = 30

[development]
base_url = https://localhost:3000
```

### S3 Configuration (`s3_settings.ini`)

Upload this file to your S3 bucket:

```ini
[ALL]
browser = chrome
headless = false
timeout = 30

[staging]
base_url = https://staging.example.com
headless = true

[production]
base_url = https://example.com
headless = true

[JENKINS]
base_url = https://staging.example.com
headless = true
```

## S3 Integration

Securely downloads configuration files from AWS S3. Credentials are read only from environment variables.

### Using S3

```python
from settings_manager import settings_manager

# Get all settings
settings = settings_manager.get_settings()

# Get specific setting with default
base_url = settings_manager.get('base_url', 'https://default.example.com')
browser = settings_manager.get('browser', 'chrome')

# Print configuration for debugging
settings_manager.print_config()
```

## Jenkins CI/CD

### Docker Image

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

## Project Structure

```
otoframework/
├── Base/                    # Base page object
├── Pages/                   # Page object models
├── features/                # Behave BDD features
│   ├── steps/              # Step definitions
│   └── environment.py      # Behave environment setup
├── utils/                   # Utility modules
│   ├── s3_utils.py         # S3 integration utilities
│   └── webdriver_utils.py  # WebDriver utilities
├── settings_manager.py      # Configuration management
├── test_s3_integration.py  # S3 integration tests
├── Jenkinsfile             # CI/CD pipeline
├── Dockerfile              # Docker image definition
├── requirements.txt         # Python dependencies
└── settings.ini            # Local development config
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

### Environment-Specific Tests
```bash
# Test local development
ENVIRONMENT=development python -c "from settings_manager import settings_manager; settings_manager.print_config()"

# Test S3 loading
ENVIRONMENT=staging python -c "from settings_manager import settings_manager; settings_manager.print_config()"
```

## Production Deployment

### 1. Build Docker Image
```bash
docker build -t ozkansisik/otoframework-ci:latest .
docker push ozkansisik/otoframework-ci:latest
```

### 2. Configure Jenkins
- Create Jenkins credentials: `aws-s3-credentials`
- Configure S3 bucket and region
- Set up pipeline with GitHub integration

### 3. Upload S3 Settings
```bash
aws s3 cp s3_settings.ini s3://your-bucket-name/s3_settings.ini
```

## Requirements

- Python 3.9+
- Chrome or Safari browser
- AWS CLI (for S3 environments)
- Docker (for CI/CD)
- Jenkins (for CI/CD)

---

**Built for professional test automation** 