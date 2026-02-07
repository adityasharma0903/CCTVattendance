"""
Direct MongoDB → Pinecone migration (SERVERLESS – WORKING VERSION)
✔ Uses NEW Pinecone SDK
✔ Compatible with serverless / dense indexes
✔ Retry logic included
"""

import os
import time
from pymongo import MongoClient
from dotenv import load_dotenv
from pinecone import Pinecone

# ============================================================
# LOAD ENV
# ============================================================

load_dotenv("backend/.env")

MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "CCTV")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "face-recognition")

# ============================================================
# MAIN
# ============================================================

def main():
    print("🚀 Direct MongoDB → Pinecone Migration (SERVERLESS FIXED)")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. MongoDB
    # --------------------------------------------------------
    print("\n📍 Step 1: Connect to MongoDB...")
    try:
        client = MongoClient(MONGODB_URL)
        db = client[DB_NAME]
        students_collection = db["students"]
        print(f"✅ Connected to MongoDB ({DB_NAME})")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return

    # --------------------------------------------------------
    # 2. Pinecone (NEW SDK – NO ENV / REGION)
    # --------------------------------------------------------
    print("\n📍 Step 2: Initialize Pinecone (serverless)...")
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)

        stats = index.describe_index_stats()
        print("✅ Pinecone connected")
        print(f"   Dimension: {stats.get('dimension')}")
    except Exception as e:
        print(f"❌ Pinecone connection failed: {e}")
        return

    # --------------------------------------------------------
    # 3. Fetch students
    # --------------------------------------------------------
    print("\n📍 Step 3: Fetch students from MongoDB...")
    try:
        students = list(students_collection.find({}))
        print(f"✅ Found {len(students)} students")
    except Exception as e:
        print(f"❌ MongoDB query failed: {e}")
        return

    # --------------------------------------------------------
    # 4. Prepare vectors
    # --------------------------------------------------------
    print("\n📍 Step 4: Prepare vectors...")
    vectors = []
    skipped = 0

    for student in students:
        student_id = str(student.get("_id"))
        roll_number = student.get("roll_number", "")
        name = student.get("name", "Unknown")
        embedding = student.get("embedding")

        if not embedding or not isinstance(embedding, list):
            print(f"⚠️  Skipped {name}: no embedding")
            skipped += 1
            continue

        # ✅ FIX: Use roll_number as vector ID, not MongoDB _id
        vectors.append({
            "id": roll_number,  # Changed from student_id to roll_number
            "values": embedding,
            "metadata": {
                "name": name,
                "roll_number": roll_number,
                "batch_id": str(student.get("batch_id", "")),
                "mongo_id": student_id  # Keep MongoDB ID in metadata
            }
        })

        print(f"✅ Prepared: {name} (roll={roll_number}) | dim={len(embedding)}")

    # --------------------------------------------------------
    # 5. Upload
    # --------------------------------------------------------
    print(f"\n📍 Step 5: Uploading {len(vectors)} vectors to Pinecone...")
    success = 0
    failed = 0

    for vec in vectors:
        for attempt in range(3):
            try:
                index.upsert(vectors=[vec])
                print(f"✅ Pushed: {vec['metadata']['name']}")
                success += 1
                break
            except Exception as e:
                if attempt < 2:
                    print(f"⚠️ Retry {attempt + 1} for {vec['metadata']['name']}")
                    time.sleep(1)
                else:
                    print(f"❌ Failed: {vec['metadata']['name']} → {e}")
                    failed += 1

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETE")
    print("=" * 60)
    print(f"Total students : {len(students)}")
    print(f"✅ Pushed      : {success}")
    print(f"⚠️ Skipped     : {skipped}")
    print(f"❌ Failed      : {failed}")
    print("=" * 60)

    client.close()


if __name__ == "__main__":
    main()
