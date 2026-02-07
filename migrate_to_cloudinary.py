"""
Migrate Existing Local Images to Cloudinary
============================================

This script helps you migrate existing student images from local folders 
to Cloudinary cloud storage.

Usage:
    python migrate_to_cloudinary.py

What it does:
1. Reads students_database.json
2. For each student with local image_path:
   - Uploads image to Cloudinary
   - Updates student record with image_url
   - Keeps image_path as fallback
3. Saves updated database

Author: Face Recognition System
Date: 2026-02-06
"""

import sys
import os

# Add backend to path for cloudinary_utils
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.cloudinary_utils import upload_from_file_path, validate_cloudinary_config
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
STUDENTS_DB_PATH = "iotproject/students_database.json"
BACKUP_PATH = "iotproject/students_database_backup.json"

def load_students():
    """Load students database"""
    if not os.path.exists(STUDENTS_DB_PATH):
        logger.error(f"❌ Database not found: {STUDENTS_DB_PATH}")
        return None
    
    with open(STUDENTS_DB_PATH, 'r') as f:
        return json.load(f)

def save_students(students_data):
    """Save students database"""
    with open(STUDENTS_DB_PATH, 'w') as f:
        json.dump(students_data, f, indent=2)
    logger.info("✅ Database saved successfully")

def backup_database():
    """Create backup of existing database"""
    if os.path.exists(STUDENTS_DB_PATH):
        with open(STUDENTS_DB_PATH, 'r') as f:
            data = json.load(f)
        with open(BACKUP_PATH, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"✅ Backup created: {BACKUP_PATH}")
        return True
    return False

def migrate_images():
    """Migrate all local images to Cloudinary"""
    
    print("=" * 70)
    print("MIGRATE IMAGES TO CLOUDINARY")
    print("=" * 70)
    
    # Step 1: Validate Cloudinary configuration
    print("\n1️⃣ Validating Cloudinary configuration...")
    if not validate_cloudinary_config():
        print("\n❌ FAILED: Cloudinary is not configured!")
        print("\nPlease follow these steps:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Cloudinary credentials to .env")
        print("  3. Get credentials from: https://cloudinary.com/console")
        return False
    
    print("✅ Cloudinary configuration is valid")
    
    # Step 2: Load students database
    print("\n2️⃣ Loading students database...")
    students_data = load_students()
    if not students_data:
        return False
    
    print(f"✅ Found {len(students_data)} students")
    
    # Step 3: Create backup
    print("\n3️⃣ Creating backup...")
    if backup_database():
        print(f"✅ Backup saved to: {BACKUP_PATH}")
    
    # Step 4: Migrate images
    print("\n4️⃣ Migrating images to Cloudinary...")
    print("-" * 70)
    
    migrated_count = 0
    skipped_count = 0
    error_count = 0
    
    for roll_number, student_data in students_data.items():
        student_name = student_data.get("name", "Unknown")
        
        # Skip if already has Cloudinary URL
        if "image_url" in student_data and student_data["image_url"]:
            print(f"⏭️  {student_name} ({roll_number}) - Already on Cloudinary")
            skipped_count += 1
            continue
        
        # Skip if no local image path
        if "image_path" not in student_data or not student_data["image_path"]:
            print(f"⚠️  {student_name} ({roll_number}) - No image path found")
            skipped_count += 1
            continue
        
        image_path = student_data["image_path"]
        
        # Check if image file exists
        if not os.path.exists(image_path):
            print(f"❌ {student_name} ({roll_number}) - Image file not found: {image_path}")
            error_count += 1
            continue
        
        # Upload to Cloudinary
        print(f"⏳ Uploading: {student_name} ({roll_number})...")
        student_id = student_data.get("student_id", f"STU_{roll_number}")
        
        result = upload_from_file_path(image_path, student_id, roll_number)
        
        if result:
            # Update student record
            student_data["image_url"] = result["url"]
            student_data["cloudinary_public_id"] = result["public_id"]
            student_data["image_metadata"] = {
                "width": result.get("width"),
                "height": result.get("height"),
                "format": result.get("format"),
                "size_bytes": result.get("bytes")
            }
            
            print(f"   ✅ Success: {result['url']}")
            migrated_count += 1
        else:
            print(f"   ❌ Failed to upload image")
            error_count += 1
    
    # Step 5: Save updated database
    print("\n5️⃣ Saving updated database...")
    save_students(students_data)
    
    # Summary
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"✅ Migrated:  {migrated_count} images")
    print(f"⏭️  Skipped:   {skipped_count} images")
    print(f"❌ Errors:    {error_count} images")
    print(f"📊 Total:     {len(students_data)} students")
    print("=" * 70)
    
    if migrated_count > 0:
        print("\n🎉 Migration completed successfully!")
        print(f"\n📂 Backup saved at: {BACKUP_PATH}")
        print("\n✅ Your images are now on Cloudinary!")
        print("   - View them at: https://cloudinary.com/console/media_library")
        print("   - Face recognition will now use cloud URLs")
        print("   - You can safely delete local images (after verification)")
    
    if error_count > 0:
        print(f"\n⚠️ {error_count} images failed to upload.")
        print("   Please check the errors above and retry.")
    
    return True

def main():
    """Main function"""
    
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "CLOUDINARY MIGRATION TOOL" + " " * 28 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    print("This tool will:")
    print("  • Upload your local student images to Cloudinary")
    print("  • Update database with cloud URLs")
    print("  • Create a backup (just in case)")
    print("\n")
    
    response = input("Ready to start migration? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Migration cancelled.")
        return
    
    success = migrate_images()
    
    if success:
        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("1. Test face recognition with camera service")
        print("2. Verify images on Cloudinary dashboard")
        print("3. Once confirmed, you can delete local images")
        print("\n")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
        print("   Your original database is safe.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user.")
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")
        print("\nPlease report this error if it persists.")
