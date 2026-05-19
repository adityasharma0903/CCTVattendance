"""Check cosine similarity between stored embeddings to diagnose giaaa issue"""
import requests
import numpy as np

r = requests.get('http://localhost:8000/api/students', timeout=5)
students = r.json()

embeddings = {}
for s in students:
    roll = s.get("roll_number", "?")
    name = s.get("name", "?")
    emb = s.get("embedding")
    if emb and isinstance(emb, list) and len(emb) > 0:
        vec = np.array(emb, dtype=np.float32)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm  # L2 normalize
        embeddings[f"{name} ({roll})"] = vec
        print(f"  {name} ({roll}): dim={vec.size}, norm={np.linalg.norm(vec):.4f}")
    else:
        print(f"  {name} ({roll}): NO EMBEDDING ❌")

print(f"\nTotal with embeddings: {len(embeddings)}")

# Check similarity between all pairs
if len(embeddings) >= 2:
    keys = list(embeddings.keys())
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            sim = float(np.dot(embeddings[keys[i]], embeddings[keys[j]]))
            print(f"\n  Similarity between {keys[i]} and {keys[j]}: {sim:.4f}")
            if sim > 0.7:
                print(f"  ⚠️  TOO SIMILAR! These embeddings might be from the same person or corrupted")
            elif sim > 0.5:
                print(f"  ⚠️  Moderately similar - could cause confusion")
            else:
                print(f"  ✅ Good separation - these are clearly different people")
