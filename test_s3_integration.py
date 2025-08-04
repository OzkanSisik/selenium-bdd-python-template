#!/usr/bin/env python3
"""
Test script for S3 integration
Demonstrates how to use the S3 settings loading functionality
"""
from utils.settings_manager import SettingsManager

def test_s3_integration():
    """Test environment-specific settings loading."""
    print("🧪 Testing Environment-Specific Settings Loading")
    print("=" * 40)
    
    settings_manager = SettingsManager()
    print(f"✅ Environment detected: {settings_manager.environment}")
    
    settings = settings_manager.get_settings()
    print(f"📁 Settings loaded: {len(settings)} items")
    
    if len(settings) > 0:
        print(f"📋 Sample settings: {dict(list(settings.items())[:3])}")
        print(f"✅ SUCCESS: Settings loaded successfully")
    else:
        print(f"❌ FAILED: No settings loaded")
    
    print(f"\n✅ Testing complete!")
    print(f"\n📋 Test Summary:")
    print(f"   - Local: Uses settings.ini from project root")
    print(f"   - Jenkins: Uses s3_settings.ini from S3 bucket")


if __name__ == "__main__":
    test_s3_integration() 