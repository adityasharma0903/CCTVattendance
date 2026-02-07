# Pinecone Setup Guide

## Overview
This system now uses **Pinecone** as a cloud-hosted vector database instead of FAISS. Pinecone provides:
- ✅ Managed cloud vector search (no local index maintenance)
- ✅ High-speed similarity search (O(1) lookup)
- ✅ Scalability for 1000s of students
- ✅ Real-time index updates
- ✅ Full redundancy & backup

## Architecture Flow

```
CCTV Camera
   ↓
RetinaFace (Detection)
   ↓
DeepSORT (Tracking)
   ↓
ArcFace (Embedding Generation)
   ↓
Pinecone (Cloud Vector Search)  ← Push embeddings during enrollment
   ↓                              ← Query during attendance
MongoDB (Attendance Records)
```

---

## Step 1: Create Pinecone Account & API Key

1. **Go to** [Pinecone Console](https://www.pinecone.io/)
2. **Sign up** for free account
3. **Navigate to** API Keys section
4. **Copy** your API Key (looks like: `pcsk_xxx...`)
5. **Note** your Environment (default: `us-east-1-aws`)

---

## Step 2: Configure Environment Variables

### Backend (.env file)

Create or update `backend/.env`:

```bash
# Pinecone Configuration
PINECONE_ENABLED=1
PINECONE_API_KEY=pcsk_your_api_key_here
PINECONE_INDEX_NAME=face-recognition
PINECONE_ENVIRONMENT=us-east-1-aws

# ... other existing configs ...
```

### Camera Service

Create or update `camera_service/.env`:

```bash
# Pinecone Configuration
PINECONE_ENABLED=1
PINECONE_API_KEY=pcsk_your_api_key_here
PINECONE_INDEX_NAME=face-recognition
PINECONE_ENVIRONMENT=us-east-1-aws

# Tracking & Detection
TRACKING_ENABLED=1
TRACK_MIN_SECONDS=3.0
TRACK_MIN_HITS=3

# ... other existing configs ...
```

---

## Step 3: Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Camera Service
cd ../camera_service
pip install -r requirements.txt
```

Verify Pinecone installation:
```bash
python -c "import pinecone; print('✅ Pinecone installed')"
```

---

## Step 4: Start Services

### Terminal 1: Backend API
```bash
cd backend
python main.py
```

**Expected logs:**
```
✅ Pinecone initialized: face-recognition
📂 Loading students from MongoDB...
✅ Loaded N students from MongoDB
```

### Terminal 2: Camera Service
```bash
cd camera_service
python attendance_service.py
```

**Expected logs:**
```
✅ Pinecone initialized: face-recognition
✅ Loaded N students from MongoDB (via API)
✨ DeepSORT Tracker initialized
```

---

## Step 5: Enroll Student (Auto-pushes to Pinecone)

When you upload a 4-photo enrollment via frontend:

1. **Backend processes** 4 photos → generates averaged embedding
2. **Pinecone receives** embedding vector (512 float32 values)
3. **Embedding indexed** under student's roll_number as vector ID
4. **MongoDB stores** embeddings + photo URLs + metadata

### Frontend Enrollment Flow
```
User uploads 4 photos (front/left/right/far)
         ↓
Backend: compute ArcFace embeddings
         ↓
Backend: average 4 embeddings
         ↓
Pinecone: upsert(vector_id=roll_number, vector=averaged_embedding)
         ↓
MongoDB: save student_data + embedding + image_urls
         ↓
✅ Student enrolled (searchable in both MongoDB & Pinecone)
```

---

## Step 6: Test Attendance

1. **Open camera feed** in camera service
2. **Student appears in frame**
3. **System:**
   - Detects face via RetinaFace
   - Generates 512-dim ArcFace embedding
   - Queries Pinecone for best match (cosine similarity)
   - Returns student name + similarity score
   - Validates via DeepSORT tracking
   - Marks attendance if all conditions met

**Expected log:**
```
✅ Detected face in frame
🔍 Pinecone search returned: roll_ECE001, similarity=0.92
👤 DeepSORT track #5 matched to ECE001 (John Doe)
✓ Track visible: 3.2s, matches: 5
✅ Attendance marked for ECE001 - John Doe
```

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `PINECONE_ENABLED` | `1` | Enable/disable Pinecone (0=disabled, 1=enabled) |
| `PINECONE_API_KEY` | `` | Your Pinecone API key (required!) |
| `PINECONE_INDEX_NAME` | `face-recognition` | Index name in Pinecone |
| `PINECONE_ENVIRONMENT` | `us-east-1-aws` | Pinecone region (us-east-1-aws, us-west-2-aws, eu-west-1-aws, etc.) |

---

## Fallback Behavior

If Pinecone is unavailable:

1. **Enrollment still succeeds** (MongoDB = source of truth)
2. **Attendance uses brute-force search** on local embeddings (slower but works)
3. **Automatic fallback** - no manual intervention needed

**Configure fallback:**
```bash
# Disable Pinecone (uses only MongoDB + local search)
PINECONE_ENABLED=0
```

---

## Pinecone Index Structure

**Index Details:**
- **Name:** `face-recognition`
- **Dimension:** 512 (ArcFace embedding size)
- **Metric:** `cosine` (cosine similarity for face matching)
- **Namespace:** `face-recognition`

**Vector ID Format:**
- `ECE001` (roll_number as ID)
- Metadata: Student name, batch, email (optional, not stored in Pinecone for speed)

---

## Troubleshooting

### ❌ "Failed to initialize Pinecone"

**Check:**
```bash
# 1. API Key is set
echo $PINECONE_API_KEY

# 2. API Key is valid (no typos, not expired)

# 3. Pinecone installed
python -c "import pinecone; print(pinecone.__version__)"
```

### ❌ Enrollment succeeds but Pinecone shows 0 vectors

**Issue:** Pinecone push failed silently

**Solution:**
1. Check logs for `❌ Failed to push embedding to Pinecone`
2. Verify index exists: `pinecone.list_indexes()`
3. Try manual upsert:
```python
import pinecone
pinecone.init(api_key="...", environment="...")
index = pinecone.Index("face-recognition")
index.upsert(vectors=[("TEST", [0.1]*512)], namespace="face-recognition")
```

### ❌ Attendance slow (taking >5 seconds)

**Check:**
- Pinecone network latency (check Pinecone dashboard)
- If slow, fallback to local search is OK (still <1s for 100 students)

---

## Monitoring

### Check Pinecone Index Status

```bash
# Python script
import pinecone

pinecone.init(api_key="...", environment="...")
index = pinecone.Index("face-recognition")

# Get index stats
stats = index.describe_index_stats()
print(f"Vectors indexed: {stats['total_vector_count']}")
print(f"Namespaces: {stats['namespaces']}")
```

### Logs to Monitor

**Backend:**
```
✅ Pinecone initialized: face-recognition
✅ Pushed embedding to Pinecone for ECE001
❌ Failed to push embedding to Pinecone: [error]
```

**Camera Service:**
✅ Pinecone initialized: face-recognition
🔍 Pinecone search returned: roll_ECE001, similarity=0.92
❌ Pinecone search failed: [error], falling back to local search
```

---

## Performance Expectations

| Operation | Time | Notes |
|-----------|------|-------|
| Pinecone query | 5-50ms | Cosine similarity on 512-dim vectors |
| Fallback (brute-force) | <500ms | For 100 students on CPU |
| Enrollment (4 photos) | 10-30s | Face detection + Pinecone push |
| Attendance marking | 1-3s | Detection + tracking + query + DB write |

---

## Advanced: Delete Student (Remove from Pinecone)

When deleting a student:

```python
# This is done automatically in the backend
if pinecone_index is not None:
    pinecone_index.delete(ids=[roll_number], namespace="face-recognition")
```

---

## Summary

✅ **Setup Complete!**

Your system now uses:
- **Pinecone** for cloud-hosted vector search (scalable, managed)
- **MongoDB** for student data & attendance records (persistent)
- **Cloudinary** for image storage (distributed, CDN)
- **RetinaFace + ArcFace** for robust face detection & recognition
- **DeepSORT** for tracking to prevent duplicate marks

**Ready to enroll students and run attendance!**
