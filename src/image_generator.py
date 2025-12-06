"""
Image Generator using Pollinations.ai
Free AI image generation for premium users
"""

import requests
from pathlib import Path
import threading
from datetime import datetime

class ImageGenerator:
    def __init__(self, app_data_dir):
        self.app_data_dir = Path(app_data_dir)
        self.images_dir = self.app_data_dir / "generated_images"
        self.images_dir.mkdir(exist_ok=True)
        
        # Pollinations.ai API endpoint (free, no API key needed!)
        self.api_url = "https://image.pollinations.ai/prompt/{prompt}"
        
    def generate_image(self, prompt, callback=None, width=1024, height=1024):
        """
        Generate an image using Pollinations.ai
        
        Args:
            prompt: Text description of the image
            callback: Function to call when complete (receives success, path/error)
            width: Image width (default 1024)
            height: Image height (default 1024)
        """
        def _generate():
            try:
                # Clean up the prompt for URL
                clean_prompt = prompt.replace(" ", "%20")
                
                # Build URL with parameters
                url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width={width}&height={height}&nologo=true"
                
                # Download the image
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Save the image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"image_{timestamp}.png"
                filepath = self.images_dir / filename
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                if callback:
                    callback(True, str(filepath))
                    
                return True, str(filepath)
                
            except requests.Timeout:
                error = "Image generation timed out. Please try again."
                if callback:
                    callback(False, error)
                return False, error
                
            except requests.RequestException as e:
                error = f"Failed to generate image: {str(e)}"
                if callback:
                    callback(False, error)
                return False, error
                
            except Exception as e:
                error = f"Unexpected error: {str(e)}"
                if callback:
                    callback(False, error)
                return False, error
        
        # Run in background thread
        thread = threading.Thread(target=_generate, daemon=True)
        thread.start()
        
    def generate_image_sync(self, prompt, width=1024, height=1024):
        """
        Generate an image synchronously (blocking)
        Returns: (success, path_or_error)
        """
        try:
            # Clean up the prompt for URL
            clean_prompt = prompt.replace(" ", "%20")
            
            # Build URL
            url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width={width}&height={height}&nologo=true"
            
            # Download the image
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.png"
            filepath = self.images_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            return True, str(filepath)
            
        except Exception as e:
            return False, f"Failed to generate image: {str(e)}"
    
    def get_generated_images(self):
        """Get list of all generated images"""
        return list(self.images_dir.glob("*.png"))
    
    def open_image(self, filepath):
        """Open an image in the default viewer"""
        import os
        import platform
        
        system = platform.system()
        if system == "Windows":
            os.startfile(filepath)
        elif system == "Darwin":  # macOS
            os.system(f"open {filepath}")
        else:  # Linux
            os.system(f"xdg-open {filepath}")
