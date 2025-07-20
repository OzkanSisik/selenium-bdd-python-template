# S3 Integration Guide

This guide explains how to use the professional S3 integration for remote configuration management in your test automation framework.

## Overview

The S3 integration provides a secure way to load configuration files from AWS S3 for production, staging, and CI/CD environments while keeping sensitive data out of your codebase.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Development   │    │     Staging     │    │   Production    │
│   Environment   │    │   Environment   │    │   Environment   │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ settings.ini    │    │ S3 settings.ini │    │ S3 settings.ini │
│ (local file)    │    │ (remote file)   │    │ (remote file)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Features

- **Secure**: Uses temporary files that are automatically cleaned up
- **Professional**: Industry-standard error handling and logging
- **Flexible**: Supports multiple environments and configurations
- **Secure**: No sensitive data in codebase
- **Reliable**: Proper exception handling and fallbacks

## Setup Instructions

### 1. Install Dependencies

```bash
pip install boto3
```

### 2. Configure AWS Credentials

#### Option A: AWS CLI (Recommended)
```bash
aws configure
```

#### Option B: Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### 3. Set Environment Variables

```bash
# Required
export S3_BUCKET_NAME=ozkanbucket

# Optional (defaults to eu-central-1)
export S3_REGION=eu-central-1
```

### 4. Upload Settings File to S3

Upload your `s3_settings.ini` file to your S3 bucket with the key `s3_settings.ini`.

**Important**: Never commit sensitive configuration files to your repository. Keep them in S3 only.

## Usage

### Environment Detection

The framework automatically detects the environment and loads the appropriate configuration:

| Environment | Source | Use Case |
|-------------|--------|----------|
| `development` | Local `settings.ini` | Local development |
| `staging` | S3 `settings.ini` | Staging testing |
| `production` | S3 `settings.ini` | Production testing |
| `JENKINS` | S3 `settings.ini` | CI/CD pipelines |

### Setting Environment

```bash
# Local development
ENVIRONMENT=development python your_test_script.py

# Staging environment (uses S3)
ENVIRONMENT=staging python your_test_script.py

# Production environment (uses S3)
ENVIRONMENT=production python your_test_script.py

# CI/CD environment (uses S3)
ENVIRONMENT=JENKINS python your_test_script.py
```

### In Your Code

```python
from settings_manager import settings_manager

# Get all settings
settings = settings_manager.get_settings()

# Get specific setting
base_url = settings_manager.get('base_url', 'https://default.example.com')
browser = settings_manager.get('browser', 'chrome')
headless = settings_manager.get('headless', False)

# Print configuration for debugging
settings_manager.print_config()
```

## S3 File Structure

Your `s3_settings.ini` file in S3 should follow this structure:

```ini
[ALL]
# Global settings for all environments
browser = chrome
headless = false
implicit_wait = 10
page_load_timeout = 30
screenshot_on_failure = true

[staging]
# Staging-specific settings
base_url = https://staging.example.com
test_data_path = /tmp/test_data
log_level = INFO
parallel_execution = true

[production]
# Production-specific settings
base_url = https://example.com
test_data_path = /tmp/test_data
log_level = WARNING
parallel_execution = false
headless = true

[JENKINS]
# CI/CD-specific settings
base_url = https://staging.example.com
test_data_path = /tmp/test_data
log_level = INFO
parallel_execution = true
headless = true
video_recording = true
```

## Security Best Practices

### 1. IAM Permissions

Create a minimal IAM policy for your S3 bucket:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::your-bucket-name/settings.ini"
        }
    ]
}
```

### 2. Bucket Security

- Enable server-side encryption
- Enable versioning for configuration changes
- Restrict bucket access to necessary users/roles
- Use bucket policies to limit access

### 3. Credential Management

- Use IAM roles instead of access keys when possible
- Rotate access keys regularly
- Never commit credentials to version control
- Use AWS Secrets Manager for sensitive data

## Error Handling

The S3 integration includes comprehensive error handling:

### Common Errors and Solutions

1. **AWS Credentials Not Found**
   ```
   ❌ AWS credentials not found. Please configure your AWS credentials.
   ```
   **Solution**: Run `aws configure` or set environment variables

2. **S3 Bucket Not Found**
   ```
   ❌ Bucket your-bucket-name not found
   ```
   **Solution**: Check bucket name and ensure it exists

3. **Settings File Not Found**
   ```
   ❌ File s3_settings.ini not found in bucket ozkanbucket
   ```
   **Solution**: Upload s3_settings.ini file to the bucket

4. **Access Denied**
   ```
   ❌ Access denied to bucket your-bucket-name
   ```
   **Solution**: Check IAM permissions and bucket policies

## Testing

### Test S3 Integration

```bash
python test_s3_integration.py
```

### Test Specific Environment

```bash
# Test local development
ENVIRONMENT=development python -c "from settings_manager import settings_manager; settings_manager.print_config()"

# Test S3 loading
ENVIRONMENT=staging python -c "from settings_manager import settings_manager; settings_manager.print_config()"
```

## Advanced Usage

### Custom S3 Key

You can customize the S3 key by modifying the `_load_remote_settings` method:

```python
# In settings_manager.py, change this line:
temp_file = s3_downloader.download_file_to_temp('s3_settings.ini')

# To use a custom key:
temp_file = s3_downloader.download_file_to_temp('config/s3_settings.ini')
```

### Environment-Specific Buckets

For different environments, use different buckets:

```bash
# Development
export S3_BUCKET_NAME=dev-test-settings

# Staging
export S3_BUCKET_NAME=staging-test-settings

# Production
export S3_BUCKET_NAME=prod-test-settings
```

### Direct S3 Downloader Usage

You can also use the S3Downloader directly:

```python
from utils.s3_utils import S3Downloader

# Initialize downloader
downloader = S3Downloader()

# Download to temporary file (recommended for config files)
temp_file = downloader.download_file_to_temp('s3_settings.ini')

# Download to specific path
downloader.download_file('s3_settings.ini', '/path/to/local/file.ini')

# Check if file exists
if downloader.file_exists('s3_settings.ini'):
    print("File exists in S3")

# Clean up temporary file
downloader.cleanup_temp_file(temp_file)
```

## Troubleshooting

### Debug Commands

```bash
# Check AWS credentials
aws sts get-caller-identity

# List S3 buckets
aws s3 ls

# List files in bucket
aws s3 ls s3://ozkanbucket/

# Download settings file for inspection
aws s3 cp s3://ozkanbucket/s3_settings.ini ./downloaded_settings.ini
```

### Common Issues

1. **Import Error**: Install boto3 with `pip install boto3`
2. **Permission Denied**: Check IAM permissions and bucket policies
3. **File Not Found**: Ensure settings.ini exists in the S3 bucket
4. **Region Mismatch**: Verify S3_REGION matches your bucket's region

## Migration Guide

### From Local-Only to S3

1. **Backup your current settings.ini**
2. **Upload to S3**: Upload your settings.ini to S3 bucket
3. **Set environment variables**: Configure S3_BUCKET_NAME and S3_REGION
4. **Test**: Run tests with ENVIRONMENT=staging
5. **Update CI/CD**: Configure CI/CD to use S3 settings

### Environment Variable Migration

```bash
# Old way (local only)
export BASE_URL=https://example.com
export BROWSER=chrome

# New way (S3 + environment variables)
export S3_BUCKET_NAME=your-settings-bucket
export ENVIRONMENT=staging
# Settings loaded from S3, can still override with env vars
export BASE_URL=https://staging.example.com
``` 