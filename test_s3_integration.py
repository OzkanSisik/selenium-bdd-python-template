#!/usr/bin/env python3
"""
Test script for S3 integration
Demonstrates how to use the S3 settings loading functionality
"""
import os

def test_s3_integration():
    """Test S3 settings integration."""
    print("🧪 Testing S3 Settings Integration")
    print("=" * 40)
    
    # Test different environments
    test_cases = [
        ('development', 'Local settings.ini'),
        ('staging', 'S3 settings.ini')
    ]
    
    for env, description in test_cases:
        print(f"\n📋 Testing {env} environment ({description})")
        print("-" * 50)
        
        # Set environment variable
        os.environ['ENVIRONMENT'] = env
        
        try:
            from utils.settings_manager import SettingsManager
            settings_manager = SettingsManager()
            
        except Exception as e:
            print(f"❌ Error testing {env}: {e}")
    
    print(f"\n✅ Testing complete!")
    print(f"\n📋 Usage Instructions:")
    print(f"   1. Set S3_BUCKET_NAME=ozkanbucket")
    print(f"   2. Set S3_REGION environment variable (optional, defaults to eu-central-1)")
    print(f"   3. Configure AWS credentials")
    print(f"   4. Upload s3_settings.ini to your S3 bucket")
    print(f"   5. Set ENVIRONMENT=staging to use S3 settings")


if __name__ == "__main__":
    test_s3_integration() 