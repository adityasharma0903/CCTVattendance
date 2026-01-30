# 📸 Face Recognition Attendance System - Complete Setup Guide

## 🎯 Project Overview

A complete full-stack face recognition attendance system with:
- ✅ **Admin Website** (React.js) - Manage all master data
- ✅ **Backend API** (Python FastAPI) - REST API for all operations
- ✅ **Camera Service** (Python) - Automatic attendance marking
- ✅ **JSON-based Database** - No external database needed
- ✅ **Automated Scheduler** - Time-based attendance trigger

---

## 📁 Project Structure

```
FACE RECOG/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Main API server
│   ├── requirements.txt        # Python dependencies
│   └── run.sh                 # Script to run server
│
├── frontend/                   # React Admin Dashboard
│   ├── src/
│   │   ├── App.js            # Main app component
│   │   ├── components/        # React components
│   │   │   ├── Dashboard.js
│   │   │   ├── StudentManager.js
│   │   │   ├── BatchManager.js
│   │   │   ├── TeacherManager.js
│   │   │   ├── SubjectManager.js
│   │   │   ├── CameraManager.js
│   │   │   ├── TimetableManager.js
│   │   │   └── AttendanceReport.js
│   │   └── styles/
│   │       └── App.css        # Styling
│   └── package.json           # Dependencies
│
├── camera_service/            # Face Recognition Service
│   ├── attendance_service.py  # Main camera service
│   └── requirements.txt        # Python dependencies
│
├── data/                       # JSON Data Files
│   ├── batches.json
│   ├── teachers.json
│   ├── subjects.json
│   ├── cameras.json
│   ├── timetable.json
│   ├── camera_schedule.json
│   └── attendance.json
│
└── README.md                   # This file
```

---

## 🚀 Installation Steps

### **Step 1: Install Backend**

```bash
cd backend
pip install -r requirements.txt
```

### **Step 2: Install Frontend**

```bash
cd frontend
npm install
```

### **Step 3: Install Camera Service**

```bash
cd camera_service
pip install -r requirements.txt
```

---

## 🎮 Running the System

### **Terminal 1 - Start Backend API**

```bash
cd backend
python main.py
```

Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**API Documentation available at:** `http://localhost:8000/docs`

### **Terminal 2 - Start Frontend (Admin Website)**

```bash
cd frontend
npm start
```

Output:
```
Compiled successfully!
Local: http://localhost:3000
```

**Access website at:** `http://localhost:3000`

### **Terminal 3 - Start Camera Service**

```bash
cd camera_service
python attendance_service.py
```

Output:
```
✅ Initialized camera: Classroom A - Main
✅ Initialized camera: Classroom B - Main
🚀 Starting Attendance Scheduler...
✅ Scheduler started successfully
```

---

## 📊 Database Structure (JSON Files)

### **batches.json**
```json
{
  "batches": [
    {
      "batch_id": "B001",
      "batch_name": "CSE Batch A",
      "semester": "4",
      "total_students": 0
    }
  ]
}
```

### **students_database.json** (from your iotproject)
```json
{
  "2410990250": {
    "name": "aditya",
    "roll_number": "2410990250",
    "batch_id": "B001",
    "email": "aditya@college.edu",
    "image_path": "student_images/aditya.jpg",
    "embedding": [...],
    "added_date": "2024-01-30T10:00:00"
  }
}
```

### **timetable.json**
```json
{
  "timetable": [
    {
      "timetable_id": "TT001",
      "batch_id": "B001",
      "day": "Monday",
      "period": 1,
      "start_time": "09:00",
      "end_time": "10:30",
      "subject_id": "S001",
      "teacher_id": "T001"
    }
  ]
}
```

### **cameras.json**
```json
{
  "cameras": [
    {
      "camera_id": "CAM_001",
      "camera_name": "Classroom A - Main",
      "location": "Room 101",
      "ip_address": "192.168.1.100",
      "batch_id": "B001",
      "is_active": true
    }
  ]
}
```

### **camera_schedule.json**
```json
{
  "camera_schedule": [
    {
      "schedule_id": "CS001",
      "camera_id": "CAM_001",
      "timetable_id": "TT001",
      "is_active": true
    }
  ]
}
```

---

## 🌐 Frontend Features

### **Dashboard**
- Summary statistics (students, batches, teachers, cameras, attendance records)

### **Student Management**
- Add/View/Delete students
- Assign students to batches
- Manage student information

### **Batch Management**
- Create new batches/classes
- Assign semester information

### **Teacher Management**
- Add teachers
- Store teacher contact information

### **Subject Management**
- Create subjects
- Assign teachers to subjects

### **Camera Configuration**
- Add cameras
- Assign cameras to batches
- Enable/Disable cameras

### **Timetable Schedule**
- Create day-wise timetables
- Set period timings
- Assign subjects and teachers
- Link cameras to schedules

### **Attendance Reports**
- View attendance records by batch
- See attendance status (PRESENT, ABSENT, LATE)
- View confidence scores
- Generate attendance statistics

---

## 🎥 Camera Service - How It Works

### **Flow:**

```
1. Check Current Time
   ↓
2. Check Timetable for Active Period
   (Is there a class now for this camera?)
   ↓
3. Capture Video from Camera
   ↓
4. Detect Faces (OpenCV)
   ↓
5. Compare with Student Database (DeepFace)
   ↓
6. If Match Found:
   - Determine Status (PRESENT, LATE)
   - Send to Backend API
   - Store in attendance.json
   - Update Website in Real-Time
   ↓
7. Continue Recording Until Class Ends
```

### **Configuration:**

Edit `camera_service/attendance_service.py`:

```python
# Model and threshold settings
MODEL = "ArcFace"
SIMILARITY_THRESHOLD = 0.5  # 0-1 (higher = stricter matching)
DETECTION_INTERVAL = 2.0    # Seconds between face checks
ATTENDANCE_COOLDOWN = 300   # 5 minutes (prevent duplicate marking)
```

---

## 🔌 API Endpoints

### **Student Endpoints**
- `GET /api/students` - Get all students
- `GET /api/students/{batch_id}` - Get batch students
- `POST /api/students` - Add new student
- `PUT /api/students/{roll_number}` - Update student
- `DELETE /api/students/{roll_number}` - Delete student

### **Attendance Endpoints**
- `GET /api/attendance` - Get all attendance
- `GET /api/attendance/{batch_id}` - Get batch attendance
- `GET /api/attendance/student/{roll_number}` - Get student attendance
- `POST /api/attendance` - Mark attendance
- `GET /api/attendance/report/{batch_id}` - Get attendance report

### **Batch Endpoints**
- `GET /api/batches` - Get all batches
- `POST /api/batches` - Add new batch

### **Teacher Endpoints**
- `GET /api/teachers` - Get all teachers
- `POST /api/teachers` - Add new teacher

### **Subject Endpoints**
- `GET /api/subjects` - Get all subjects
- `POST /api/subjects` - Add new subject

### **Camera Endpoints**
- `GET /api/cameras` - Get all cameras
- `GET /api/cameras/{batch_id}` - Get batch cameras
- `POST /api/cameras` - Add new camera

### **Timetable Endpoints**
- `GET /api/timetable` - Get all timetables
- `GET /api/timetable/{batch_id}` - Get batch timetable
- `POST /api/timetable` - Add timetable entry

### **Camera Schedule Endpoints**
- `GET /api/camera-schedule` - Get all schedules
- `GET /api/camera-schedule/{camera_id}` - Get camera schedule
- `POST /api/camera-schedule` - Add camera schedule

### **Dashboard Endpoints**
- `GET /api/dashboard/summary` - Get dashboard summary
- `GET /api/attendance/report/{batch_id}` - Get attendance report

---

## 🔧 Configuration & Customization

### **1. Change Similarity Threshold**

Edit `camera_service/attendance_service.py`:

```python
SIMILARITY_THRESHOLD = 0.5  # Range: 0-1
# Higher value = stricter matching (fewer false positives)
# Lower value = lenient matching (more matches but more false positives)
```

### **2. Add New Camera**

1. Open **Website** → **Cameras**
2. Click **+ Add New Camera**
3. Fill in:
   - Camera ID (e.g., CAM_003)
   - Camera Name
   - Location
   - IP Address
   - Select Batch
4. Click **Save Camera**

### **3. Assign Camera to Timetable**

1. Go to **Timetable** → Create timetable entry
2. Go to **Camera Schedule** (API or JSON)
3. Link camera to timetable entry

### **4. Add Student with Face Encoding**

Option A: **Using Website**
1. Click **Students** → **+ Add New Student**
2. Fill roll number, name, batch
3. Provide image path

Option B: **Using Setup Script** (from iotproject)
```bash
cd iotproject
python setup_students.py
```

---

## 🎬 Setting Up Face Recognition

### **Step 1: Prepare Student Images**

```
frontend/
└── public/
    └── student_images/
        ├── 2410990250.jpg  (Clear frontal face)
        ├── 2410990251.jpg
        └── ...
```

### **Step 2: Register Students**

```bash
cd iotproject
python setup_students.py
```

**Follow prompts:**
```
Enter Roll Number: 2410990250
Enter Student Name: Aditya
Enter image path: student_images/aditya.jpg
```

This will:
- Load the image
- Extract face embedding using DeepFace
- Save to `students_database.json`

### **Step 3: Verify in Website**

- Go to **Students** page
- Should see all registered students

---

## 📋 Typical Usage Flow

### **Day 1: Setup (Administrator)**

1. **Add Batches**
   - CSE Batch A (Semester 4)
   - CSE Batch B (Semester 4)

2. **Add Teachers**
   - Dr. Sharma
   - Prof. Verma

3. **Add Subjects**
   - Data Structures (Dr. Sharma)
   - Database Management (Prof. Verma)

4. **Add Cameras**
   - Classroom A Camera
   - Classroom B Camera

5. **Add Students**
   - Roll numbers, names, images
   - Assign to batches

6. **Create Timetable**
   - Monday 9-10:30 AM: Data Structures (Batch A, Room 101)
   - Monday 10:30-12 PM: Database (Batch A, Room 101)
   - Tuesday 9-10:30 AM: Web Dev (Batch B, Room 102)

7. **Assign Cameras to Schedule**
   - Classroom A Camera → Data Structures period
   - Classroom B Camera → Web Dev period

### **Day 2: Attendance Taking**

1. **Start System**
   - Backend API running
   - Camera service running
   - Website open

2. **Class Starts (9:00 AM)**
   - Camera automatically activates
   - Starts detecting faces
   - Marks attendance in real-time

3. **View Attendance**
   - Go to **Attendance Report**
   - Select batch
   - See live updates as students arrive

---

## 🐛 Troubleshooting

### **Camera not detecting faces**

- Check image quality (clear frontal faces)
- Increase exposure/lighting
- Lower similarity threshold
- Check logs in camera service terminal

### **Attendance not marking**

- Verify timetable is set correctly
- Check camera schedule is enabled
- Ensure backend API is running
- Check `attendance.json` for records

### **Frontend can't connect to API**

- Ensure backend is running on port 8000
- Check for CORS errors in browser console
- Verify API URL in components

### **DeepFace model download issues**

```bash
# Install manually
python -c "from deepface import DeepFace; DeepFace.represent([], model_name='ArcFace')"
```

---

## 📱 Mobile Access

Access website from any device on same network:

1. Get your computer IP:
```bash
ipconfig  # Windows
ifconfig  # Mac/Linux
```

2. Access from mobile:
```
http://<YOUR_IP>:3000
```

---

## 🔒 Security Notes

- This is a basic system (no authentication)
- Use in controlled environments only
- Add authentication before production use
- Store sensitive data properly
- Use HTTPS in production

---

## 📈 Scaling Tips

1. **Multiple Cameras**: Add more cameras to different batches
2. **Database Optimization**: Currently using JSON (suitable for < 1000 students)
3. **Real Database**: Replace JSON with PostgreSQL/MongoDB for large scale
4. **Cloud Deployment**: Deploy to AWS/Azure for remote access

---

## 🤝 Support & Customization

For modifications:
- Backend: FastAPI documentation
- Frontend: React documentation
- Camera: OpenCV, DeepFace documentation

---

## ✅ Checklist Before Deployment

- [ ] All students registered with face images
- [ ] Timetable configured
- [ ] Cameras configured
- [ ] Camera schedules linked
- [ ] Tested attendance marking
- [ ] Verified database JSON files
- [ ] Tested website functionality

---

**Happy Attendance Tracking! 🎉**
