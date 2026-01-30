# 🏗️ System Architecture & Flow

## **System Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                    ADMIN DASHBOARD (Website)                    │
│                   http://localhost:3000                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Master Data Entry (Students, Teachers, Batches)       │  │
│  │ • Timetable Management (Day-wise Schedule)              │  │
│  │ • Camera Configuration                                  │  │
│  │ • Live Attendance View                                  │  │
│  │ • Attendance Reports & Analytics                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                          ↓
                  (React.js Frontend)
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│              BACKEND API (FastAPI)                              │
│             http://localhost:8000                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Student Management API                                │  │
│  │ • Batch Management API                                  │  │
│  │ • Teacher Management API                                │  │
│  │ • Subject Management API                                │  │
│  │ • Camera Configuration API                              │  │
│  │ • Timetable Management API                              │  │
│  │ • Attendance Recording API                              │  │
│  │ • Reports & Analytics API                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
            ↓                           ↑
  (REST API Calls)           (Attendance Data)
            ↓                           ↑
┌─────────────────────────────────────────────────────────────────┐
│              JSON DATA STORAGE                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • batches.json          • attendance.json                │  │
│  │ • students_database.json • subjects.json                 │  │
│  │ • teachers.json         • cameras.json                   │  │
│  │ • timetable.json        • camera_schedule.json           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                          ↑
                  (Read/Write Data)
                          ↑
┌─────────────────────────────────────────────────────────────────┐
│              CAMERA SERVICE (Scheduler)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Continuous Time Monitoring                            │  │
│  │ • Schedule Checking (Timetable)                          │  │
│  │ • Video Capture from Camera                             │  │
│  │ • Face Detection (OpenCV)                               │  │
│  │ • Face Recognition (DeepFace)                           │  │
│  │ • Attendance Marking & Storage                          │  │
│  │ • API Integration                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
           ↓                          ↑
    (Camera Feed)          (Student Database)
           ↓                          ↑
    ┌───────────┐            ┌───────────────┐
    │  CAMERA   │            │  STUDENT FACE │
    │  (CCTV)   │            │  ENCODINGS    │
    └───────────┘            └───────────────┘
```

---

## **Data Flow - Real-Time Attendance**

```
9:00 AM - CLASS STARTS
│
├─→ Camera Service Checks Time
│   └─→ Looks at timetable.json for 9:00 AM period
│       └─→ Found: Data Structures (Room 101, CAM_001)
│
├─→ Activates Camera
│   └─→ Starts video capture from camera
│
├─→ Continuous Face Detection
│   ├─→ Frame 1: No face detected
│   ├─→ Frame 2: Student enters
│   └─→ Frame 3: FACE DETECTED! ✅
│
├─→ Face Recognition
│   ├─→ Extract face encoding
│   ├─→ Compare with students_database.json
│   ├─→ Calculate similarity scores
│   └─→ MATCH FOUND: Aditya (Roll: 2410990250) ✅
│
├─→ Status Determination
│   ├─→ Get start_time from timetable
│   ├─→ Check current_time vs start_time
│   └─→ Status: PRESENT ✅ (on time)
│
├─→ Store Attendance
│   ├─→ Send to Backend API
│   ├─→ Backend stores in attendance.json
│   └─→ API Response: Success ✅
│
└─→ Website Updates
    └─→ Teacher sees "Aditya - PRESENT" in real-time ✅

10:30 AM - CLASS ENDS
│
└─→ Period ended
    └─→ Camera stops recording
        └─→ Waits for next period
```

---

## **File Organization**

```
Data Directory (data/)
│
├── batches.json
│   {
│     "batches": [
│       {
│         "batch_id": "B001",
│         "batch_name": "CSE Batch A",
│         "semester": "4"
│       }
│     ]
│   }
│
├── students_database.json (from iotproject/)
│   {
│     "2410990250": {
│       "name": "aditya",
│       "roll_number": "2410990250",
│       "batch_id": "B001",
│       "embedding": [...],  // Face vector
│       "image_path": "..."
│     }
│   }
│
├── teachers.json
│   {
│     "teachers": [
│       {
│         "teacher_id": "T001",
│         "name": "Dr. Sharma",
│         "email": "...",
│         "phone": "..."
│       }
│     ]
│   }
│
├── subjects.json
│   {
│     "subjects": [
│       {
│         "subject_id": "S001",
│         "subject_name": "Data Structures",
│         "teacher_id": "T001"
│       }
│     ]
│   }
│
├── cameras.json
│   {
│     "cameras": [
│       {
│         "camera_id": "CAM_001",
│         "camera_name": "Classroom A",
│         "batch_id": "B001",
│         "is_active": true
│       }
│     ]
│   }
│
├── timetable.json
│   {
│     "timetable": [
│       {
│         "timetable_id": "TT001",
│         "batch_id": "B001",
│         "day": "Monday",
│         "start_time": "09:00",
│         "end_time": "10:30",
│         "subject_id": "S001",
│         "teacher_id": "T001"
│       }
│     ]
│   }
│
├── camera_schedule.json
│   {
│     "camera_schedule": [
│       {
│         "schedule_id": "CS001",
│         "camera_id": "CAM_001",
│         "timetable_id": "TT001",
│         "is_active": true
│       }
│     ]
│   }
│
└── attendance.json
    {
      "attendance": [
        {
          "attendance_id": "UUID",
          "student_id": "STU_2410990250",
          "roll_number": "2410990250",
          "camera_id": "CAM_001",
          "timestamp": "2024-01-30T09:05:00",
          "subject_id": "S001",
          "batch_id": "B001",
          "status": "PRESENT",
          "confidence_score": 0.98
        }
      ]
    }
```

---

## **Component Interaction**

### **1. Website → Backend**

```
User Action: Add Student
    ↓
Website (React) sends POST request
    ↓
http://localhost:8000/api/students
{
  "roll_number": "2410990250",
  "name": "Aditya",
  "batch_id": "B001"
}
    ↓
Backend receives and processes
    ↓
Updates students_database.json
    ↓
Returns success response
    ↓
Website updates UI
```

### **2. Camera → Backend**

```
Camera detects face
    ↓
Matches with student database
    ↓
Creates attendance record
    ↓
Sends POST request to Backend
    ↓
http://localhost:8000/api/attendance
{
  "student_id": "STU_2410990250",
  "camera_id": "CAM_001",
  "status": "PRESENT",
  "confidence_score": 0.98
}
    ↓
Backend stores in attendance.json
    ↓
Website polls API (or WebSocket)
    ↓
Shows "Aditya - PRESENT" in real-time
```

### **3. Timetable → Camera**

```
Camera Service Scheduler
    ↓
Every minute, check current time
    ↓
Look in timetable.json
    ↓
Is there a class now for this camera?
    ↓
YES → Activate camera
NO  → Stay idle
    ↓
Once activated:
  • Load student embeddings
  • Start video capture
  • Detect & recognize faces
  • Mark attendance
```

---

## **Key Differences from Your Original Setup**

| Aspect | Original (iotproject) | New System |
|--------|----------------------|-----------|
| **Interface** | Console/Terminal | Web Dashboard (React) |
| **Data Storage** | JSON in iotproject/ | Centralized data/ folder |
| **API** | None (direct Python) | RESTful API (FastAPI) |
| **Communication** | Local only | HTTP API (network) |
| **Master Data** | Hardcoded | Website-managed |
| **Timetable** | Not implemented | Full day-wise schedule |
| **Camera Config** | Not implemented | Web interface |
| **Reports** | Basic logs | Detailed analytics |
| **Scalability** | Single camera | Multi-camera support |

---

## **REST API Request/Response Examples**

### **Get All Students**
```
GET http://localhost:8000/api/students

Response:
[
  {
    "student_id": "STU_2410990250",
    "roll_number": "2410990250",
    "name": "aditya",
    "batch_id": "B001",
    "email": "aditya@college.edu",
    "embedding": [...],
    "added_date": "2024-01-30T10:00:00"
  }
]
```

### **Mark Attendance**
```
POST http://localhost:8000/api/attendance

Request Body:
{
  "student_id": "STU_2410990250",
  "roll_number": "2410990250",
  "camera_id": "CAM_001",
  "timestamp": "2024-01-30T09:05:00",
  "subject_id": "S001",
  "batch_id": "B001",
  "status": "PRESENT",
  "confidence_score": 0.98
}

Response:
{
  "status": "success",
  "message": "Attendance marked successfully",
  "record": { ... }
}
```

### **Get Attendance Report**
```
GET http://localhost:8000/api/attendance/report/B001

Response:
{
  "batch_id": "B001",
  "total_records": 150,
  "present": 145,
  "absent": 3,
  "late": 2,
  "attendance_percentage": 96.67
}
```

---

## **Time-Based Automation Flow**

```
START CAMERA SERVICE
   ↓
Every 1 second:
   ├─→ Get current time & day
   │   Example: Monday, 09:15:00
   │
   ├─→ Check camera_schedule.json
   │   Loop through each schedule
   │
   ├─→ For each active camera:
   │   └─→ Check linked timetable entries
   │       └─→ Is there an active period NOW?
   │           │
   │           ├─→ YES:
   │           │   ├─→ Load student face database
   │           │   ├─→ Activate camera
   │           │   ├─→ Start face detection loop
   │           │   └─→ Mark attendance automatically
   │           │
   │           └─→ NO:
   │               └─→ Keep camera idle
   │
   └─→ Repeat every second
```

---

## **Example: 5-Day Schedule**

```
MONDAY
├─ 09:00 - 10:30: Data Structures (Batch A, CAM_001)
├─ 10:30 - 12:00: Database (Batch A, CAM_001)
└─ 14:00 - 15:30: Web Dev (Batch B, CAM_002)

TUESDAY
├─ 09:00 - 10:30: Web Dev (Batch A, CAM_001)
├─ 10:30 - 12:00: Networks (Batch A, CAM_001)
└─ 14:00 - 15:30: Data Structures (Batch B, CAM_002)

... and so on

CAMERA ACTIVATION
├─ Monday 08:59: CAM_001 initializes
├─ Monday 09:00: CAM_001 starts recording (Data Structures)
├─ Monday 10:30: CAM_001 stops, CAM_001 starts (Database)
├─ Monday 12:00: CAM_001 stops, idles
├─ Monday 13:59: CAM_002 initializes
├─ Monday 14:00: CAM_002 starts recording (Web Dev)
└─ Monday 15:30: CAM_002 stops
```

---

## **Performance Considerations**

```
Student Database Size  | Processing Time | Recommendation
──────────────────────┼─────────────────┼──────────────
< 100 students        | ~50ms per face  | Local JSON (Good)
100-500 students      | ~100ms per face | Local JSON (Okay)
500-1000 students     | ~200ms+ per face| Consider Database
1000+ students        | ~400ms+ per face| Use PostgreSQL/MongoDB
```

---

**Now your system is ready to capture attendance automatically! 🎉**
