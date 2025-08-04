# Selenium BDD Framework

A Python-based test automation framework with Selenium, Behave, and AWS S3 integration. Designed for professional CI/CD pipelines with Docker containerization. Easily adaptable for any web application testing needs. This is a framework template with basic test examples that demonstrates the structure and setup - you can extend it with your own comprehensive test scenarios.

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
├── requirements.txt        # Python dependencies
├── settings.ini            # Local development config
└── s3_settings_template.ini # S3 config template for staging/CI
```

## What's Included

- **BDD Testing**: Write tests using Gherkin syntax
- **Page Object Model**: Clean separation of test logic and UI interactions
- **Multi-Environment Support**: Development and staging environments
- **S3 Integration**: Remote configuration management
- **Jenkins CI/CD**: Docker-based pipeline with AWS EC2
- **Docker Containerization**: Isolated test environment
- **Smart Driver Management**: Automatic driver detection for development, fixed driver for CI/CD
- **Screenshot Support**: Automatic screenshots on test failures
- **Security**: Credentials stored in environment variables, not in code

## Key Features

### 🐳 **Docker Containerization**
- Isolated test environment with Chrome and ChromeDriver pre-installed
- Consistent execution across different environments
- Resource management and cleanup

### 🔧 **Smart Driver Management**
- **Development Environment**: Automatic ChromeDriver detection and download
- **CI/CD Environment**: Fixed ChromeDriver version from S3 for stability
- Environment-aware configuration

### 📸 **Screenshot Support**
- **Automatic Capture**: Screenshots captured on test failures
- **Organized Storage**: Saved with descriptive names and timestamps

### ☁️ **AWS Integration**
- S3-based configuration management
- EC2-hosted Jenkins with Docker
- Secure credential management

## Setup

### Get Started

```bash
git clone <repo-url>
cd selenium-bdd-framework
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```



## Docker Setup

### Building the Docker Image

**Important**: For AWS deployment, build the image on Linux or use multi-platform build to ensure compatibility.

```bash
# Standard build
docker build -t selenium-bdd-framework .

# Multi-platform build (recommended for AWS)
docker buildx build --platform linux/amd64 -t selenium-bdd-framework .
```

### Docker Image Features
- **Chrome Browser**: Pre-installed Google Chrome
- **ChromeDriver**: Fixed version from S3 for CI/CD stability
- **Python Environment**: All dependencies pre-installed
- **Jenkins User**: Proper user permissions (UID 1000)
- **Resource Management**: Optimized for CI/CD execution

## Jenkins & AWS Setup

### AWS EC2 Requirements
- **Instance Type**: t3.medium or higher (minimum 2GB RAM)
- **Docker**: Pre-installed on EC2
- **Security Groups**: Allow Jenkins port (8080) and SSH (22)

### Jenkins Pipeline Features
- **Docker Container**: Runs tests in isolated environment
- **S3 Integration**: Downloads configuration from S3
- **Credential Management**: Secure AWS credentials handling
- **Resource Cleanup**: Automatic container cleanup after tests

### Jenkins Credentials Setup
For AWS access in the Jenkins pipeline, use a "username with password" credential:
- **Username**: AWS Access Key ID
- **Password**: AWS Secret Access Key



## How It Works

The framework automatically detects the environment and loads the appropriate configuration:

| Environment | Source | Driver Management | Use Case |
|-------------|--------|-------------------|----------|
| `development` | Local `settings.ini` | Automatic (Selenium Manager) | Local development |
| `staging` | S3 `s3_settings.ini` | Fixed ChromeDriver from S3 | Staging testing and CI/CD |



## Configuration Files

### Local Development (`settings.ini`)

```ini
[ALL]
browser = chrome
headless = false
timeout = 30

[development]
base_url = https://your-application-url.com
headless = false
test_username = testuser@example.com
test_password = testpassword123 
```

### S3 Configuration (`s3_settings.ini`)

Upload this file to your S3 bucket (no [development] section needed):

```ini
[ALL]
browser = chrome
headless = false
timeout = 30

[staging]
base_url = https://your-staging-url.com
headless = true
test_username = testuser@example.com
test_password = testpassword123 
```

## Screenshots

Screenshots are automatically captured when tests fail and saved in the `screenshots/` directory with descriptive names including scenario name and timestamp.

## Running Tests

### Local Development
```bash
# All tests
behave

# Specific feature
behave features/demoblaze_authentication.feature



### Docker Environment
```bash
# Run tests in Docker
docker run --rm selenium-bdd-framework behave

# Run specific feature in Docker
docker run --rm selenium-bdd-framework behave features/demoblaze_authentication.feature
```

## Requirements

- Python 3.9+
- Chrome or Safari browser
- AWS CLI (for S3 environments)
- Docker (for CI/CD)
- Jenkins (for CI/CD)


## Security Notes

- Never store sensitive information in code or config files
- All credentials are managed securely in Jenkins credentials store
- Docker containers are isolated and cleaned up after execution
- S3 bucket policies should be properly configured for access control


---
