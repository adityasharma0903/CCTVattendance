"""
Cloudinary Helper for Face Recognition System
Downloads and processes images from Cloudinary URLs
"""

import requests
import cv2
import numpy as np
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def download_image_from_url(image_url: str) -> Optional[np.ndarray]:
    """
    Download image from Cloudinary URL and convert to OpenCV format
    
    Args:
        image_url: Cloudinary image URL
    
    Returns:
        OpenCV image (numpy array) or None if failed
    """
    try:
        # Download image
        response = requests.get(image_url, timeout=10)
        if response.status_code != 200:
            logger.error(f"❌ Failed to download image: HTTP {response.status_code}")
            return None
        
        # Convert to numpy array
        nparr = np.frombuffer(response.content, np.uint8)
        
        # Decode to OpenCV image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            logger.error(f"❌ Failed to decode image from URL")
            return None
        
        return img
        
    except Exception as e:
        logger.error(f"❌ Error downloading image from URL: {e}")
        return None


def get_image_from_student(student_data: dict) -> Optional[np.ndarray]:
    """
    Get image from student data (supports both Cloudinary URL and local path)
    
    Args:
        student_data: Student dictionary with image_url or image_path
    
    Returns:
        OpenCV image (numpy array) or None if failed
    """
    # Try Cloudinary URL first (preferred)
    if "image_url" in student_data and student_data["image_url"]:
        logger.info(f"📥 Downloading image from Cloudinary for {student_data.get('name', 'Unknown')}")
        img = download_image_from_url(student_data["image_url"])
        if img is not None:
            return img
        logger.warning(f"⚠️ Failed to download from Cloudinary, trying local path...")
    
    # Fallback to local path (legacy support)
    if "image_path" in student_data and student_data["image_path"]:
        import os
        image_path = student_data["image_path"]
        if os.path.exists(image_path):
            logger.info(f"📂 Loading image from local path for {student_data.get('name', 'Unknown')}")
            img = cv2.imread(image_path)
            return img
        else:
            logger.error(f"❌ Local image file not found: {image_path}")
    
    logger.error(f"❌ No valid image source found for student")
    return None


if __name__ == "__main__":
    # Test downloading an image
    test_url = "https://res.cloudinary.com/demo/image/upload/sample.jpg"
    print(f"Testing image download from: {test_url}")
    img = download_image_from_url(test_url)
    if img is not None:
        print(f"✅ Successfully downloaded image: {img.shape}")
    else:
        print("❌ Failed to download test image")
