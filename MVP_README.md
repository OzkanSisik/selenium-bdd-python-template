# MVP S3 Settings Integration

A simple, secure configuration management system for your test automation framework.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install boto3
```

### 2. Configure AWS (for S3 environments)
```bash
aws configure
```

### 3. Set Environment Variables
```bash
# For local development
export ENVIRONMENT=development

# For S3 environments
export ENVIRONMENT=staging
export S3_BUCKET_NAME=ozkanbucket
```

### 4. Create Settings Files

**Local Development** (`settings.ini`):
```ini
[ALL]
browser = chrome
headless = false
timeout = 30

[development]
base_url = https://localhost:3000
```

**S3 Settings** (`s3_settings.ini` - upload to S3):
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
```

### 5. Upload to S3
```bash
aws s3 cp s3_settings.ini s3://ozkanbucket/s3_settings.ini
```

### 6. Use in Your Code
```python
from mvp_s3_settings import mvp_settings

# Get settings
base_url = mvp_settings.get('base_url', 'https://default.example.com')
browser = mvp_settings.get('browser', 'chrome')
headless = mvp_settings.get('headless', False)

# Use in your tests
print(f"Testing {base_url} with {browser}")
```

## 📋 Environment Behavior

| Environment | Source | File |
|-------------|--------|------|
| `development` | Local | `settings.ini` |
| `staging` | S3 | `s3_settings.ini` |
| `production` | S3 | `s3_settings.ini` |
| `JENKINS` | S3 | `s3_settings.ini` |

## 🧪 Testing

```bash
# Test all environments
python test_mvp.py

# Test specific environment
ENVIRONMENT=staging python example_usage.py
```

## 🔒 Security

- ✅ No credentials in code
- ✅ Uses AWS CLI configuration
- ✅ Temporary files auto-deleted
- ✅ Environment-based configuration

## 📁 Files

- `mvp_s3_settings.py` - Main MVP implementation
- `test_mvp.py` - Test script
- `example_usage.py` - Usage example
- `settings.ini` - Local development settings
- `s3_settings.ini` - S3 settings (upload to S3)

## 🚀 Production Ready

This MVP is ready for:
- ✅ Local development
- ✅ Jenkins CI/CD
- ✅ Production environments
- ✅ Secure credential management 