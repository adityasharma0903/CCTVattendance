"""
MongoDB Database Module for Face Recognition Attendance System
Handles all database operations
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from typing import List, Dict, Optional
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION - MONGODB ATLAS (CLOUD)
# ============================================================================

# Using MongoDB Atlas (Cloud)
# Connection string format:
# mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority

# Get from .env file or environment variables
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "face_recognition")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL not found in environment variables or .env file")

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

class MongoDatabase:
    """MongoDB database connection and operations"""
    
    def __init__(self, url: str = MONGODB_URL, db_name: str = DB_NAME):
        """Initialize MongoDB connection"""
        self.url = url
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(
                self.url, 
                serverSelectionTimeoutMS=10000,
                socketTimeoutMS=10000,
                connectTimeoutMS=10000,
                tlsAllowInvalidCertificates=True,
                tlsAllowInvalidHostnames=True,
                retryWrites=True,
                ssl=True
            )
            # Verify connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            logger.info(f"✅ Connected to MongoDB: {self.db_name}")
            self.initialize_collections()
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ MongoDB Connection Error: {e}")
            logger.error("Make sure MongoDB is running. For local: 'mongod' command")
            logger.error("Or update MONGODB_URL in db.py for cloud (Atlas)")
            raise
    
    def initialize_collections(self):
        """Initialize collections and create indexes"""
        collections = {
            "students": [("roll_number", 1)],
            "batches": [("batch_id", 1)],
            "teachers": [("teacher_id", 1)],
            "subjects": [("subject_id", 1)],
            "cameras": [("camera_id", 1)],
            "camera_modes": [("camera_id", 1)],
            "camera_schedules": [("schedule_id", 1)],
            "timetable": [("timetable_id", 1), ("batch_id", 1)],
            "attendance": [("attendance_id", 1), ("roll_number", 1), ("batch_id", 1)],
            "exam_violations": [("violation_id", 1), ("student_id", 1)]
        }
        
        for collection_name, indexes in collections.items():
            collection = self.db[collection_name]
            for index in indexes:
                try:
                    collection.create_index(index)
                except Exception as e:
                    logger.warning(f"Could not create index {index} on {collection_name}: {e}")
            logger.info(f"✅ Initialized collection: {collection_name}")
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# ============================================================================
# GLOBAL DATABASE INSTANCE
# ============================================================================

db_instance = None

def get_db() -> MongoDatabase:
    """Get database instance (singleton pattern)"""
    global db_instance
    if db_instance is None:
        db_instance = MongoDatabase()
    return db_instance

# ============================================================================
# STUDENTS OPERATIONS
# ============================================================================

def add_student(student_data: Dict) -> Dict:
    """Add a new student to database"""
    db = get_db()
    students = db.db["students"]
    
    student = {
        "student_id": student_data.get("student_id"),
        "roll_number": student_data.get("roll_number"),
        "name": student_data.get("name"),
        "batch_id": student_data.get("batch_id"),
        "email": student_data.get("email"),
        "image_path": student_data.get("image_path"),
        "image_url": student_data.get("image_url"),
        "image_urls": student_data.get("image_urls"),
        "cloudinary_public_id": student_data.get("cloudinary_public_id"),
        "cloudinary_public_ids": student_data.get("cloudinary_public_ids"),
        "image_metadata": student_data.get("image_metadata"),
        "embedding": student_data.get("embedding"),
        "added_date": datetime.now().isoformat()
    }
    
    result = students.insert_one(student)
    return {"id": str(result.inserted_id), "roll_number": student_data.get("roll_number")}

def get_all_students() -> List[Dict]:
    """Get all students"""
    db = get_db()
    students = db.db["students"]
    return list(students.find({}, {"_id": 0}))

def get_student_by_roll(roll_number: str) -> Optional[Dict]:
    """Get student by roll number"""
    db = get_db()
    students = db.db["students"]
    return students.find_one({"roll_number": roll_number}, {"_id": 0})

def get_batch_students(batch_id: str) -> List[Dict]:
    """Get all students in a batch"""
    db = get_db()
    students = db.db["students"]
    return list(students.find({"batch_id": batch_id}, {"_id": 0}))

def update_student(roll_number: str, student_data: Dict) -> bool:
    """Update student information"""
    db = get_db()
    students = db.db["students"]
    
    result = students.update_one(
        {"roll_number": roll_number},
        {"$set": student_data}
    )
    return result.modified_count > 0

def delete_student(roll_number: str) -> bool:
    """Delete a student"""
    db = get_db()
    students = db.db["students"]
    
    result = students.delete_one({"roll_number": roll_number})
    return result.deleted_count > 0

# ============================================================================
# BATCHES OPERATIONS
# ============================================================================

def add_batch(batch_data: Dict) -> Dict:
    """Add a new batch"""
    db = get_db()
    batches = db.db["batches"]
    
    batch = {
        "batch_id": batch_data.get("batch_id"),
        "batch_name": batch_data.get("batch_name"),
        "semester": batch_data.get("semester"),
        "total_students": 0,
        "created_date": datetime.now().isoformat()
    }
    
    result = batches.insert_one(batch)
    return {"id": str(result.inserted_id)}

def get_all_batches() -> List[Dict]:
    """Get all batches"""
    db = get_db()
    batches = db.db["batches"]
    return list(batches.find({}, {"_id": 0}))

def get_batch(batch_id: str) -> Optional[Dict]:
    """Get batch by ID"""
    db = get_db()
    batches = db.db["batches"]
    return batches.find_one({"batch_id": batch_id}, {"_id": 0})

# ============================================================================
# TEACHERS OPERATIONS
# ============================================================================

def add_teacher(teacher_data: Dict) -> Dict:
    """Add a new teacher"""
    db = get_db()
    teachers = db.db["teachers"]
    
    teacher = {
        "teacher_id": teacher_data.get("teacher_id"),
        "name": teacher_data.get("name"),
        "email": teacher_data.get("email"),
        "phone": teacher_data.get("phone"),
        "created_date": datetime.now().isoformat()
    }
    
    result = teachers.insert_one(teacher)
    return {"id": str(result.inserted_id)}

def get_all_teachers() -> List[Dict]:
    """Get all teachers"""
    db = get_db()
    teachers = db.db["teachers"]
    return list(teachers.find({}, {"_id": 0}))

def get_teacher(teacher_id: str) -> Optional[Dict]:
    """Get teacher by ID"""
    db = get_db()
    teachers = db.db["teachers"]
    return teachers.find_one({"teacher_id": teacher_id}, {"_id": 0})

# ============================================================================
# SUBJECTS OPERATIONS
# ============================================================================

def add_subject(subject_data: Dict) -> Dict:
    """Add a new subject"""
    db = get_db()
    subjects = db.db["subjects"]
    
    subject = {
        "subject_id": subject_data.get("subject_id"),
        "subject_name": subject_data.get("subject_name"),
        "subject_code": subject_data.get("subject_code"),
        "teacher_id": subject_data.get("teacher_id"),
        "created_date": datetime.now().isoformat()
    }
    
    result = subjects.insert_one(subject)
    return {"id": str(result.inserted_id)}

def get_all_subjects() -> List[Dict]:
    """Get all subjects"""
    db = get_db()
    subjects = db.db["subjects"]
    return list(subjects.find({}, {"_id": 0}))

def get_subject(subject_id: str) -> Optional[Dict]:
    """Get subject by ID"""
    db = get_db()
    subjects = db.db["subjects"]
    return subjects.find_one({"subject_id": subject_id}, {"_id": 0})

# ============================================================================
# CAMERAS OPERATIONS
# ============================================================================

def add_camera(camera_data: Dict) -> Dict:
    """Add a new camera"""
    db = get_db()
    cameras = db.db["cameras"]
    
    camera = {
        "camera_id": camera_data.get("camera_id"),
        "camera_name": camera_data.get("camera_name"),
        "location": camera_data.get("location"),
        "ip_address": camera_data.get("ip_address"),
        "batch_id": camera_data.get("batch_id"),
        "is_active": camera_data.get("is_active", True),
        "created_date": datetime.now().isoformat()
    }
    
    result = cameras.insert_one(camera)
    return {"id": str(result.inserted_id)}

def get_all_cameras() -> List[Dict]:
    """Get all cameras"""
    db = get_db()
    cameras = db.db["cameras"]
    return list(cameras.find({}, {"_id": 0}))

def get_batch_cameras(batch_id: str) -> List[Dict]:
    """Get all cameras for a batch"""
    db = get_db()
    cameras = db.db["cameras"]
    return list(cameras.find({"batch_id": batch_id}, {"_id": 0}))

def get_camera(camera_id: str) -> Optional[Dict]:
    """Get camera by ID"""
    db = get_db()
    cameras = db.db["cameras"]
    return cameras.find_one({"camera_id": camera_id}, {"_id": 0})

def update_camera(camera_id: str, camera_data: Dict) -> bool:
    """Update camera information"""
    db = get_db()
    cameras = db.db["cameras"]
    
    result = cameras.update_one(
        {"camera_id": camera_id},
        {"$set": camera_data}
    )
    return result.modified_count > 0

# ============================================================================
# CAMERA MODE OPERATIONS
# ============================================================================

def set_camera_mode(camera_id: str, mode: str) -> Dict:
    """Set camera mode (NORMAL or EXAM)"""
    db = get_db()
    modes = db.db["camera_modes"]
    
    result = modes.update_one(
        {"camera_id": camera_id},
        {"$set": {"mode": mode, "updated_at": datetime.now().isoformat()}},
        upsert=True
    )
    return {"camera_id": camera_id, "mode": mode}

def get_camera_mode(camera_id: str) -> str:
    """Get camera mode"""
    db = get_db()
    modes = db.db["camera_modes"]
    
    mode_doc = modes.find_one({"camera_id": camera_id})
    if mode_doc:
        return mode_doc.get("mode", "NORMAL")
    return "NORMAL"

# ============================================================================
# TIMETABLE OPERATIONS
# ============================================================================

def add_timetable_entry(entry_data: Dict) -> Dict:
    """Add timetable entry"""
    db = get_db()
    timetable = db.db["timetable"]
    
    entry = {
        "timetable_id": entry_data.get("timetable_id"),
        "batch_id": entry_data.get("batch_id"),
        "day": entry_data.get("day"),
        "period": entry_data.get("period"),
        "start_time": entry_data.get("start_time"),
        "end_time": entry_data.get("end_time"),
        "subject_id": entry_data.get("subject_id"),
        "teacher_id": entry_data.get("teacher_id"),
        "room": entry_data.get("room", "Unknown Room"),
        "is_exam": entry_data.get("is_exam", False),
        "created_date": datetime.now().isoformat()
    }
    
    result = timetable.insert_one(entry)
    return {"id": str(result.inserted_id)}

def get_all_timetable() -> List[Dict]:
    """Get all timetable entries"""
    db = get_db()
    timetable = db.db["timetable"]
    return list(timetable.find({}, {"_id": 0}))

def get_batch_timetable(batch_id: str) -> List[Dict]:
    """Get timetable for a batch"""
    db = get_db()
    timetable = db.db["timetable"]
    return list(timetable.find({"batch_id": batch_id}, {"_id": 0}))

# ============================================================================
# CAMERA SCHEDULE OPERATIONS
# ============================================================================

def add_camera_schedule(schedule_data: Dict) -> Dict:
    """Add camera schedule"""
    db = get_db()
    schedules = db.db["camera_schedules"]
    
    schedule = {
        "schedule_id": schedule_data.get("schedule_id"),
        "camera_id": schedule_data.get("camera_id"),
        "timetable_id": schedule_data.get("timetable_id"),
        "is_active": schedule_data.get("is_active", True),
        "created_date": datetime.now().isoformat()
    }
    
    result = schedules.insert_one(schedule)
    return {"id": str(result.inserted_id)}

def get_camera_schedules(camera_id: str) -> List[Dict]:
    """Get schedules for a camera"""
    db = get_db()
    schedules = db.db["camera_schedules"]
    return list(schedules.find({"camera_id": camera_id}, {"_id": 0}))

def get_all_camera_schedules() -> List[Dict]:
    """Get all camera schedules"""
    db = get_db()
    schedules = db.db["camera_schedules"]
    return list(schedules.find({}, {"_id": 0}))

# ============================================================================
# ATTENDANCE OPERATIONS
# ============================================================================

def add_attendance(attendance_data: Dict) -> Dict:
    """Add attendance record"""
    db = get_db()
    attendance = db.db["attendance"]
    
    record = {
        "attendance_id": attendance_data.get("attendance_id"),
        "student_id": attendance_data.get("student_id"),
        "roll_number": attendance_data.get("roll_number"),
        "camera_id": attendance_data.get("camera_id"),
        "timestamp": attendance_data.get("timestamp", datetime.now().isoformat()),
        "subject_id": attendance_data.get("subject_id"),
        "batch_id": attendance_data.get("batch_id"),
        "status": attendance_data.get("status", "PRESENT"),
        "confidence_score": attendance_data.get("confidence_score", 0.0)
    }
    
    result = attendance.insert_one(record)
    return {"id": str(result.inserted_id)}

def get_all_attendance() -> List[Dict]:
    """Get all attendance records"""
    db = get_db()
    attendance = db.db["attendance"]
    return list(attendance.find({}, {"_id": 0}))

def get_batch_attendance(batch_id: str) -> List[Dict]:
    """Get attendance for a batch"""
    db = get_db()
    attendance = db.db["attendance"]
    return list(attendance.find({"batch_id": batch_id}, {"_id": 0}))

def get_student_attendance(roll_number: str) -> List[Dict]:
    """Get attendance for a student"""
    db = get_db()
    attendance = db.db["attendance"]
    return list(attendance.find({"roll_number": roll_number}, {"_id": 0}))

def check_attendance_exists(roll_number: str, date: str, subject_id: str, batch_id: str) -> Optional[Dict]:
    """Check if attendance exists for student on given date and subject"""
    db = get_db()
    attendance = db.db["attendance"]
    
    # Find records for the date
    record = attendance.find_one({
        "roll_number": roll_number,
        "subject_id": subject_id,
        "batch_id": batch_id,
        "timestamp": {"$regex": f"^{date}"}
    }, {"_id": 0})
    
    return record

# ============================================================================
# EXAM VIOLATIONS OPERATIONS
# ============================================================================

def add_exam_violation(violation_data: Dict) -> Dict:
    """Add exam violation record"""
    db = get_db()
    violations = db.db["exam_violations"]
    
    violation = {
        "violation_id": violation_data.get("violation_id"),
        "timestamp": violation_data.get("timestamp", datetime.now().isoformat()),
        "student_id": violation_data.get("student_id"),
        "student_name": violation_data.get("student_name"),
        "teacher_id": violation_data.get("teacher_id"),
        "subject_id": violation_data.get("subject_id"),
        "camera_id": violation_data.get("camera_id"),
        "camera_name": violation_data.get("camera_name"),
        "camera_location": violation_data.get("camera_location"),
        "confidence": violation_data.get("confidence", 0.0),
        "duration_seconds": violation_data.get("duration_seconds"),
        "notes": violation_data.get("notes"),
        "severity": violation_data.get("severity", "high")
    }
    
    result = violations.insert_one(violation)
    return {"id": str(result.inserted_id)}

def get_all_exam_violations() -> List[Dict]:
    """Get all exam violations"""
    db = get_db()
    violations = db.db["exam_violations"]
    return list(violations.find({}, {"_id": 0}))

def get_student_violations(student_id: str) -> List[Dict]:
    """Get violations for a student"""
    db = get_db()
    violations = db.db["exam_violations"]
    return list(violations.find({"student_id": student_id}, {"_id": 0}))

def delete_exam_violation(violation_id: str) -> bool:
    """Delete exam violation"""
    db = get_db()
    violations = db.db["exam_violations"]
    
    result = violations.delete_one({"violation_id": violation_id})
    return result.deleted_count > 0

# ============================================================================
# DASHBOARD & REPORTING
# ============================================================================

def get_dashboard_summary() -> Dict:
    """Get dashboard summary"""
    db = get_db()
    
    return {
        "total_students": db.db["students"].count_documents({}),
        "total_batches": db.db["batches"].count_documents({}),
        "total_teachers": db.db["teachers"].count_documents({}),
        "total_cameras": db.db["cameras"].count_documents({}),
        "total_attendance_records": db.db["attendance"].count_documents({})
    }

def get_attendance_report(batch_id: str) -> Dict:
    """Get attendance report for a batch"""
    db = get_db()
    attendance = db.db["attendance"]
    
    batch_attendance = list(attendance.find({"batch_id": batch_id}))
    
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
