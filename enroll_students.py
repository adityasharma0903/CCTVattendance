"""
Enroll students to Pinecone via Backend API
Uses existing backend enrollment endpoint to properly push embeddings
"""
import requests
import json

# Configuration
BACKEND_API = "http://localhost:8000/api"

def enroll_student(roll_number, name, embedding):
    """Enroll a student via backend API"""
    try:
        # Backend expects enrollment data
        # We'll use the embedding directly without re-computing
        data = {
            "roll_number": roll_number,
            "name": name,
            "embeddings": [embedding]  # Already have the embedding, just wrap it
        }
        
        response = requests.post(
            f"{BACKEND_API}/enroll-student",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "Success"
        else:
            return False, f"Status {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)

def main():
    print("🚀 Enrolling students via Backend API")
    print("=" * 60)
    
    # 1. Fetch students from MongoDB
    print("\n📍 Step 1: Fetch students from MongoDB...")
    try:
        response = requests.get(f"{BACKEND_API}/students")
        if response.status_code != 200:
            print(f"❌ Failed to fetch students: {response.status_code}")
            return
        
        students = response.json()
        print(f"✅ Fetched {len(students)} students")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # 2. Enroll each student
    print("\n📍 Step 2: Enroll students...")
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for student in students:
        roll_number = student.get("roll_number")
        name = student.get("name")
        embedding = student.get("embedding")
        
        if not embedding:
            print(f"⚠️  Skipping {name} ({roll_number}): No embedding")
            skip_count += 1
            continue
        
        success, msg = enroll_student(roll_number, name, embedding)
        
        if success:
            print(f"✅ Enrolled: {name} ({roll_number})")
            success_count += 1
        else:
            print(f"❌ Failed: {name} ({roll_number}): {msg}")
            fail_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ ENROLLMENT COMPLETE!")
    print("=" * 60)
    print(f"   Total students: {len(students)}")
    print(f"   ✅ Successfully enrolled: {success_count}")
    print(f"   ⚠️  Skipped (no embedding): {skip_count}")
    print(f"   ❌ Failed: {fail_count}")
    print("\n💡 Check Pinecone console for records:")
    print("   https://app.pinecone.io/")
    print("=" * 60)

if __name__ == "__main__":
    main()
