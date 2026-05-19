"""
Diagnostic script to check face embeddings in the database.
Run this to understand WHY everyone is being recognized as the same person.

Usage: python diagnose_embeddings.py
"""

import requests
import numpy as np
import json

BACKEND_API = "http://localhost:8000/api"

def main():
    print("=" * 70)
    print("🔍 FACE RECOGNITION EMBEDDING DIAGNOSTIC")
    print("=" * 70)
    
    # 1. Fetch all students
    try:
        response = requests.get(f"{BACKEND_API}/students", timeout=5)
        if response.status_code != 200:
            print(f"❌ Failed to fetch students: HTTP {response.status_code}")
            return
        students = response.json()
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure the backend is running: python -m uvicorn main:app --port 8000")
        return
    
    print(f"\n📊 Total students in database: {len(students)}")
    
    # 2. Check embeddings
    students_with_embeddings = []
    students_without_embeddings = []
    
    for s in students:
        roll = s.get("roll_number", "?")
        name = s.get("name", "?")
        emb = s.get("embedding")
        
        if emb and isinstance(emb, list) and len(emb) > 0:
            try:
                vec = np.array(emb, dtype=np.float32)
                if np.isfinite(vec).all() and vec.size > 0:
                    students_with_embeddings.append((roll, name, vec))
                else:
                    students_without_embeddings.append((roll, name, "has NaN/Inf values"))
            except:
                students_without_embeddings.append((roll, name, "invalid format"))
        else:
            students_without_embeddings.append((roll, name, "missing/empty"))
    
    print(f"✅ Students WITH valid embeddings: {len(students_with_embeddings)}")
    print(f"❌ Students WITHOUT valid embeddings: {len(students_without_embeddings)}")
    
    if students_without_embeddings:
        print("\n⚠️  Students missing embeddings (will NEVER be recognized):")
        for roll, name, reason in students_without_embeddings:
            print(f"   - {name} ({roll}): {reason}")
    
    if len(students_with_embeddings) < 2:
        print("\n🚨 CRITICAL: Less than 2 students have embeddings!")
        print("   If only 1 student has an embedding, ALL faces will match to that person.")
        if students_with_embeddings:
            print(f"   The only student with an embedding is: {students_with_embeddings[0][1]} ({students_with_embeddings[0][0]})")
        return
    
    # 3. Check embedding dimensions
    print(f"\n📏 Embedding dimensions:")
    for roll, name, vec in students_with_embeddings:
        norm = np.linalg.norm(vec)
        print(f"   {name} ({roll}): dim={vec.size}, L2-norm={norm:.4f}, min={vec.min():.4f}, max={vec.max():.4f}")
    
    # 4. Check if embeddings are identical (common bug)
    print(f"\n🔬 Checking if any embeddings are IDENTICAL (duplicate bug):")
    for i in range(len(students_with_embeddings)):
        for j in range(i + 1, len(students_with_embeddings)):
            r1, n1, v1 = students_with_embeddings[i]
            r2, n2, v2 = students_with_embeddings[j]
            if v1.size == v2.size and np.allclose(v1, v2, atol=1e-5):
                print(f"   🚨 IDENTICAL embeddings: {n1} ({r1}) == {n2} ({r2})")
                print(f"      This means they were enrolled with the SAME photo!")
    
    # 5. Compute full similarity matrix
    print(f"\n📊 INTER-STUDENT SIMILARITY MATRIX (cosine similarity):")
    print(f"   (Same person should be >0.6, different people should be <0.4)")
    print()
    
    # Header
    names = [f"{n[:12]}" for _, n, _ in students_with_embeddings]
    header = "              " + "  ".join(f"{n:>12}" for n in names)
    print(header)
    print("   " + "-" * (len(header) - 3))
    
    similarity_matrix = []
    for i, (r1, n1, v1) in enumerate(students_with_embeddings):
        row = []
        row_str = f"   {n1[:12]:>12} |"
        for j, (r2, n2, v2) in enumerate(students_with_embeddings):
            if v1.size == v2.size:
                sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            else:
                sim = 0.0
            row.append(float(sim))
            
            # Color-code: high similarity between different people is BAD
            if i == j:
                row_str += f"  {'1.000':>12}"
            elif sim >= 0.55:
                row_str += f"  {'⚠️'+f'{sim:.3f}':>12}"  # Warning: too similar
            else:
                row_str += f"  {f'{sim:.3f}':>12}"
        
        similarity_matrix.append(row)
        print(row_str)
    
    # 6. Summary diagnosis
    print(f"\n{'=' * 70}")
    print("📋 DIAGNOSIS SUMMARY")
    print(f"{'=' * 70}")
    
    # Find max off-diagonal similarity
    max_off_diag = 0
    max_pair = ("", "")
    for i in range(len(similarity_matrix)):
        for j in range(len(similarity_matrix)):
            if i != j and similarity_matrix[i][j] > max_off_diag:
                max_off_diag = similarity_matrix[i][j]
                max_pair = (students_with_embeddings[i][1], students_with_embeddings[j][1])
    
    if max_off_diag >= 0.55:
        print(f"⚠️  HIGH inter-student similarity detected: {max_off_diag:.3f}")
        print(f"   Between: {max_pair[0]} and {max_pair[1]}")
        print(f"   This means the model sees these people as very similar.")
        print(f"   Consider re-enrolling with better quality photos.")
    
    if len(students_without_embeddings) > 0:
        print(f"⚠️  {len(students_without_embeddings)} student(s) have no embeddings - they can NEVER be recognized")
    
    current_threshold = 0.40
    print(f"\n🎯 Current SIMILARITY_THRESHOLD: {current_threshold}")
    print(f"   Recommended for ArcFace: 0.60 - 0.68")
    if current_threshold < 0.55:
        print(f"   🚨 YOUR THRESHOLD IS TOO LOW! Random faces will match above {current_threshold}")
        print(f"   This is the MAIN reason everyone is recognized as the same person.")
    
    print(f"\n💡 RECOMMENDED FIXES:")
    print(f"   1. Set SIMILARITY_THRESHOLD=0.62 in camera_service/.env")
    print(f"   2. Re-enroll students with clear, well-lit frontal photos")
    print(f"   3. Use the multi-image enrollment (4 photos) for better accuracy")
    print()

if __name__ == "__main__":
    main()
