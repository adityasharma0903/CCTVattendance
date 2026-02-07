from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import os
from datetime import datetime
import logging
import cv2
import numpy as np
from io import BytesIO
from deepface import DeepFace

# Import Cloudinary utilities
from cloudinary_utils import (
    upload_student_image,
    upload_from_file_path,
    delete_student_image,
    download_image_from_url,
    validate_cloudinary_config
)

# Import MongoDB operations
import db

# ============================================================================
# LOGGING SETUP
# ============================================================================
logger = logging.getLogger(__name__)

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
    image_url: Optional[str] = None  # Cloudinary URL
    image_path: Optional[str] = None  # Legacy support
    cloudinary_public_id: Optional[str] = None
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

class ExamViolation(BaseModel):
    violation_id: str
    timestamp: str
    student_id: str
    student_name: str
    teacher_id: str
    subject_id: str
    camera_id: str
    camera_name: Optional[str] = None
    camera_location: Optional[str] = None
    confidence: float
    duration_seconds: Optional[int] = None
    notes: Optional[str] = None
    severity: Optional[str] = "high"

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
# STUDENTS ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/students", response_model=List[Dict])
async def get_all_students():
    """Get all students from MongoDB"""
    try:
        students = db.get_all_students()
        return students
    except Exception as e:
        logger.error(f"Error getting students: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/students/{batch_id}", response_model=List[Dict])
async def get_batch_students(batch_id: str):
    """Get students from specific batch from MongoDB"""
    try:
        batch_students = db.get_batch_students(batch_id)
        return batch_students
    except Exception as e:
        logger.error(f"Error getting batch students: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/students")
async def add_student(student: Dict):
    """Add new student to MongoDB"""
    try:
        roll_number = student.get("roll_number")
        
        # Check if student exists
        existing = db.get_student_by_roll(roll_number)
        if existing:
            raise HTTPException(status_code=400, detail="Student already exists")
        
        student_data = {
            "student_id": f"STU_{roll_number}",
            "roll_number": roll_number,
            "name": student.get("name"),
            "batch_id": student.get("batch_id"),
            "email": student.get("email"),
            "image_path": student.get("image_path") or student.get("image_url"),  # Accept both field names
            "image_url": student.get("image_url"),  # Save Cloudinary URL
            "cloudinary_public_id": student.get("cloudinary_public_id"),
            "embedding": student.get("embedding")
        }
        
        result = db.add_student(student_data)
        logger.info(f"✅ Student added to MongoDB: {roll_number}")
        return {"status": "success", "message": "Student added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding student: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/students/{roll_number}")
async def update_student(roll_number: str, student: Dict):
    """Update student information in MongoDB"""
    try:
        # Check if student exists
        existing = db.get_student_by_roll(roll_number)
        if not existing:
            raise HTTPException(status_code=404, detail="Student not found")
        
        success = db.update_student(roll_number, student)
        if success:
            logger.info(f"✅ Student updated in MongoDB: {roll_number}")
            return {"status": "success", "message": "Student updated successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update student")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating student: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/students/{roll_number}")
async def delete_student(roll_number: str):
    """Delete student from MongoDB"""
    try:
        # Check if student exists
        existing = db.get_student_by_roll(roll_number)
        if not existing:
            raise HTTPException(status_code=404, detail="Student not found")
        
        success = db.delete_student(roll_number)
        if success:
            logger.info(f"✅ Student deleted from MongoDB: {roll_number}")
            return {"status": "success", "message": "Student deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete student")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting student: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/students/upload-image")
async def upload_student_image_endpoint(
    file: UploadFile = File(...),
    student_id: str = Form(...),
    roll_number: str = Form(...),
    name: str = Form(...),
    batch_id: str = Form(...),
    email: Optional[str] = Form(None)
):
    """
    Upload student image to Cloudinary, generate face embedding, and save to database
    """
    try:
        # Validate Cloudinary config
        if not validate_cloudinary_config():
            raise HTTPException(
                status_code=500,
                detail="Cloudinary is not configured properly. Check environment variables."
            )
        
        # Read image file
        contents = await file.read()
        
        # Convert to OpenCV format for face detection
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Generate face embedding using DeepFace
        logger.info(f"⏳ Generating face embedding for {name} (Roll: {roll_number})...")
        try:
            embedding_result = DeepFace.represent(
                img,
                model_name="ArcFace",
                enforce_detection=True
            )
            embedding = embedding_result[0]["embedding"]
            logger.info(f"✅ Face embedding generated successfully")
        except Exception as e:
            logger.error(f"❌ Face detection failed: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Face detection failed. Please ensure the image contains a clear, frontal face. Error: {str(e)}"
            )
        
        # Upload image to Cloudinary
        logger.info(f"⏳ Uploading image to Cloudinary for {name}...")
        file.file.seek(0)  # Reset file pointer
        upload_result = upload_student_image(file.file, student_id, roll_number)
        
        if not upload_result:
            raise HTTPException(status_code=500, detail="Failed to upload image to Cloudinary")
        
        logger.info(f"✅ Image uploaded to Cloudinary: {upload_result['url']}")
        
        # Check if student exists and delete old image if needed
        existing_student = db.get_student_by_roll(roll_number)
        if existing_student:
            old_public_id = existing_student.get("cloudinary_public_id")
            if old_public_id and old_public_id != upload_result["public_id"]:
                delete_student_image(old_public_id)
        
        # Save/Update in MongoDB
        student_data = {
            "student_id": student_id,
            "roll_number": roll_number,
            "name": name,
            "batch_id": batch_id,
            "email": email,
            "image_url": upload_result["url"],
            "cloudinary_public_id": upload_result["public_id"],
            "embedding": embedding,
            "image_metadata": {
                "width": upload_result.get("width"),
                "height": upload_result.get("height"),
                "format": upload_result.get("format"),
                "size_bytes": upload_result.get("bytes")
            }
        }
        
        # Check if student exists
        existing = db.get_student_by_roll(roll_number)
        if existing:
            # Update existing
            old_public_id = existing.get("cloudinary_public_id")
            if old_public_id and old_public_id != upload_result["public_id"]:
                delete_student_image(old_public_id)
            db.update_student(roll_number, student_data)
            logger.info(f"✅ Student {name} updated in MongoDB with Cloudinary image")
        else:
            # Add new
            db.add_student(student_data)
            logger.info(f"✅ Student {name} added to MongoDB with Cloudinary image")
        
        return {
            "status": "success",
            "message": f"Student {name} registered successfully with face recognition",
            "data": {
                "student_id": student_id,
                "roll_number": roll_number,
                "name": name,
                "image_url": upload_result["url"],
                "cloudinary_public_id": upload_result["public_id"]
            }
        }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error uploading student image: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/students/{roll_number}/upload-image")
async def update_student_image_endpoint(
    roll_number: str,
    file: UploadFile = File(...)
):
    """
    Upload/Update image for existing student to Cloudinary and update MongoDB
    """
    try:
        # Check if student exists
        existing_student = db.get_student_by_roll(roll_number)
        if not existing_student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Validate Cloudinary config
        if not validate_cloudinary_config():
            raise HTTPException(
                status_code=500,
                detail="Cloudinary is not configured properly. Check environment variables."
            )
        
        # Read image file
        contents = await file.read()
        
        # Convert to OpenCV format for face detection
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Generate face embedding using DeepFace
        logger.info(f"⏳ Generating face embedding for {existing_student.get('name')}...")
        try:
            embedding_result = DeepFace.represent(
                img,
                model_name="ArcFace",
                enforce_detection=True
            )
            embedding = embedding_result[0]["embedding"]
            logger.info(f"✅ Face embedding generated successfully")
        except Exception as e:
            logger.error(f"❌ Face detection failed: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Face detection failed. Please ensure the image contains a clear, frontal face. Error: {str(e)}"
            )
        
        # Upload image to Cloudinary
        logger.info(f"⏳ Uploading image to Cloudinary...")
        file.file.seek(0)  # Reset file pointer
        student_id = existing_student.get("student_id", f"STU_{roll_number}")
        upload_result = upload_student_image(file.file, student_id, roll_number)
        
        if not upload_result:
            raise HTTPException(status_code=500, detail="Failed to upload image to Cloudinary")
        
        logger.info(f"✅ Image uploaded to Cloudinary: {upload_result['url']}")
        
        # Delete old image if exists
        old_public_id = existing_student.get("cloudinary_public_id")
        if old_public_id:
            delete_student_image(old_public_id)
        
        # Update in MongoDB
        update_data = {
            "image_url": upload_result["url"],
            "image_path": upload_result["url"],  # Keep both field names for consistency
            "cloudinary_public_id": upload_result["public_id"],
            "embedding": embedding,
            "image_metadata": {
                "width": upload_result.get("width"),
                "height": upload_result.get("height"),
                "format": upload_result.get("format"),
                "size_bytes": upload_result.get("bytes")
            }
        }
        
        db.update_student(roll_number, update_data)
        logger.info(f"✅ Student {existing_student.get('name')} image updated in MongoDB")
        
        return {
            "status": "success",
            "message": f"Student {existing_student.get('name')} image updated successfully",
            "data": {
                "roll_number": roll_number,
                "image_url": upload_result["url"],
                "cloudinary_public_id": upload_result["public_id"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating student image: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# ============================================================================
# BATCHES ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/batches", response_model=List[Dict])
async def get_all_batches():
    """Get all batches from MongoDB"""
    try:
        batches = db.get_all_batches()
        return batches
    except Exception as e:
        logger.error(f"Error getting batches: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/batches")
async def add_batch(batch: Dict):
    """Add new batch to MongoDB"""
    try:
        batch_data = {
            "batch_id": batch.get("batch_id"),
            "batch_name": batch.get("batch_name"),
            "semester": batch.get("semester"),
            "total_students": 0
        }
        
        result = db.add_batch(batch_data)
        logger.info(f"✅ Batch added to MongoDB: {batch.get('batch_id')}")
        return {"status": "success", "message": "Batch added successfully"}
    except Exception as e:
        logger.error(f"Error adding batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TEACHERS ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/teachers", response_model=List[Dict])
async def get_all_teachers():
    """Get all teachers from MongoDB"""
    try:
        teachers = db.get_all_teachers()
        return teachers
    except Exception as e:
        logger.error(f"Error getting teachers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/teachers")
async def add_teacher(teacher: Dict):
    """Add new teacher to MongoDB"""
    try:
        teacher_data = {
            "teacher_id": teacher.get("teacher_id"),
            "name": teacher.get("name"),
            "email": teacher.get("email"),
            "phone": teacher.get("phone")
        }
        
        result = db.add_teacher(teacher_data)
        logger.info(f"✅ Teacher added to MongoDB: {teacher.get('teacher_id')}")
        return {"status": "success", "message": "Teacher added successfully"}
    except Exception as e:
        logger.error(f"Error adding teacher: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# SUBJECTS ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/subjects", response_model=List[Dict])
async def get_all_subjects():
    """Get all subjects from MongoDB"""
    try:
        subjects = db.get_all_subjects()
        return subjects
    except Exception as e:
        logger.error(f"Error getting subjects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/subjects")
async def add_subject(subject: Dict):
    """Add new subject to MongoDB"""
    try:
        subject_data = {
            "subject_id": subject.get("subject_id"),
            "subject_name": subject.get("subject_name"),
            "subject_code": subject.get("subject_code"),
            "teacher_id": subject.get("teacher_id")
        }
        
        result = db.add_subject(subject_data)
        logger.info(f"✅ Subject added to MongoDB: {subject.get('subject_id')}")
        return {"status": "success", "message": "Subject added successfully"}
    except Exception as e:
        logger.error(f"Error adding subject: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CAMERAS ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/cameras", response_model=List[Dict])
async def get_all_cameras():
    """Get all cameras from MongoDB"""
    try:
        cameras = db.get_all_cameras()
        return cameras
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cameras/{batch_id}", response_model=List[Dict])
async def get_batch_cameras(batch_id: str):
    """Get cameras for specific batch from MongoDB"""
    try:
        batch_cameras = db.get_batch_cameras(batch_id)
        return batch_cameras
    except Exception as e:
        logger.error(f"Error getting batch cameras: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CAMERA MODE ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/camera-mode/{camera_id}")
async def get_camera_mode(camera_id: str):
    """Get mode for a specific camera from MongoDB"""
    try:
        mode = db.get_camera_mode(camera_id)
        return {"camera_id": camera_id, "mode": mode}
    except Exception as e:
        logger.error(f"Error getting camera mode: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/camera-mode")
async def set_camera_mode(payload: Dict):
    """Set mode for a camera in MongoDB"""
    try:
        camera_id = payload.get("camera_id")
        mode = payload.get("mode", "NORMAL")
        
        if mode not in ["NORMAL", "EXAM"]:
            raise HTTPException(status_code=400, detail="Invalid mode")
        
        result = db.set_camera_mode(camera_id, mode)
        logger.info(f"✅ Camera mode set in MongoDB: {camera_id} -> {mode}")
        return {"status": "success", "camera_id": camera_id, "mode": mode}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting camera mode: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TIMETABLE ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/timetable", response_model=List[Dict])
async def get_all_timetable():
    """Get all timetable entries from MongoDB"""
    try:
        timetable = db.get_all_timetable()
        return timetable
    except Exception as e:
        logger.error(f"Error getting timetable: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/timetable/{batch_id}", response_model=List[Dict])
async def get_batch_timetable(batch_id: str):
    """Get timetable for specific batch from MongoDB"""
    try:
        batch_timetable = db.get_batch_timetable(batch_id)
        return batch_timetable
    except Exception as e:
        logger.error(f"Error getting batch timetable: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/timetable")
async def add_timetable_entry(entry: Dict):
    """Add new timetable entry to MongoDB"""
    try:
        timetable_data = {
            "timetable_id": entry.get("timetable_id"),
            "batch_id": entry.get("batch_id"),
            "day": entry.get("day"),
            "period": entry.get("period"),
            "start_time": entry.get("start_time"),
            "end_time": entry.get("end_time"),
            "subject_id": entry.get("subject_id"),
            "teacher_id": entry.get("teacher_id"),
            "room": entry.get("room"),
            "is_exam": entry.get("is_exam", False)
        }
        
        result = db.add_timetable_entry(timetable_data)
        logger.info(f"✅ Timetable entry added to MongoDB: {entry.get('timetable_id')}")
        return {"status": "success", "message": "Timetable entry added successfully"}
    except Exception as e:
        logger.error(f"Error adding timetable entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CAMERA SCHEDULE ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/camera-schedules", response_model=List[Dict])
async def get_all_camera_schedules():
    """Get all camera schedules from MongoDB"""
    try:
        schedules = db.get_all_camera_schedules()
        return schedules
    except Exception as e:
        logger.error(f"Error getting camera schedules: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/camera-schedule/{camera_id}", response_model=List[Dict])
async def get_camera_schedule_by_id(camera_id: str):
    """Get schedule for specific camera from MongoDB"""
    try:
        cam_schedule = db.get_camera_schedules(camera_id)
        return cam_schedule
    except Exception as e:
        logger.error(f"Error getting camera schedule: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/camera-schedule")
async def add_camera_schedule(schedule: Dict):
    """Add camera schedule to MongoDB"""
    try:
        schedule_data = {
            "schedule_id": schedule.get("schedule_id"),
            "camera_id": schedule.get("camera_id"),
            "timetable_id": schedule.get("timetable_id"),
            "is_active": schedule.get("is_active", True)
        }
        
        result = db.add_camera_schedule(schedule_data)
        logger.info(f"✅ Camera schedule added to MongoDB")
        return {"status": "success", "message": "Camera schedule added successfully"}
    except Exception as e:
        logger.error(f"Error adding camera schedule: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ATTENDANCE ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/attendance", response_model=List[Dict])
async def get_all_attendance():
    """Get all attendance records from MongoDB"""
    try:
        attendance = db.get_all_attendance()
        return attendance
    except Exception as e:
        logger.error(f"Error getting attendance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance/{batch_id}", response_model=List[Dict])
async def get_batch_attendance(batch_id: str):
    """Get attendance for specific batch from MongoDB"""
    try:
        batch_attendance = db.get_batch_attendance(batch_id)
        return batch_attendance
    except Exception as e:
        logger.error(f"Error getting batch attendance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance/student/{roll_number}", response_model=List[Dict])
async def get_student_attendance(roll_number: str):
    """Get attendance for specific student from MongoDB"""
    try:
        student_attendance = db.get_student_attendance(roll_number)
        return student_attendance
    except Exception as e:
        logger.error(f"Error getting student attendance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance-check")
async def check_attendance_exists(roll_number: str, date: str, subject_id: str, batch_id: str):
    """Check if attendance already exists for student on given date and subject in MongoDB"""
    try:
        record = db.check_attendance_exists(roll_number, date, subject_id, batch_id)
        if record:
            return {"exists": True, "record": record}
        return {"exists": False}
    except Exception as e:
        logger.error(f"Error checking attendance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/attendance")
async def mark_attendance(record: Dict):
    """Mark attendance for a student in MongoDB"""
    try:
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
        
        result = db.add_attendance(new_record)
        logger.info(f"✅ Attendance marked in MongoDB for {record.get('roll_number')}")
        return {"status": "success", "message": "Attendance marked successfully", "record": new_record}
    except Exception as e:
        logger.error(f"❌ Error marking attendance: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to mark attendance: {str(e)}")

# ============================================================================
# DASHBOARD & REPORTS
# ============================================================================

@app.get("/api/dashboard/summary")
async def get_dashboard_summary():
    """Get dashboard summary from MongoDB"""
    try:
        summary = db.get_dashboard_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance/report/{batch_id}")
async def get_attendance_report(batch_id: str):
    """Get attendance report for a batch from MongoDB"""
    try:
        batch_attendance = db.get_batch_attendance(batch_id)
        
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
    except Exception as e:
        logger.error(f"Error getting attendance report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# EXAM VIOLATIONS ENDPOINTS (MongoDB)
# ============================================================================

@app.get("/api/exam-violations")
async def get_exam_violations():
    """Get all exam violations from MongoDB"""
    try:
        violations = db.get_all_exam_violations()
        return violations
    except Exception as e:
        logger.error(f"Error getting exam violations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/exam-violations")
async def add_exam_violation(violation: ExamViolation):
    """Add new exam violation to MongoDB"""
    try:
        violation_dict = violation.dict()
        result = db.add_exam_violation(violation_dict)
        logger.info(f"✅ Exam violation added to MongoDB: {violation.violation_id}")
        return {
            "status": "success",
            "violation_id": violation.violation_id,
            "message": "Phone detection violation recorded"
        }
    except Exception as e:
        logger.error(f"Error adding exam violation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/exam-violations/{student_id}")
async def get_student_violations(student_id: str):
    """Get all violations for a specific student from MongoDB"""
    try:
        violations = db.get_student_violations(student_id)
        return violations
    except Exception as e:
        logger.error(f"Error getting student violations: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    violations = load_exam_violations()
    student_violations = [v for v in violations if v.get("student_id") == student_id]
    return student_violations

@app.delete("/api/exam-violations/{violation_id}")
async def delete_violation(violation_id: str):
    """Delete an exam violation record"""
    violations = load_exam_violations()
    filtered_violations = [v for v in violations if v.get("violation_id") != violation_id]
    save_exam_violations(filtered_violations)
    return {
        "status": "success",
        "message": f"Violation {violation_id} deleted"
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
