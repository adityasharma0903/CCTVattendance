import cv2
from deepface import DeepFace
import json
import os
import numpy as np
from datetime import datetime, time
import time as time_module
import requests
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_DIR = "../data"
STUDENTS_DB_FILE = "../iotproject/students_database.json"
BACKEND_API = "http://localhost:8000/api"

SIMILARITY_THRESHOLD = 0.5
MODEL = "ArcFace"
DETECTION_INTERVAL = 2.0
ATTENDANCE_COOLDOWN = 30  # Seconds cooldown between camera detections (database check handles duplicates)
TEST_MODE_ALWAYS_ACTIVE = False  # False = only mark during scheduled time, True = always mark
PROCESS_EVERY_N_FRAMES = 15  # Reduce heavy DeepFace calls

# ============================================================================
# UTILITIES
# ============================================================================

def load_json_file(filepath):
    """Load JSON file"""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return {}

def load_from_data_dir(filename):
    """Load from data directory"""
    return load_json_file(os.path.join(DATA_DIR, filename))

# ============================================================================
# STUDENT FACE DATABASE
# ============================================================================

class FaceDatabase:
    def __init__(self):
        self.students = {}
        self.embeddings = {}
        self.load_students()
    
    def load_students(self):
        """Load student embeddings from database"""
        self.students = load_json_file(STUDENTS_DB_FILE)
        logger.info(f"✅ Loaded {len(self.students)} students from database")
        
        for roll, student_data in self.students.items():
            if "embedding" in student_data:
                self.embeddings[roll] = np.array(student_data["embedding"])
    
    def get_student_by_roll(self, roll_number):
        """Get student info by roll number"""
        return self.students.get(roll_number)
    
    def get_all_embeddings(self):
        """Get all student embeddings"""
        return self.embeddings

# ============================================================================
# CAMERA ATTENDANCE
# ============================================================================

class CameraAttendance:
    def __init__(self, camera_id, camera_name, batch_id):
        self.camera_id = camera_id
        self.camera_name = camera_name
        self.batch_id = batch_id
        self.face_db = FaceDatabase()
        self.last_marked = {}  # {"roll_number": timestamp}
        self.is_recording = False
        self.last_schedule_log = None
    
    def get_current_schedule(self):
        """Get current class schedule for this camera"""
        current_day = datetime.now().strftime("%A")
        current_time = datetime.now().time()
        
        # Load timetable and camera schedule
        camera_schedule = load_from_data_dir("camera_schedule.json").get("camera_schedule", [])
        timetable_data = load_from_data_dir("timetable.json").get("timetable", [])
        
        # Find active schedules for this camera
        active_schedule = None
        
        for schedule in camera_schedule:
            if schedule.get("camera_id") == self.camera_id and schedule.get("is_active"):
                timetable_id = schedule.get("timetable_id")
                
                # Find corresponding timetable entry
                for tt in timetable_data:
                    if tt.get("timetable_id") == timetable_id:
                        if tt.get("day") == current_day:
                            start_time = datetime.strptime(tt.get("start_time"), "%H:%M").time()
                            end_time = datetime.strptime(tt.get("end_time"), "%H:%M").time()
                            
                            if start_time <= current_time <= end_time:
                                active_schedule = {
                                    "subject_id": tt.get("subject_id"),
                                    "teacher_id": tt.get("teacher_id"),
                                    "start_time": start_time,
                                    "end_time": end_time
                                }
                                break
        
        if active_schedule:
            return active_schedule

        # Test mode: allow attendance even without active schedule
        if TEST_MODE_ALWAYS_ACTIVE:
            if camera_schedule and timetable_data:
                # Try to use the first linked timetable entry for subject/teacher
                for schedule in camera_schedule:
                    if schedule.get("camera_id") == self.camera_id and schedule.get("is_active"):
                        timetable_id = schedule.get("timetable_id")
                        for tt in timetable_data:
                            if tt.get("timetable_id") == timetable_id:
                                return {
                                    "subject_id": tt.get("subject_id"),
                                    "teacher_id": tt.get("teacher_id"),
                                    "start_time": datetime.strptime("00:00", "%H:%M").time(),
                                    "end_time": datetime.strptime("23:59", "%H:%M").time()
                                }

        # Log once every 30 seconds when no schedule found
        now = datetime.now()
        if not self.last_schedule_log or (now - self.last_schedule_log).total_seconds() > 30:
            logger.warning(f"⏱️ No active schedule for {self.camera_name} at {current_day} {current_time.strftime('%H:%M:%S')}")
            self.last_schedule_log = now

        return None
    
    def detect_faces_in_frame(self, frame):
        """Detect and recognize faces in frame"""
        try:
            # Get all student embeddings
            embeddings_db = self.face_db.get_all_embeddings()
            
            if not embeddings_db:
                logger.warning("No student embeddings in database")
                return []
            
            # Get frame embedding
            try:
                result = DeepFace.represent(frame, model_name=MODEL, enforce_detection=True)
                if not result:
                    return []
                
                frame_embedding = np.array(result[0]["embedding"])
            except Exception as e:
                logger.debug(f"No face detected in frame: {e}")
                return []
            
            # Compare with all students
            recognized_students = []
            
            for roll_number, student_embedding in embeddings_db.items():
                # Calculate cosine similarity
                similarity = np.dot(frame_embedding, student_embedding) / (
                    np.linalg.norm(frame_embedding) * np.linalg.norm(student_embedding)
                )
                
                if similarity >= SIMILARITY_THRESHOLD:
                    student = self.face_db.get_student_by_roll(roll_number)
                    recognized_students.append({
                        "roll_number": roll_number,
                        "name": student.get("name"),
                        "similarity": float(similarity)
                    })
            
            return recognized_students
        
        except Exception as e:
            logger.error(f"Error detecting faces: {e}")
            return []
    
    def mark_attendance(self, roll_number, confidence_score, current_schedule):
        """Mark attendance for a student"""
        current_time = datetime.now()
        last_mark_time = self.last_marked.get(roll_number)
        
        # Check cooldown
        if last_mark_time:
            time_diff = (current_time - last_mark_time).total_seconds()
            if time_diff < ATTENDANCE_COOLDOWN:
                logger.debug(f"Cooldown active for {roll_number}")
                return False
        
        # Check if already marked for this class today
        schedule = current_schedule
        student = self.face_db.get_student_by_roll(roll_number)
        
        if not student or not schedule:
            return False
        
        try:
            # Check existing attendance for today
            today = datetime.now().strftime("%Y-%m-%d")
            check_url = f"{BACKEND_API}/attendance-check"
            params = {
                "roll_number": roll_number,
                "date": today,
                "subject_id": schedule.get("subject_id"),
                "batch_id": self.batch_id
            }
            
            logger.info(f"🔍 Checking existing attendance: {params}")
            response = requests.get(check_url, params=params, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"📋 Check response: {result}")
                
                if isinstance(result, dict) and result.get("exists"):
                    logger.info(f"⚠️ {student.get('name')} already marked for this class today")
                    return False
                else:
                    logger.info(f"✅ No existing attendance found, proceeding to mark")
            else:
                logger.warning(f"Backend check failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Could not check existing attendance (network error): {e}")
        except Exception as e:
            logger.warning(f"Could not check existing attendance: {e}")
            logger.info(f"Response content: {response.text if 'response' in locals() else 'No response'}")
        
        # Determine status
        schedule = current_schedule
        student = self.face_db.get_student_by_roll(roll_number)
        
        if not student or not schedule:
            return False
        
        current_time_obj = datetime.now().time()
        start_time = schedule.get("start_time")
        
        # Check if late (5 minutes after start)
        late_time = (datetime.combine(datetime.today(), start_time).timestamp() + 300)
        current_timestamp = datetime.combine(datetime.today(), current_time_obj).timestamp()
        
        status = "LATE" if current_timestamp > late_time else "PRESENT"
        
        # Send to backend API
        attendance_data = {
            "student_id": f"STU_{roll_number}",
            "roll_number": roll_number,
            "camera_id": self.camera_id,
            "timestamp": current_time.isoformat(),
            "subject_id": schedule.get("subject_id"),
            "batch_id": self.batch_id,
            "status": status,
            "confidence_score": confidence_score
        }
        
        try:
            response = requests.post(f"{BACKEND_API}/attendance", json=attendance_data)
            if response.status_code == 200:
                time_slot = f"{schedule.get('start_time').strftime('%H:%M')}-{schedule.get('end_time').strftime('%H:%M')}"
                logger.info(f"✅ Attendance Marked: {student.get('name')} ({roll_number}) - {status}")
                logger.info(f"   📚 Subject: {schedule.get('subject_id')} | ⏰ Time Slot: {time_slot}")
                self.last_marked[roll_number] = current_time
                return True
            else:
                logger.error(f"Failed to mark attendance: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending attendance to API: {e}")
            return False
    
    def process_frame(self, frame):
        """Process a single frame"""
        schedule = self.get_current_schedule()
        
        if not schedule:
            return {"status": "no_schedule"}
        
        # Detect faces
        recognized = self.detect_faces_in_frame(frame)
        
        if recognized:
            logger.info(f"🔎 Detected {len(recognized)} face(s) in frame")
            for student in recognized:
                logger.info(f"   -> {student['name']} (similarity: {student['similarity']:.2f})")
                marked = self.mark_attendance(
                    student["roll_number"],
                    student["similarity"],
                    schedule
                )
                if marked:
                    # Add visual indicator on frame
                    return {"status": "marked", "student": student}
            return {"status": "recognized", "recognized": recognized}

        return {"status": "no_face"}
    
    def find_available_camera(self):
        """Find available camera on system"""
        logger.info("🔍 Searching for available cameras...")
        
        # Try multiple camera indices
        for camera_index in range(10):
            cap = cv2.VideoCapture(camera_index)
            if cap.isOpened():
                # Try to read a frame
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None:
                    logger.info(f"✅ Found camera at index {camera_index}")
                    return camera_index
        
        logger.error("❌ No camera found!")
        return None
    
    def start_camera_stream(self, camera_source=0):
        """Start camera stream and process attendance"""
        logger.info(f"🎥 Starting camera {self.camera_name}...")
        
        # Find available camera
        actual_camera = self.find_available_camera()
        if actual_camera is None:
            logger.error("❌ No camera available. Please check:")
            logger.error("   1. Webcam is connected")
            logger.error("   2. No other app is using the camera")
            logger.error("   3. Windows permissions allow camera access")
            return
        
        # Use DirectShow on Windows for better compatibility
        cap = cv2.VideoCapture(actual_camera, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            logger.error(f"Failed to open camera {actual_camera}")
            return
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.is_recording = True
        frame_count = 0
        consecutive_failures = 0
        last_detection = None
        
        try:
            logger.info(f"✅ Camera {actual_camera} opened successfully!")
            while self.is_recording and consecutive_failures < 30:
                ret, frame = cap.read()
                
                if not ret:
                    consecutive_failures += 1
                    continue
                
                consecutive_failures = 0
                frame_count += 1
                
                # Flip frame for mirror effect
                frame = cv2.flip(frame, 1)
                
                detection_result = None
                # Process every Nth frame to reduce processing load
                if frame_count % PROCESS_EVERY_N_FRAMES == 0:
                    detection_result = self.process_frame(frame)
                
                # Display frame with info
                cv2.putText(frame, f"Camera: {self.camera_name}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Frame: {frame_count}", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Show detection results
                if detection_result:
                    status = detection_result.get("status")
                    if status == "marked":
                        student = detection_result.get("student", {})
                        name = student.get("name", "Unknown")
                        cv2.putText(frame, f"✅ ATTENDANCE MARKED: {name}", (10, 110),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
                        last_detection = datetime.now()
                    elif status == "recognized":
                        count = len(detection_result.get("recognized", []))
                        cv2.putText(frame, f"🔎 Detected {count} face(s)", (10, 110),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    elif status == "no_schedule":
                        cv2.putText(frame, "⏱️ No active schedule", (10, 110),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Show message to quit
                cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
                
                cv2.imshow(f"Camera - {self.camera_name}", frame)
                
                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # Yield to avoid UI freeze
                time_module.sleep(0.01)
        
        except Exception as e:
            logger.error(f"Error processing camera stream: {e}")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.is_recording = False
            logger.info(f"🛑 Stopped camera {self.camera_name}")
    
    def stop(self):
        """Stop camera recording"""
        self.is_recording = False

# ============================================================================
# SCHEDULER
# ============================================================================

class AttendanceScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.camera_threads = {}
        self.cameras = {}
    
    def load_camera_config(self):
        """Load camera configuration"""
        cameras_data = load_from_data_dir("cameras.json").get("cameras", [])
        return cameras_data
    
    def initialize_cameras(self):
        """Initialize camera objects"""
        cameras = self.load_camera_config()
        
        for camera in cameras:
            if camera.get("is_active"):
                camera_id = camera.get("camera_id")
                camera_name = camera.get("camera_name")
                batch_id = camera.get("batch_id")
                
                self.cameras[camera_id] = CameraAttendance(camera_id, camera_name, batch_id)
                logger.info(f"✅ Initialized camera: {camera_name}")
    
    def start_all_cameras(self):
        """Start all active cameras"""
        self.initialize_cameras()
        
        for camera_id, camera_obj in self.cameras.items():
            # Start each camera in separate thread
            thread = threading.Thread(target=camera_obj.start_camera_stream, daemon=True)
            self.camera_threads[camera_id] = thread
            thread.start()
    
    def start(self):
        """Start the scheduler"""
        logger.info("🚀 Starting Attendance Scheduler...")
        self.start_all_cameras()
        
        # Start background scheduler
        self.scheduler.start()
        logger.info("✅ Scheduler started successfully")
    
    def stop(self):
        """Stop the scheduler"""
        logger.info("🛑 Stopping Scheduler...")
        self.scheduler.shutdown()
        
        for camera_obj in self.cameras.values():
            camera_obj.stop()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    scheduler = AttendanceScheduler()
    
    try:
        scheduler.start()
        logger.info("Press Ctrl+C to stop...")
        while True:
            time_module.sleep(1)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
        scheduler.stop()
        logger.info("✅ Scheduler stopped")
