"""
Migrate student embeddings from MongoDB to Pinecone
Run this once to populate Pinecone index with existing students
"""
import os
import requests
import pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

# Configuration
MONGODB_API = "http://localhost:8000/api"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "face-recognition")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")

def main():
    print("🚀 Starting migration: MongoDB → Pinecone")
    print("=" * 60)
    
    # 1. Initialize Pinecone
    print("\n📍 Step 1: Initialize Pinecone...")
    try:
        pinecone.init(
            api_key=PINECONE_API_KEY,
            environment=PINECONE_ENVIRONMENT
        )
        
        # For serverless indexes, skip stats check initially
        print(f"✅ Pinecone initialized")
        
        # Connect to index (will fail if index doesn't exist)
        index = pinecone.Index(PINECONE_INDEX_NAME)
        print(f"✅ Connected to index: {PINECONE_INDEX_NAME}")
    except Exception as e:
        print(f"❌ Failed to connect to Pinecone: {e}")
        print(f"\n💡 Note: For serverless index, make sure:")
        print(f"   - Index name is correct: {PINECONE_INDEX_NAME}")
        print(f"   - Index exists in Pinecone console")
        print(f"   - API key has access")
        return
    
    # 3. Fetch students from MongoDB via backend API
    print("\n📍 Step 2: Fetch students from MongoDB...")
    try:
        response = requests.get(f"{MONGODB_API}/students")
        if response.status_code != 200:
            print(f"❌ Failed to fetch students: {response.status_code}")
            return
        
        students = response.json()
        print(f"✅ Fetched {len(students)} students from MongoDB")
    except Exception as e:
        print(f"❌ Error fetching students: {e}")
        return
    
    # 4. Push embeddings to Pinecone
    print("\n📍 Step 3: Push embeddings to Pinecone...")
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
        
        try:
            # Upsert to Pinecone
            index.upsert(
                vectors=[
                    {
                        "id": roll_number,
                        "values": embedding,
                        "metadata": {
                            "roll_number": roll_number,
                            "name": name,
                            "batch_id": student.get("batch_id", ""),
                            "branch": student.get("branch", "")
                        }
                    }
                ],
                namespace="face-recognition"
            )
            print(f"✅ Pushed: {name} ({roll_number})")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to push {name} ({roll_number}): {e}")
            fail_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 60)
    print(f"   Total students: {len(students)}")
    print(f"   ✅ Successfully pushed: {success_count}")
    print(f"   ⚠️  Skipped (no embedding): {skip_count}")
    print(f"   ❌ Failed: {fail_count}")
    print("\n💡 Verify in Pinecone console: https://app.pinecone.io/")
    print("=" * 60)

if __name__ == "__main__":
    main()
