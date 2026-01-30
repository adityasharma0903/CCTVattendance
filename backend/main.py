from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import os
from datetime import datetime

# ============================================================================
# FASTAPI APP SETUP
# ============================================================================

app = FastAPI(title="Face Recognition Attendance System")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
DATA_DIR = "../data"

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class Student(BaseModel):
    student_id: str
    roll_number: str
    name: str
    batch_id: str
    email: Optional[str] = None
    image_path: Optional[str] = None
    embedding: Optional[List[float]] = None

class Batch(BaseModel):
    batch_id: str
    batch_name: str
    semester: str

class Teacher(BaseModel):
    teacher_id: str
    name: str
    email: str
    phone: str

class Subject(BaseModel):
    subject_id: str
    subject_name: str
    subject_code: str
    teacher_id: str

class Camera(BaseModel):
    camera_id: str
    camera_name: str
    location: str
    ip_address: str
    batch_id: str
    is_active: bool

class Timetable(BaseModel):
    timetable_id: str
    batch_id: str
    day: str
    period: int
    start_time: str
    end_time: str
    subject_id: str
    teacher_id: str

class CameraSchedule(BaseModel):
    schedule_id: str
    camera_id: str
    timetable_id: str
    is_active: bool

class AttendanceRecord(BaseModel):
    attendance_id: str
    student_id: str
    roll_number: str
    camera_id: str
    timestamp: str
    subject_id: str
    batch_id: str
    status: str  # PRESENT, ABSENT, LATE
    confidence_score: float

# ============================================================================
# FILE MANAGEMENT UTILITIES
# ============================================================================

def load_json_file(filename):
    """Load JSON file from data directory"""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return {}

def save_json_file(filename, data):
    """Save JSON file to data directory"""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

# ============================================================================
# STUDENTS ENDPOINTS
# ============================================================================

@app.get("/api/students", response_model=List[Dict])
async def get_all_students():
    """Get all students"""
    students_data = load_json_file("students_database.json")
    students_list = []
    for roll_id, student_data in students_data.items():
        students_list.append(student_data)
    return students_list

@app.get("/api/students/{batch_id}", response_model=List[Dict])
async def get_batch_students(batch_id: str):
    """Get students from specific batch"""
    students_data = load_json_file("students_database.json")
    batch_students = []
    for roll_id, student in students_data.items():
        if student.get("batch_id") == batch_id or student.get("roll_number").startswith(batch_id):
            batch_students.append(student)
    return batch_students

@app.post("/api/students")
async def add_student(student: Dict):
    """Add new student"""
    students_data = load_json_file("students_database.json")
    roll_number = student.get("roll_number")
    
    if roll_number in students_data:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    students_data[roll_number] = {
        "student_id": f"STU_{roll_number}",
        "roll_number": roll_number,
        "name": student.get("name"),
        "batch_id": student.get("batch_id"),
        "email": student.get("email"),
        "image_path": student.get("image_path"),
        "embedding": student.get("embedding"),
        "added_date": datetime.now().isoformat()
    }
    
    if save_json_file("students_database.json", students_data):
        return {"status": "success", "message": "Student added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add student")

@app.put("/api/students/{roll_number}")
async def update_student(roll_number: str, student: Dict):
    """Update student information"""
    students_data = load_json_file("students_database.json")
    
    if roll_number not in students_data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    students_data[roll_number].update(student)
    
    if save_json_file("students_database.json", students_data):
        return {"status": "success", "message": "Student updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update student")

@app.delete("/api/students/{roll_number}")
async def delete_student(roll_number: str):
    """Delete student"""
    students_data = load_json_file("students_database.json")
    
    if roll_number not in students_data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    del students_data[roll_number]
    
    if save_json_file("students_database.json", students_data):
        return {"status": "success", "message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete student")

# ============================================================================
# BATCHES ENDPOINTS
# ============================================================================

@app.get("/api/batches", response_model=List[Dict])
async def get_all_batches():
    """Get all batches"""
    batches = load_json_file("batches.json")
    return batches.get("batches", [])

@app.post("/api/batches")
async def add_batch(batch: Dict):
    """Add new batch"""
    batches_data = load_json_file("batches.json")
    
    new_batch = {
        "batch_id": batch.get("batch_id"),
        "batch_name": batch.get("batch_name"),
        "semester": batch.get("semester"),
        "total_students": 0
    }
    
    batches_data.setdefault("batches", []).append(new_batch)
    
    if save_json_file("batches.json", batches_data):
        return {"status": "success", "message": "Batch added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add batch")

# ============================================================================
# TEACHERS ENDPOINTS
# ============================================================================

@app.get("/api/teachers", response_model=List[Dict])
async def get_all_teachers():
    """Get all teachers"""
    teachers = load_json_file("teachers.json")
    return teachers.get("teachers", [])

@app.post("/api/teachers")
async def add_teacher(teacher: Dict):
    """Add new teacher"""
    teachers_data = load_json_file("teachers.json")
    
    new_teacher = {
        "teacher_id": teacher.get("teacher_id"),
        "name": teacher.get("name"),
        "email": teacher.get("email"),
        "phone": teacher.get("phone")
    }
    
    teachers_data.setdefault("teachers", []).append(new_teacher)
    
    if save_json_file("teachers.json", teachers_data):
        return {"status": "success", "message": "Teacher added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add teacher")

# ============================================================================
# SUBJECTS ENDPOINTS
# ============================================================================

@app.get("/api/subjects", response_model=List[Dict])
async def get_all_subjects():
    """Get all subjects"""
    subjects = load_json_file("subjects.json")
    return subjects.get("subjects", [])

@app.post("/api/subjects")
async def add_subject(subject: Dict):
    """Add new subject"""
    subjects_data = load_json_file("subjects.json")
    
    new_subject = {
        "subject_id": subject.get("subject_id"),
        "subject_name": subject.get("subject_name"),
        "subject_code": subject.get("subject_code"),
        "teacher_id": subject.get("teacher_id")
    }
    
    subjects_data.setdefault("subjects", []).append(new_subject)
    
    if save_json_file("subjects.json", subjects_data):
        return {"status": "success", "message": "Subject added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add subject")

# ============================================================================
# CAMERAS ENDPOINTS
# ============================================================================

@app.get("/api/cameras", response_model=List[Dict])
async def get_all_cameras():
    """Get all cameras"""
    cameras = load_json_file("cameras.json")
    return cameras.get("cameras", [])

@app.get("/api/cameras/{batch_id}", response_model=List[Dict])
async def get_batch_cameras(batch_id: str):
    """Get cameras for specific batch"""
    cameras = load_json_file("cameras.json")
    batch_cameras = [cam for cam in cameras.get("cameras", []) if cam.get("batch_id") == batch_id]
    return batch_cameras

@app.post("/api/cameras")
async def add_camera(camera: Dict):
    """Add new camera"""
    cameras_data = load_json_file("cameras.json")
    
    new_camera = {
        "camera_id": camera.get("camera_id"),
        "camera_name": camera.get("camera_name"),
        "location": camera.get("location"),
        "ip_address": camera.get("ip_address"),
        "batch_id": camera.get("batch_id"),
        "is_active": camera.get("is_active", True)
    }
    
    cameras_data.setdefault("cameras", []).append(new_camera)
    
    if save_json_file("cameras.json", cameras_data):
        return {"status": "success", "message": "Camera added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add camera")

# ============================================================================
# TIMETABLE ENDPOINTS
# ============================================================================

@app.get("/api/timetable", response_model=List[Dict])
async def get_timetable():
    """Get all timetable entries"""
    timetable = load_json_file("timetable.json")
    return timetable.get("timetable", [])

@app.get("/api/timetable/{batch_id}", response_model=List[Dict])
async def get_batch_timetable(batch_id: str):
    """Get timetable for specific batch"""
    timetable = load_json_file("timetable.json")
    batch_timetable = [tt for tt in timetable.get("timetable", []) if tt.get("batch_id") == batch_id]
    return batch_timetable

@app.post("/api/timetable")
async def add_timetable(entry: Dict):
    """Add timetable entry"""
    timetable_data = load_json_file("timetable.json")
    
    new_entry = {
        "timetable_id": entry.get("timetable_id"),
        "batch_id": entry.get("batch_id"),
        "day": entry.get("day"),
        "period": entry.get("period"),
        "start_time": entry.get("start_time"),
        "end_time": entry.get("end_time"),
        "subject_id": entry.get("subject_id"),
        "teacher_id": entry.get("teacher_id")
    }
    
    timetable_data.setdefault("timetable", []).append(new_entry)
    
    if save_json_file("timetable.json", timetable_data):
        return {"status": "success", "message": "Timetable entry added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add timetable entry")

# ============================================================================
# CAMERA SCHEDULE ENDPOINTS
# ============================================================================

@app.get("/api/camera-schedule", response_model=List[Dict])
async def get_camera_schedule():
    """Get all camera schedules"""
    schedule = load_json_file("camera_schedule.json")
    return schedule.get("camera_schedule", [])

@app.get("/api/camera-schedule/{camera_id}", response_model=List[Dict])
async def get_camera_schedule_by_id(camera_id: str):
    """Get schedule for specific camera"""
    schedule = load_json_file("camera_schedule.json")
    cam_schedule = [s for s in schedule.get("camera_schedule", []) if s.get("camera_id") == camera_id]
    return cam_schedule

@app.post("/api/camera-schedule")
async def add_camera_schedule(schedule: Dict):
    """Add camera schedule"""
    schedule_data = load_json_file("camera_schedule.json")
    
    new_schedule = {
        "schedule_id": schedule.get("schedule_id"),
        "camera_id": schedule.get("camera_id"),
        "timetable_id": schedule.get("timetable_id"),
        "is_active": schedule.get("is_active", True)
    }
    
    schedule_data.setdefault("camera_schedule", []).append(new_schedule)
    
    if save_json_file("camera_schedule.json", schedule_data):
        return {"status": "success", "message": "Camera schedule added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add camera schedule")

# ============================================================================
# ATTENDANCE ENDPOINTS
# ============================================================================

@app.get("/api/attendance", response_model=List[Dict])
async def get_all_attendance():
    """Get all attendance records"""
    attendance = load_json_file("attendance.json")
    return attendance.get("attendance", [])

@app.get("/api/attendance/{batch_id}", response_model=List[Dict])
async def get_batch_attendance(batch_id: str):
    """Get attendance for specific batch"""
    attendance = load_json_file("attendance.json")
    batch_attendance = [a for a in attendance.get("attendance", []) if a.get("batch_id") == batch_id]
    return batch_attendance

@app.get("/api/attendance/student/{roll_number}", response_model=List[Dict])
async def get_student_attendance(roll_number: str):
    """Get attendance for specific student"""
    attendance = load_json_file("attendance.json")
    student_attendance = [a for a in attendance.get("attendance", []) if a.get("roll_number") == roll_number]
    return student_attendance

@app.get("/api/attendance-check")
async def check_attendance_exists(roll_number: str, date: str, subject_id: str, batch_id: str):
    """Check if attendance already exists for student on given date and subject"""
    attendance_data = load_json_file("attendance.json")
    
    for record in attendance_data.get("attendance", []):
        # Check if same student, subject, batch, and same day
        record_date = record.get("timestamp", "")[:10]  # Get YYYY-MM-DD part
        
        if (record.get("roll_number") == roll_number and
            record.get("subject_id") == subject_id and
            record.get("batch_id") == batch_id and
            record_date == date):
            return {"exists": True, "record": record}
    
    return {"exists": False}

@app.post("/api/attendance")
async def mark_attendance(record: Dict):
    """Mark attendance for a student"""
    attendance_data = load_json_file("attendance.json")
    
    import uuid
    new_record = {
        "attendance_id": str(uuid.uuid4()),
        "student_id": record.get("student_id"),
        "roll_number": record.get("roll_number"),
        "camera_id": record.get("camera_id"),
        "timestamp": record.get("timestamp", datetime.now().isoformat()),
        "subject_id": record.get("subject_id"),
        "batch_id": record.get("batch_id"),
        "status": record.get("status", "PRESENT"),
        "confidence_score": record.get("confidence_score", 0.0)
    }
    
    attendance_data.setdefault("attendance", []).append(new_record)
    
    if save_json_file("attendance.json", attendance_data):
        return {"status": "success", "message": "Attendance marked successfully", "record": new_record}
    else:
        raise HTTPException(status_code=500, detail="Failed to mark attendance")

# ============================================================================
# DASHBOARD & REPORTS
# ============================================================================

@app.get("/api/dashboard/summary")
async def get_dashboard_summary():
    """Get dashboard summary"""
    students = load_json_file("students_database.json")
    batches = load_json_file("batches.json")
    teachers = load_json_file("teachers.json")
    cameras = load_json_file("cameras.json")
    attendance = load_json_file("attendance.json")
    
    return {
        "total_students": len(students),
        "total_batches": len(batches.get("batches", [])),
        "total_teachers": len(teachers.get("teachers", [])),
        "total_cameras": len(cameras.get("cameras", [])),
        "total_attendance_records": len(attendance.get("attendance", []))
    }

@app.get("/api/attendance/report/{batch_id}")
async def get_attendance_report(batch_id: str):
    """Get attendance report for a batch"""
    attendance_data = load_json_file("attendance.json")
    batch_attendance = [a for a in attendance_data.get("attendance", []) if a.get("batch_id") == batch_id]
    
    # Calculate statistics
    total_records = len(batch_attendance)
    present_count = len([a for a in batch_attendance if a.get("status") == "PRESENT"])
    absent_count = len([a for a in batch_attendance if a.get("status") == "ABSENT"])
    late_count = len([a for a in batch_attendance if a.get("status") == "LATE"])
    
    return {
        "batch_id": batch_id,
        "total_records": total_records,
        "present": present_count,
        "absent": absent_count,
        "late": late_count,
        "attendance_percentage": (present_count / total_records * 100) if total_records > 0 else 0
    }

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Face Recognition Attendance System API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
