import os
import json
from classroom_attendance import StudentDatabase

def setup_students():
    """Interactive setup to add students to the system"""
    print("\n" + "="*70)
    print("       STUDENT REGISTRATION SETUP")
    print("="*70)
    
    # Create student images folder if not exists
    if not os.path.exists("student_images"):
        os.makedirs("student_images")
        print("✅ Created 'student_images' folder")
    
    db = StudentDatabase()
    
    print("\n📝 Current Students in Database:")
    if len(db.students) == 0:
        print("   (None)")
    else:
        for roll, data in db.students.items():
            print(f"   • {data['name']} (Roll: {roll})")
    
    print("\n" + "="*70)
    print("ADD NEW STUDENTS")
    print("="*70)
    print("\nInstructions:")
    print("1. Place student photos in the 'student_images' folder")
    print("2. Photos should contain a clear frontal face")
    print("3. Recommended: Use format 'RollNumber_Name.jpg' (e.g., '101_John.jpg')")
    print("\nType 'done' when finished adding students.\n")
    
    while True:
        print("-" * 50)
        roll = input("Enter Roll Number (or 'done' to finish): ").strip()
        
        if roll.lower() == 'done':
            break
        
        if roll in db.students:
            print(f"⚠️  Roll number {roll} already exists!")
            overwrite = input("Overwrite? (yes/no): ").strip().lower()
            if overwrite != 'yes':
                continue
        
        name = input("Enter Student Name: ").strip()
        image_path = input("Enter image path (relative to current directory): ").strip()
        
        # Add student
        success = db.add_student(roll, name, image_path)
        
        if success:
            db.save_database()
            print(f"✅ {name} registered successfully!\n")
        else:
            print(f"❌ Failed to register {name}\n")
    
    print("\n" + "="*70)
    print("SETUP COMPLETE!")
    print("="*70)
    print(f"\n✅ Total students registered: {len(db.students)}")
    print("\nYou can now run the attendance system:")
    print("   python classroom_attendance.py")
    print("\n")

if __name__ == "__main__":
    setup_students()