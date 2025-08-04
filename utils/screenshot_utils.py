"""
Simple Screenshot Utility
Provides basic screenshot functionality for test debugging
"""
import os
import logging
from datetime import datetime
from pathlib import Path
from utils.settings_manager import settings_manager

logger = logging.getLogger(__name__)


class ScreenshotUtils:
    """Simple utility class for capturing screenshots"""
    
    def __init__(self, driver, output_dir=None):
        self.driver = driver
        # Get screenshot directory from settings, fallback to "screenshots"
        self.output_dir = output_dir or settings_manager.get("screenshot_dir", "screenshots")
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Ensure the output directory exists"""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def capture_screenshot(self, name=None, include_timestamp=True):
        """
        Capture a screenshot and save it to the output directory
        
        Args:
            name (str): Name for the screenshot file
            include_timestamp (bool): Whether to include timestamp in filename
            
        Returns:
            str: Path to the saved screenshot file
        """
        try:
            if name is None:
                name = "screenshot"
            
            if include_timestamp:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}.png"
            else:
                filename = f"{name}.png"
            
            filepath = os.path.join(self.output_dir, filename)
            
            # Take screenshot
            self.driver.save_screenshot(filepath)
            logger.info(f"Screenshot saved: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")
            return None
    
    def capture_screenshot_on_failure(self, scenario_name, step_name=None):
        """
        Capture screenshot specifically for test failures
        
        Args:
            scenario_name (str): Name of the failing scenario
            step_name (str): Name of the failing step
            
        Returns:
            str: Path to the saved screenshot file
        """
        safe_name = self._sanitize_filename(f"{scenario_name}_{step_name or 'failure'}")
        return self.capture_screenshot(safe_name)
    
    def _sanitize_filename(self, filename):
        """Sanitize filename for safe file system usage"""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename 