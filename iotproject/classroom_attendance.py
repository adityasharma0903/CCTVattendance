import cv2 
from deepface import DeepFace
import json
import os
from datetime import datetime
import time
import threading
import numpy as np

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------

STUDENTS_DB_FILE = "students_database.json"
ATTENDANCE_LOG_FILE = "attendance_log.json"
STUDENT_IMAGES_FOLDER = "student_images"
ATTENDANCE_COOLDOWN = 300  # 5 minutes (prevent duplicate entries)

# Face recognition settings
MODEL = "ArcFace"
SIMILARITY_THRESHOLD = 0.5
DETECTION_INTERVAL = 2.0  # Check every 2 seconds

# ----------------------------------------------------------------------
# DATABASE MANAGEMENT
# ----------------------------------------------------------------------

class StudentDatabase:
    def __init__(self):
        self.students = {}
        self.load_database()
    
    def load_database(self):
        """Load student database from JSON file"""
        if os.path.exists(STUDENTS_DB_FILE):
            with open(STUDENTS_DB_FILE, 'r') as f:
                data = json.load(f)
                self.students = data
            print(f"✅ Loaded {len(self.students)} students from database")
        else:
            print("⚠️  No existing database found. Creating new one.")
            self.students = {}
    
    def save_database(self):
        """Save student database to JSON file"""
        with open(STUDENTS_DB_FILE, 'w') as f:
            json.dump(self.students, f, indent=2)
        print(f"✅ Database saved with {len(self.students)} students")
    
    def add_student(self, roll_number, name, image_path):
        """Add a new student to the database"""
        try:
            if not os.path.exists(image_path):
                print(f"❌ Image not found: {image_path}")
                return False
            
            img = cv2.imread(image_path)
            if img is None:
                print(f"❌ Could not read image: {image_path}")
                return False
            
            print(f"⏳ Processing {name} (Roll: {roll_number})...")
            embedding = DeepFace.represent(img, model_name=MODEL, enforce_detection=True)[0]["embedding"]
            
            self.students[roll_number] = {
                "name": name,
                "roll_number": roll_number,
                "image_path": image_path,
                "embedding": embedding,
                "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"✅ {name} added successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error adding {name}: {e}")
            return False
    
    def get_all_students(self):
        """Get list of all students"""
        return [(data['roll_number'], data['name']) for roll, data in self.students.items()]

# ----------------------------------------------------------------------
# ATTENDANCE MANAGEMENT
# ----------------------------------------------------------------------

class AttendanceManager:
    def __init__(self):
        self.attendance_log = []
        self.last_marked = {}  # Track when each student was last marked
        self.load_attendance()
    
    def load_attendance(self):
        """Load attendance log from JSON file"""
        if os.path.exists(ATTENDANCE_LOG_FILE):
            with open(ATTENDANCE_LOG_FILE, 'r') as f:
                self.attendance_log = json.load(f)
            print(f"✅ Loaded {len(self.attendance_log)} attendance records")
        else:
            print("⚠️  No existing attendance log found. Creating new one.")
            self.attendance_log = []
    
    def save_attendance(self):
        """Save attendance log to JSON file"""
        with open(ATTENDANCE_LOG_FILE, 'w') as f:
            json.dump(self.attendance_log, f, indent=2)
    
    def mark_attendance(self, roll_number, name):
        """Mark attendance for a student"""
        current_time = time.time()
        
        # Check cooldown
        if roll_number in self.last_marked:
            time_since_last = current_time - self.last_marked[roll_number]
            if time_since_last < ATTENDANCE_COOLDOWN:
                remaining = ATTENDANCE_COOLDOWN - time_since_last
                print(f"⏳ {name} already marked. Cooldown: {remaining/60:.1f} minutes remaining")
                return False
        
        # Mark attendance
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_only = datetime.now().strftime("%Y-%m-%d")
        
        record = {
            "roll_number": roll_number,
            "name": name,
            "timestamp": timestamp,
            "date": date_only
        }
        
        self.attendance_log.append(record)
        self.last_marked[roll_number] = current_time
        self.save_attendance()
        
        print(f"✅ ATTENDANCE MARKED: {name} (Roll: {roll_number}) at {timestamp}")
        return True
    
    def get_today_attendance(self):
        """Get today's attendance"""
        today = datetime.now().strftime("%Y-%m-%d")
        return [record for record in self.attendance_log if record['date'] == today]
    
    def get_attendance_by_date(self, date):
        """Get attendance for a specific date (YYYY-MM-DD)"""
        return [record for record in self.attendance_log if record['date'] == date]

# ----------------------------------------------------------------------
# FACE RECOGNITION ENGINE
# ----------------------------------------------------------------------

class FaceRecognitionEngine:
    def __init__(self, student_db, attendance_manager):
        self.student_db = student_db
        self.attendance_manager = attendance_manager
        self.is_processing = False
        self.last_match = None
        self.last_detection_time = 0
    
    def recognize_face(self, frame):
        """Detect and recognize faces in the frame"""
        if self.is_processing:
            return None
        
        self.is_processing = True
        result = None
        
        try:
            # Detect faces using DeepFace
            face_objs = DeepFace.extract_faces(
                img_path=frame,
                detector_backend='opencv',
                enforce_detection=False,
                align=True
            )
            
            if not face_objs or len(face_objs) == 0:
                self.is_processing = False
                return None
            
            # Process first detected face
            face_obj = face_objs[0]
            facial_area = face_obj['facial_area']
            
            x = facial_area['x']
            y = facial_area['y']
            w = facial_area['w']
            h = facial_area['h']
            
            # Extract face ROI with padding
            padding = 20
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(frame.shape[1], x + w + padding)
            y2 = min(frame.shape[0], y + h + padding)
            
            face_roi = frame[y1:y2, x1:x2]
            
            # Get embedding
            rgb_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
            face_embedding = DeepFace.represent(
                rgb_face, 
                model_name=MODEL, 
                enforce_detection=False
            )[0]["embedding"]
            
            # Compare with all students
            best_match_roll = None
            best_match_name = None
            best_similarity = 0
            
            for roll, student_data in self.student_db.students.items():
                ref_embedding = student_data['embedding']
                
                # Calculate cosine similarity
                from numpy.linalg import norm
                from numpy import dot
                cosine_sim = dot(ref_embedding, face_embedding) / (norm(ref_embedding) * norm(face_embedding))
                
                if cosine_sim > best_similarity:
                    best_similarity = cosine_sim
                    best_match_roll = roll
                    best_match_name = student_data['name']
            
            # Check if match exceeds threshold
            if best_similarity > SIMILARITY_THRESHOLD:
                self.last_match = {
                    'roll': best_match_roll,
                    'name': best_match_name,
                    'similarity': best_similarity,
                    'bbox': (x1, y1, x2, y2)
                }
                
                # Mark attendance
                self.attendance_manager.mark_attendance(best_match_roll, best_match_name)
                
                result = self.last_match
            else:
                self.last_match = None
                result = None
        
        except Exception as e:
            print(f"❌ Recognition Error: {e}")
        finally:
            self.is_processing = False
        
        return result

# ----------------------------------------------------------------------
# MAIN CLASSROOM ATTENDANCE SYSTEM
# ----------------------------------------------------------------------

def main():
    print("\n" + "="*70)
    print("       CLASSROOM ATTENDANCE SYSTEM - FACE RECOGNITION")
    print("="*70)
    
    # Initialize components
    student_db = StudentDatabase()
    attendance_manager = AttendanceManager()
    recognition_engine = FaceRecognitionEngine(student_db, attendance_manager)
    
    # Check if students are registered
    if len(student_db.students) == 0:
        print("\n⚠️  WARNING: No students registered in the system!")
        print("   Please run the setup script to add students first.")
        print("   Run: python setup_students.py")
        return
    
    print(f"\n📚 Students Registered: {len(student_db.students)}")
    for roll, name in student_db.get_all_students():
        print(f"   • {name} (Roll: {roll})")
    
    # Show today's attendance
    today_attendance = attendance_manager.get_today_attendance()
    print(f"\n📊 Today's Attendance: {len(today_attendance)} students")
    
    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ ERROR: Cannot open camera.")
        return
    
    print("\n" + "="*70)
    print("SYSTEM STARTED - Monitoring for faces...")
    print("="*70)
    print("Controls:")
    print("  'q' - Quit")
    print("  's' - Show today's attendance")
    print("  'r' - Generate Excel report")
    print("="*70 + "\n")
    
    last_recognition_time = 0
    current_match = None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            ih, iw = frame.shape[:2]
            current_time = time.time()
            
            # Perform face recognition periodically
            if current_time - last_recognition_time >= DETECTION_INTERVAL:
                def recognize():
                    global current_match
                    current_match = recognition_engine.recognize_face(frame.copy())
                
                threading.Thread(target=recognize, daemon=True).start()
                last_recognition_time = current_time
            
            # Draw UI
            if current_match:
                # Draw bounding box
                x1, y1, x2, y2 = current_match['bbox']
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Show name and roll number
                text = f"{current_match['name']} (Roll: {current_match['roll']})"
                similarity_text = f"Match: {current_match['similarity']:.2%}"
                
                cv2.putText(frame, text, (x1, y1-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, similarity_text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                status_text = "RECOGNIZED"
                color = (0, 255, 0)
            else:
                status_text = "SCANNING..."
                color = (0, 165, 255)
            
            # Status text
            cv2.putText(frame, status_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            
            # Show stats
            stats_text = f"Students: {len(student_db.students)} | Today: {len(attendance_manager.get_today_attendance())}"
            cv2.putText(frame, stats_text, (20, ih - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow("Classroom Attendance System", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                print("\n" + "="*50)
                print("TODAY'S ATTENDANCE:")
                print("="*50)
                today = attendance_manager.get_today_attendance()
                for i, record in enumerate(today, 1):
                    print(f"{i}. {record['name']} (Roll: {record['roll_number']}) - {record['timestamp']}")
                print("="*50 + "\n")
            elif key == ord('r'):
                print("\n⏳ Generating Excel report...")
                from attendance_report import generate_excel_report
                generate_excel_report(attendance_manager, student_db)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  System interrupted by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✅ System stopped")

if __name__ == "__main__":
    main()


    