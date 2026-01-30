import json
import os
import requests
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = "../data"
BACKEND_API = "http://localhost:8000/api"

def load_json_file(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return {}

def test_backend():
    """Test backend connectivity"""
    logger.info("🧪 Testing Backend API...")
    try:
        response = requests.get(f"{BACKEND_API}/students")
        if response.status_code == 200:
            logger.info(f"✅ Backend is running! Found {len(response.json())} students")
            return True
        else:
            logger.error(f"❌ Backend returned error: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Cannot connect to backend: {e}")
        logger.error(f"   Make sure backend is running: .\start_backend_venv.bat")
        return False

def test_data_files():
    """Test data files"""
    logger.info("\n📂 Checking Data Files...")
    files_needed = ["students_database.json", "cameras.json", "timetable.json", "camera_schedule.json"]
    
    all_exist = True
    for file in files_needed:
        path = os.path.join(DATA_DIR, file) if not file.startswith("..") else file
        if file == "students_database.json":
            path = "../iotproject/students_database.json"
        
        if os.path.exists(path):
            logger.info(f"   ✅ {file}")
        else:
            logger.error(f"   ❌ {file} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_mark_attendance():
    """Test marking attendance via API"""
    logger.info("\n📝 Testing Attendance Marking...")
    
    # Check if we have students
    students_db = load_json_file("../iotproject/students_database.json")
    if not students_db:
        logger.error("❌ No students in database")
        return False
    
    # Get first student
    first_roll = list(students_db.keys())[0]
    student = students_db[first_roll]
    
    test_attendance = {
        "student_id": f"STU_{first_roll}",
        "roll_number": first_roll,
        "camera_id": "CAM_001",
        "timestamp": datetime.now().isoformat(),
        "subject_id": "S001",
        "batch_id": "B001",
        "status": "PRESENT",
        "confidence_score": 0.95
    }
    
    try:
        response = requests.post(f"{BACKEND_API}/attendance", json=test_attendance)
        if response.status_code == 200:
            logger.info(f"✅ Successfully marked attendance for {student.get('name', first_roll)}")
            logger.info(f"   Response: {response.json()}")
            return True
        else:
            logger.error(f"❌ Failed to mark attendance: {response.status_code}")
            logger.error(f"   Error: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def main():
    logger.info("=" * 50)
    logger.info("CAMERA SERVICE - SYSTEM TEST")
    logger.info("=" * 50)
    
    backend_ok = test_backend()
    files_ok = test_data_files()
    attendance_ok = test_mark_attendance() if backend_ok else False
    
    logger.info("\n" + "=" * 50)
    logger.info("TEST SUMMARY:")
    logger.info(f"  Backend:     {'✅ OK' if backend_ok else '❌ FAILED'}")
    logger.info(f"  Data Files:  {'✅ OK' if files_ok else '❌ FAILED'}")
    logger.info(f"  Attendance:  {'✅ OK' if attendance_ok else '❌ FAILED'}")
    logger.info("=" * 50)
    
    if all([backend_ok, files_ok, attendance_ok]):
        logger.info("\n✅ All systems ready! You can now run the camera service.")
        logger.info("   Make sure your webcam is connected.")
        logger.info("   Run: .\start_camera_service_venv.bat")
    else:
        logger.error("\n❌ Some systems are not ready. Fix the errors above.")

if __name__ == "__main__":
    main()
