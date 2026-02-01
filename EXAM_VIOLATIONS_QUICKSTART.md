# 🚀 Quick Start - Exam Violations Report

## Step 1: Start All Services
```bash
# Terminal 1: Backend
cd backend
./start_backend_venv.bat

# Terminal 2: Frontend  
cd frontend
./start_frontend.bat

# Terminal 3: Camera Service
cd camera_service
./start_camera_service_venv.bat
```

## Step 2: Access Frontend
Open browser: `http://localhost:3000`

## Step 3: Create Exam Schedule
1. Go to **🕐 Timetable** section
2. Add new timetable with:
   - Day: Saturday
   - Start time: 12:20
   - End time: 12:40
   - Subject: S001 or S002
   - Check "✓ Exam Time Slot"
3. Save timetable

## Step 4: Set Camera to Exam Mode
1. Go to **🎥 Cameras** section
2. Click **Exam Mode** button for your camera
3. Camera is now ready to detect phones

## Step 5: Test Phone Detection
1. Go to **📱 Exam Violations** 
2. During scheduled exam time (12:20-12:40):
   - Show your phone to camera
   - Even partial phone visible will trigger detection
3. Check violation dashboard
4. See:
   - When phone was detected (timestamp)
   - Teacher on duty
   - Which exam room
   - Which subject
   - Confidence percentage

## What You'll See in Dashboard

### Statistics (Top Cards)
- **Total Violations**: 1
- **Today's Violations**: 1 
- **Students Caught**: 1
- **Invigilators**: 1

### Violation Table Columns
| Timestamp | Student | Teacher | Subject | Room | Confidence | Status |
|-----------|---------|---------|---------|------|------------|--------|
| 14:30:15  | aditya  | T001    | S001    | Cam1 | 95%       | 🚨ALERT|

### Detailed View
- Student name and ID
- Invigilator (teacher) name
- Exam room (camera location)
- Subject being examined
- Confidence percentage (95%)
- Notes about detection

## Features Ready to Use

✅ **Real-time Phone Detection**
- Shows immediately when phone detected
- Works with partial phone visibility

✅ **Teacher/Invigilator Tracking**
- See which teacher was on duty
- Know who needs to be notified

✅ **Room/Camera Identification**
- Know which exam room the violation occurred in
- Multi-camera support

✅ **Filtering Options**
- Filter by today's violations
- Filter by specific teacher
- Filter by specific room/camera

✅ **Detailed Records**
- Timestamp of detection
- Confidence level of detection
- Duration of phone visibility
- Notes about incident

## 🎯 Next Steps

1. **Deploy in Real Exam**
   - Set exam time in timetable
   - Switch camera to EXAM mode
   - Dashboard will auto-populate with detections

2. **Configure Email Alerts** (Optional)
   - Set SMTP environment variables
   - Invigilators get instant email alerts

3. **Review Violations**
   - Check dashboard after exam
   - Take appropriate action
   - Archive records for documentation

## 💡 Tips

- **Instant Detection**: Phone must be just visible (edge/corner counts)
- **Confidence**: 95%+ means very certain, 30%+ means possible detection
- **Check Often**: Dashboard updates in real-time
- **Filter by Teacher**: Assign blame/responsibility easily
- **Filter by Room**: Identify problem classrooms

---

**Ready to catch cheating? Go to 📱 Exam Violations now!**
