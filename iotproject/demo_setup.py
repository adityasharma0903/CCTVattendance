"""
Quick Demo Setup Script
Creates sample student database for testing the attendance system
"""

import os
import json
from datetime import datetime

def create_demo_database():
    """Create a demo student database with sample entries"""
    
    print("\n" + "="*70)
    print("       DEMO SETUP - CLASSROOM ATTENDANCE SYSTEM")
    print("="*70)
    
    # Create folders
    if not os.path.exists("student_images"):
        os.makedirs("student_images")
        print("✅ Created 'student_images' folder")
    
    print("\n📝 DEMO MODE")
    print("This will create a sample database structure.")
    print("You'll need to add actual student photos to make it work.\n")
    
    # Sample database structure
    demo_db = {
        "101": {
            "name": "Student 1",
            "roll_number": "101",
            "image_path": "student_images/101_student1.jpg",
            "embedding": [],  # Will be generated when real image is added
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "102": {
            "name": "Student 2",
            "roll_number": "102",
            "image_path": "student_images/102_student2.jpg",
            "embedding": [],
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "103": {
            "name": "Student 3",
            "roll_number": "103",
            "image_path": "student_images/103_student3.jpg",
            "embedding": [],
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    
    # Create empty attendance log
    demo_attendance = []
    
    print("⚠️  IMPORTANT STEPS:")
    print("\n1. Add student photos to 'student_images' folder:")
    print("   - 101_student1.jpg")
    print("   - 102_student2.jpg")
    print("   - 103_student3.jpg")
    print("\n2. Run setup_students.py to register actual students")
    print("\n3. Then run classroom_attendance.py to start the system")
    
    print("\n" + "="*70)
    print("✅ Demo folders created!")
    print("="*70)
    
    # Create instruction file
    instructions = """
SETUP INSTRUCTIONS:
==================

1. ADD STUDENT PHOTOS:
   - Place clear frontal face photos in 'student_images' folder
   - Format: RollNumber_Name.jpg (e.g., 101_Aditya.jpg)
   - Requirements: Good lighting, no sunglasses, high resolution

2. REGISTER STUDENTS:
   Run: python setup_students.py
   
   Follow prompts to add each student:
   - Enter Roll Number
   - Enter Student Name  
   - Enter image path (e.g., student_images/101_Aditya.jpg)

3. START ATTENDANCE SYSTEM:
   Run: python classroom_attendance.py
   
   Controls:
   - 'q' to quit
   - 's' to show today's attendance
   - 'r' to generate Excel report

4. TEST WITH YOUR CAMERA:
   - Sit in front of camera
   - Make sure face is clearly visible
   - System will detect and recognize you

TROUBLESHOOTING:
===============
- Face not detected? → Check lighting
- Wrong recognition? → Increase similarity threshold
- Camera not working? → Try different camera index

For detailed help, see README_ATTENDANCE.md
"""
    
    with open("SETUP_INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)
    
    print("\n📄 Created SETUP_INSTRUCTIONS.txt - Read this file for detailed steps!")
    print("\n")

if __name__ == "__main__":
    create_demo_database()