"""
Cloudinary Integration for Face Recognition System
Handles image upload and management on Cloudinary
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv
import logging
from typing import Optional, Dict
import requests
from io import BytesIO

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# ============================================================================
# CLOUDINARY CONFIGURATION
# ============================================================================

def configure_cloudinary():
    """Configure Cloudinary with credentials from environment variables"""
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )
    logger.info("✅ Cloudinary configured successfully")

# Configure on import
configure_cloudinary()

# ============================================================================
# IMAGE UPLOAD FUNCTIONS
# ============================================================================

def upload_student_image(image_file, student_id: str, roll_number: str) -> Optional[Dict]:
    """
    Upload student image to Cloudinary
    
    Args:
        image_file: File object or file path
        student_id: Unique student ID
        roll_number: Student roll number
    
    Returns:
        Dict with image URL and public_id, or None if failed
    """
    try:
        # Create a folder structure: face_recognition/students/{roll_number}
        folder_path = f"face_recognition/students"
        public_id = f"{folder_path}/{roll_number}_{student_id}"
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            image_file,
            public_id=public_id,
            folder=folder_path,
            overwrite=True,
            resource_type="image",
            tags=["student", "face_recognition", roll_number]
        )
        
        logger.info(f"✅ Image uploaded successfully for student {roll_number}")
        
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "width": result.get("width"),
            "height": result.get("height"),
            "format": result.get("format"),
            "bytes": result.get("bytes")
        }
        
    except Exception as e:
        logger.error(f"❌ Error uploading image for student {roll_number}: {e}")
        return None


def upload_student_image_variant(
    image_file,
    student_id: str,
    roll_number: str,
    variant: str
) -> Optional[Dict]:
    """
    Upload a variant of a student image to Cloudinary without overwriting.

    Args:
        image_file: File object or file path
        student_id: Unique student ID
        roll_number: Student roll number
        variant: Variant suffix (e.g. "1", "2", "front")

    Returns:
        Dict with image URL and public_id, or None if failed
    """
    try:
        folder_path = f"face_recognition/students"
        public_id = f"{folder_path}/{roll_number}_{student_id}_{variant}"

        result = cloudinary.uploader.upload(
            image_file,
            public_id=public_id,
            folder=folder_path,
            overwrite=False,
            resource_type="image",
            tags=["student", "face_recognition", roll_number]
        )

        logger.info(f"✅ Image variant uploaded successfully for student {roll_number}")

        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "width": result.get("width"),
            "height": result.get("height"),
            "format": result.get("format"),
            "bytes": result.get("bytes")
        }
    except Exception as e:
        logger.error(f"❌ Error uploading image variant for student {roll_number}: {e}")
        return None


def upload_from_file_path(file_path: str, student_id: str, roll_number: str) -> Optional[Dict]:
    """
    Upload student image from local file path to Cloudinary
    
    Args:
        file_path: Local path to the image file
        student_id: Unique student ID
        roll_number: Student roll number
    
    Returns:
        Dict with image URL and public_id, or None if failed
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"❌ File not found: {file_path}")
            return None
        
        return upload_student_image(file_path, student_id, roll_number)
        
    except Exception as e:
        logger.error(f"❌ Error uploading from file path: {e}")
        return None


def delete_student_image(public_id: str) -> bool:
    """
    Delete image from Cloudinary
    
    Args:
        public_id: Cloudinary public ID of the image
    
    Returns:
        True if successful, False otherwise
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        if result.get("result") == "ok":
            logger.info(f"✅ Image deleted successfully: {public_id}")
            return True
        else:
            logger.warning(f"⚠️ Image deletion result: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error deleting image {public_id}: {e}")
        return False


def get_image_url(public_id: str, transformation: Optional[Dict] = None) -> str:
    """
    Get Cloudinary URL for an image with optional transformations
    
    Args:
        public_id: Cloudinary public ID
        transformation: Optional transformation parameters (resize, crop, etc.)
    
    Returns:
        Image URL
    """
    try:
        if transformation:
            url = cloudinary.CloudinaryImage(public_id).build_url(**transformation)
        else:
            url = cloudinary.CloudinaryImage(public_id).build_url()
        
        return url
        
    except Exception as e:
        logger.error(f"❌ Error getting image URL: {e}")
        return ""


def download_image_from_url(image_url: str) -> Optional[bytes]:
    """
    Download image from Cloudinary URL
    
    Args:
        image_url: Cloudinary image URL
    
    Returns:
        Image bytes or None if failed
    """
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            logger.error(f"❌ Failed to download image: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error downloading image: {e}")
        return None


def get_optimized_url(public_id: str, width: int = 800, quality: str = "auto") -> str:
    """
    Get optimized image URL for better performance
    
    Args:
        public_id: Cloudinary public ID
        width: Target width
        quality: Quality setting (auto, best, good, etc.)
    
    Returns:
        Optimized image URL
    """
    transformation = {
        "width": width,
        "quality": quality,
        "fetch_format": "auto"
    }
    return get_image_url(public_id, transformation)


# ============================================================================
# BATCH OPERATIONS
# ============================================================================

def upload_multiple_images(image_files: list, student_data: list) -> list:
    """
    Upload multiple student images in batch
    
    Args:
        image_files: List of file objects or file paths
        student_data: List of dicts with student_id and roll_number
    
    Returns:
        List of upload results
    """
    results = []
    
    for i, (image_file, student) in enumerate(zip(image_files, student_data)):
        result = upload_student_image(
            image_file,
            student["student_id"],
            student["roll_number"]
        )
        results.append({
            "student_id": student["student_id"],
            "roll_number": student["roll_number"],
            "upload_result": result
        })
    
    logger.info(f"✅ Batch upload completed: {len(results)} images processed")
    return results


def list_student_images(max_results: int = 100) -> list:
    """
    List all student images from Cloudinary
    
    Args:
        max_results: Maximum number of results to return
    
    Returns:
        List of image resources
    """
    try:
        result = cloudinary.api.resources(
            type="upload",
            prefix="face_recognition/students",
            max_results=max_results
        )
        return result.get("resources", [])
        
    except Exception as e:
        logger.error(f"❌ Error listing images: {e}")
        return []


# ============================================================================
# VALIDATION
# ============================================================================

def validate_cloudinary_config() -> bool:
    """
    Validate Cloudinary configuration
    
    Returns:
        True if configuration is valid, False otherwise
    """
    try:
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
        
        if not all([cloud_name, api_key, api_secret]):
            logger.error("❌ Cloudinary credentials are missing in environment variables")
            return False
        
        # Test connection by getting account details
        cloudinary.api.ping()
        logger.info("✅ Cloudinary configuration is valid")
        return True
        
    except Exception as e:
        logger.error(f"❌ Cloudinary configuration validation failed: {e}")
        return False


if __name__ == "__main__":
    # Test configuration
    print("Testing Cloudinary Configuration...")
    if validate_cloudinary_config():
        print("✅ Cloudinary is properly configured!")
    else:
        print("❌ Cloudinary configuration failed!")
        print("\nMake sure you have set the following environment variables:")
        print("  - CLOUDINARY_CLOUD_NAME")
        print("  - CLOUDINARY_API_KEY")
        print("  - CLOUDINARY_API_SECRET")
