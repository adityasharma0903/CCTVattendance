import requests
r = requests.get('http://localhost:8000/api/students', timeout=5)
students = r.json()
print(f"Total students: {len(students)}")
for s in students:
    name = s.get("name", "?")
    roll = s.get("roll_number", "?")
    has_emb = "YES" if s.get("embedding") else "NO"
    emb_len = len(s["embedding"]) if s.get("embedding") else 0
    print(f"  {name} ({roll}) - Embedding: {has_emb} (dim={emb_len})")
