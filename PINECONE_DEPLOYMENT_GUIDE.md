# 🚀 Pinecone Deployment Guide

## System Architecture

```
📹 CCTV
  ↓
🔍 RetinaFace (Detection)
  ↓
👥 DeepSORT (Tracking)
  ↓
🧠 ArcFace (512-dim Embeddings)
  ↓
☁️ PINECONE (Cloud Vector Search) ← NEW!
  ↓
✅ Attendance Logic (3sec + 3frame + liveness)
  ↓
💾 MongoDB (Records)
```

---

## ✅ What's Implemented

| Component | Technology | Status |
|-----------|-----------|--------|
| Face Detection | RetinaFace + MTCNN fallback | ✅ Done |
| Face Tracking | DeepSORT | ✅ Done |
| Embedding | ArcFace (512-dim) | ✅ Done |
| Vector Search | **Pinecone Cloud** | ✅ Done |
| Enrollment | 4 labeled photos + avg embedding | ✅ Done |
| Attendance | Track-based marking (3sec+3frame+liveness) | ✅ Done |
| MongoDB | Record storage + fallback search | ✅ Done |
| Cloudinary | Image backup | ✅ Done |

---

## 🔧 Installation Steps

### Step 1: Get Pinecone API Key

1. Go to https://www.pinecone.io/
2. Sign up (FREE tier available)
3. Go to **API Keys** section in dashboard
4. **Copy** your API key (format: `pcsk_xxx...`)
5. **Note** your **Environment** (default: `us-east-1-aws`)

### Step 2: Update Environment Variables

**File: `backend/.env`**
```bash
PINECONE_ENABLED=1
PINECONE_API_KEY=pcsk_your_key_here
PINECONE_INDEX_NAME=face-recognition
PINECONE_ENVIRONMENT=us-east-1-aws

# Existing configs (keep these)
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
MONGO_URL=mongodb://localhost:27017
```

**File: `camera_service/.env`**
```bash
PINECONE_ENABLED=1
PINECONE_API_KEY=pcsk_your_key_here
PINECONE_INDEX_NAME=face-recognition
PINECONE_ENVIRONMENT=us-east-1-aws

# Tracking settings
TRACKING_ENABLED=1
TRACK_MIN_SECONDS=3.0
TRACK_MIN_HITS=3

# Detection settings
FRAME_WIDTH=1280
FRAME_HEIGHT=720
SIMILARITY_THRESHOLD=0.45
```

### Step 3: Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Camera Service
cd ../camera_service
pip install -r requirements.txt
```

**Verify Pinecone install:**
```bash
python -c "import pinecone; print('✅ Pinecone ready')"
```

### Step 4: Start MongoDB (if not running)

```bash
# Option 1: Docker
docker run -d -p 27017:27017 mongo

# Option 2: Local MongoDB
mongod
```

### Step 5: Start Backend API

```bash
cd backend
python main.py
```

**Expected output:**
```
✅ Pinecone initialized: face-recognition
📂 Loading students from MongoDB...
✅ Loaded N students from MongoDB
🚀 API running on http://localhost:8000
```

### Step 6: Start Camera Service

**Terminal 2:**
```bash
cd camera_service
python attendance_service.py
```

**Expected output:**
```
✅ Pinecone initialized: face-recognition
✅ Loaded N students from MongoDB (via API)
✨ DeepSORT Tracker initialized
🎥 Camera stream starting...
```

### Step 7: Open Frontend

```bash
cd frontend
npm start
```

Opens at http://localhost:3000

---

## 📝 Enrollment Test

### Via Frontend:

1. Navigate to **Student Manager** tab
2. Fill student details:
   - Roll Number: `ECE001`
   - Name: `John Doe`
   - Batch: `ECE001`
3. **Upload 4 photos**:
   - **Front:** Face looking straight at camera
   - **Left:** Face turned 45° left
   - **Right:** Face turned 45° right
   - **Far:** Face from 3-4 feet distance
4. Click **Submit**

### Expected Logs:

**Backend:**
```
✅ Student John Doe added to MongoDB with multi-image embeddings
✅ Pushed embedding to Pinecone for ECE001
```

**Verification:**
- Check [Pinecone Dashboard](https://app.pinecone.io) → Index Details
- Should show **1 vector** indexed

---

## 🎯 Attendance Test

### Step 1: Register 3-5 test students
- Use different people for best results
- Each needs 4 labeled photos

### Step 2: Run camera service
```bash
python camera_service.py
```

### Step 3: Open camera feed UI
```bash
# In another terminal or browser
python camera_ui.py  # or access from frontend dashboard
```

### Step 4: Test attendance

Position student in frame:

**Expected flow:**
```
[Frame] → 🔍 Detected face in frame
        → 🧠 Computed embedding
        → 🔎 Querying Pinecone...
        → ✅ Pinecone returned: roll_ECE001, similarity=0.92
        → 👥 DeepSORT track #1 matched to ECE001
        → ⏱️ Track visible: 0.8s (need 3.0s)
        → ⏱️ Track visible: 1.5s
        → ⏱️ Track visible: 3.2s ← ✓ Time met!
        → 🔄 Matched 4 frames ← ✓ Frame count met!
        → ✨ Liveness check: movement detected ← ✓ Liveness OK!
        → ✅ Attendance marked for ECE001 - John Doe
        → 📊 Dashboard updated
        → 💾 MongoDB recorded
```

### Expected Logs:
```
✅ Detected face in frame
🔍 Pinecone search returned: roll_ECE001, similarity=0.92
👤 DeepSORT track #1: ECE001 (John Doe)
✓ Track visible: 3.2s, matches: 4
✅ Attendance marked for ECE001 - John Doe
```

---

## ⚙️ Configuration Tuning

### For Fast Marking (< 2 seconds)
```bash
TRACK_MIN_SECONDS=2.0      # Reduce to 2 sec
TRACK_MIN_HITS=2           # Reduce to 2 frames
LIVENESS_ENABLED=0         # Disable liveness (faster)
```

### For Strict Marking (reduce false positives)
```bash
TRACK_MIN_SECONDS=4.0      # Increase to 4 sec
TRACK_MIN_HITS=5           # Increase to 5 frames
SIMILARITY_THRESHOLD=0.50  # Raise threshold
LIVENESS_MIN_MOVEMENT_PX=15.0  # Stricter movement
```

### For Distant Faces
```bash
FACE_DET_UPSCALE=2.0       # Increase upscaling
FRAME_HEIGHT=1080          # Increase resolution
FRAME_WIDTH=1920
```

---

## 🔍 Monitoring & Logs

### Check Pinecone Status

```bash
# Python quick check
python << 'EOF'
import pinecone

pinecone.init(
    api_key="your_api_key",
    environment="us-east-1-aws"
)

index = pinecone.Index("face-recognition")
stats = index.describe_index_stats()

print(f"✅ Vectors indexed: {stats['total_vector_count']}")
print(f"📊 Namespaces: {list(stats['namespaces'].keys())}")
EOF
```

### Backend Logs
```bash
tail -f backend.log
```

**Look for:**
- `✅ Pinecone initialized`
- `✅ Pushed embedding to Pinecone`
- `❌ Failed to push` → troubleshoot API key

### Camera Service Logs
```bash
tail -f camera.log
```

**Look for:**
- `✅ Pinecone initialized`
- `🔍 Pinecone search returned`
- `✅ Attendance marked`

---

## 🆘 Troubleshooting

### ❌ "Pinecone not enabled or API key missing"

**Check:**
```bash
# Verify .env file exists
ls backend/.env camera_service/.env

# Verify API key is set
echo $PINECONE_API_KEY

# Expected: pcsk_xxx...
```

**Fix:**
1. Add `.env` file if missing (copy from `.env.example`)
2. Add `PINECONE_API_KEY` value to `.env`
3. Restart service

---

### ❌ "Failed to create index in Pinecone"

**Cause:** API key invalid or quota exceeded

**Fix:**
1. Verify API key in [Pinecone console](https://app.pinecone.io)
2. Check quota: monthly free tier = 1M operations
3. Regenerate API key if needed

---

### ❌ Enrollment succeeds but no vector in Pinecone

**Logs show:** `❌ Failed to push embedding to Pinecone`

**Diagnose:**
```python
# Test API connection
import pinecone

try:
    pinecone.init(api_key="your_key", environment="us-east-1-aws")
    idx = pinecone.Index("face-recognition")
    print("✅ Connected to Pinecone")
except Exception as e:
    print(f"❌ Error: {e}")
```

**Try manual upsert:**
```python
# Push test vector
idx.upsert(
    vectors=[("TEST_001", [0.1]*512)],
    namespace="face-recognition"
)
print("✅ Test vector uploaded")
```

---

### ❌ Attendance not being marked

**Check in order:**

1. **Face detected?**
   ```bash
   # Look for: "Detected face in frame"
   ```
   - If NO: increase `FACE_DET_UPSCALE`

2. **Pinecone search working?**
   ```bash
   # Look for: "Pinecone search returned"
   ```
   - If NO: check API key + network

3. **Similarity above threshold?**
   ```bash
   # Look for: "similarity=0.XX"
   # If < SIMILARITY_THRESHOLD: mark anyway
   ```
   - If NO: student not enrolled correctly

4. **Tracking requirements met?**
   ```bash
   # Look for: "Track visible: X.Xs, matches: N"
   # Need: >= TRACK_MIN_SECONDS + >= TRACK_MIN_HITS
   ```
   - If gap: reduce threshold or keep face in frame longer

5. **Liveness passed?**
   ```bash
   # Look for: "liveness OK" or "Liveness check failed"
   ```
   - If NO: move head slightly

---

### ❌ "Query timeout" / "Pinecone slow"

**Normal:** 30-50ms is OK (includes network)

**If >1 second:**
1. Check Pinecone dashboard for latency
2. Try fallback mode:
   ```bash
   PINECONE_ENABLED=0  # Uses local search instead
   ```
3. Contact Pinecone support

---

## 📊 Database Verification

### Check MongoDB Records

```bash
# Connect to MongoDB
mongosh

# Browse database
use face_recognition_db
db.students.find()  # Show all students
db.students.findOne({roll_number: "ECE001"})  # Show one student
db.attendance.find()  # Show attendance records
db.attendance.find({roll_number: "ECE001"})  # Show one student's attendance
```

### Check Pinecone Index

```bash
# Via Python
import pinecone

pinecone.init(api_key="...", environment="...")
idx = pinecone.Index("face-recognition")

# Describe index
stats = idx.describe_index_stats()
print(f"Vectors: {stats['total_vector_count']}")

# Query test vector
test_vector = [0.1] * 512
results = idx.query(vector=test_vector, top_k=5, namespace="face-recognition")
print(results)
```

---

## 📈 Performance Checklist

After deployment, verify:

- [ ] Backend API responsive (`curl http://localhost:8000/api/health`)
- [ ] Pinecone initialization logged (`✅ Pinecone initialized`)
- [ ] Students load successfully (`✅ Loaded N students from MongoDB`)
- [ ] Enrollment push succeeds (`✅ Pushed embedding to Pinecone`)
- [ ] Face detection works (detects faces in camera)
- [ ] Pinecone search works (gets matches with similarity score)
- [ ] Attendance marks within 3-5 seconds
- [ ] MongoDB updates with attendance records
- [ ] Dashboard reflects updates in real-time

---

## 🎓 Viva Talking Points

### System Highlights:

1. **Pinecone Cloud Vector Database**
   - Managed service (no index maintenance)
   - Scales to 1000s of students
   - Fast cosine similarity search
   - Reliable 99.95% SLA

2. **Multi-Angle Enrollment (4 photos)**
   - Front/left/right/far angles
   - Averaged embeddings = robust to lighting/angles
   - Better than single frontal photo

3. **DeepSORT Tracking**
   - Tracks unique students across frames
   - Prevents duplicate marking
   - Enables 100+ students in 5-10 minutes

4. **Anti-Spoofing (Liveness Check)**
   - Detects head movement
   - Prevents photo/video spoofing
   - 3-second visibility requirement

5. **Fallback Resilience**
   - If Pinecone unavailable: uses local brute-force
   - If CCTV fails: graceful shutdown
   - No single point of failure

---

## 🌍 Production Considerations

### For Large Deployments (100+ cameras):

```bash
# Use environment-specific configs
PINECONE_ENVIRONMENT=us-east-1-aws  # Choose closest region
PINECONE_API_KEY=xxx  # Use Pinecone Premium plan

# Load balancing
BACKEND_REPLICAS=3
CAMERA_SERVICE_REPLICAS=5

# Caching
REDIS_CACHE=redis://localhost:6379
CACHE_TTL=300  # 5 min cache for embeddings
```

### Security Hardening:

```bash
# API security
AUTH_TOKEN=secret_jwt_token
CORS_ORIGINS=https://yourdomain.com

# Data encryption
MONGODB_AUTH=username:password
MONGODB_SSL=true

# Audit logging
LOG_LEVEL=DEBUG
LOG_PATH=/secure/logs/
```

---

## 📞 Support

- **Pinecone Docs:** https://docs.pinecone.io/
- **Pinecone Dashboard:** https://app.pinecone.io/
- **System Issues:** Check logs in `backend.log` and `camera.log`

---

## ✅ Summary Checklist

**Before Going Live:**
- [ ] Pinecone account created + API key obtained
- [ ] All `.env` files updated with correct keys
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] MongoDB running and accessible
- [ ] Backend API starts without errors
- [ ] Camera service starts without errors
- [ ] At least 5 test students enrolled
- [ ] Attendance marking tested and verified
- [ ] Logs show `✅ Pinecone initialized` messages
- [ ] Pinecone dashboard shows vectors indexed

**Go!** 🎉
