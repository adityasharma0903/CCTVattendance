import cv2 
from deepface import DeepFace
import threading
import time
import numpy as np
import os

# ----------------------------------------------------------------------
# MULTI-FACE RECOGNITION SETUP
# ----------------------------------------------------------------------

# Dictionary to store authorized faces
authorized_faces = {}

def load_authorized_faces(image_paths):
    """
    Load multiple face images and generate embeddings
    
    Args:
        image_paths: Dictionary of {"Name": "path/to/image.jpg"}
    """
    print("\n" + "="*60)
    print("LOADING AUTHORIZED FACES")
    print("="*60)
    
    for name, path in image_paths.items():
        try:
            if not os.path.exists(path):
                print(f"❌ {name}: Image not found at {path}")
                continue
            
            img = cv2.imread(path)
            if img is None:
                print(f"❌ {name}: Could not read image")
                continue
            
            print(f"⏳ Processing {name}...")
            embedding = DeepFace.represent(img, model_name="ArcFace", enforce_detection=True)[0]["embedding"]
            authorized_faces[name] = embedding
            print(f"✅ {name}: Face loaded successfully")
            
        except Exception as e:
            print(f"❌ {name}: Error loading face - {e}")
    
    if len(authorized_faces) == 0:
        print("\n❌ ERROR: No authorized faces loaded!")
        exit()
    
    print(f"\n✅ Total authorized faces: {len(authorized_faces)}")
    print(f"   Names: {', '.join(authorized_faces.keys())}")
    print("="*60 + "\n")

# ----------------------------------------------------------------------
# CONFIGURE YOUR AUTHORIZED FACES HERE
# ----------------------------------------------------------------------
AUTHORIZED_FACES = {
    "Person1": r"aditya.jpg",
    # Add more faces below:
    # "Person2": r"path/to/person2.jpg",
    # "Person3": r"path/to/person3.jpg",
}

# Load all authorized faces
load_authorized_faces(AUTHORIZED_FACES)

counter = 0
face_match = False
matched_person = None
MODEL = "ArcFace"
is_processing = False

similarity_threshold = 0.5  # Adjust this (0.4-0.6 recommended)

# ----------------------------------------------------------------------
# FACE DETECTION AND RECOGNITION FUNCTION
# ----------------------------------------------------------------------

def detect_and_check_face(frame):
    """Detect faces and check against authorized faces using DeepFace"""
    global face_match, matched_person, is_processing
    
    if is_processing:
        return None
    
    is_processing = True
    detected_faces = []

    try:
        # Use DeepFace's built-in face detection
        face_objs = DeepFace.extract_faces(
            img_path=frame,
            detector_backend='opencv',  # Fast detector
            enforce_detection=False,
            align=True
        )
        
        if not face_objs or len(face_objs) == 0:
            face_match = False
            matched_person = None
            is_processing = False
            return None
        
        # Get the first detected face
        face_obj = face_objs[0]
        facial_area = face_obj['facial_area']
        
        # Extract face region with padding
        x = facial_area['x']
        y = facial_area['y']
        w = facial_area['w']
        h = facial_area['h']
        
        # Add padding
        padding = 20
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(frame.shape[1], x + w + padding)
        y2 = min(frame.shape[0], y + h + padding)
        
        face_roi = frame[y1:y2, x1:x2]
        
        # Get embedding for detected face
        rgb_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
        face_embedding = DeepFace.represent(
            rgb_face, 
            model_name=MODEL, 
            enforce_detection=False
        )[0]["embedding"]

        from numpy.linalg import norm
        from numpy import dot
        
        # Check against all authorized faces
        best_match = None
        best_similarity = 0
        
        for name, ref_embedding in authorized_faces.items():
            cosine_sim = dot(ref_embedding, face_embedding) / (norm(ref_embedding) * norm(face_embedding))
            
            if cosine_sim > best_similarity:
                best_similarity = cosine_sim
                best_match = name
        
        # Check if best match exceeds threshold
        face_match = best_similarity > similarity_threshold
        matched_person = best_match if face_match else None
        
        if face_match:
            print(f"🔍 Face Analysis: ✅ MATCH - {matched_person} (Similarity: {best_similarity:.4f})")
        else:
            print(f"🔍 Face Analysis: ❌ NO MATCH (Best: {best_match} - {best_similarity:.4f})")
        
        return (x1, y1, x2, y2)

    except Exception as e:
        print(f"❌ Error: {e}")
        face_match = False
        matched_person = None
        return None
    finally:
        is_processing = False

# ----------------------------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------------------------

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Cannot open webcam.")
    exit()

print("\n" + "="*60)
print("FACE RECOGNITION SYSTEM STARTED")
print("="*60)
print("Controls:")
print("  'q' - Quit")
print("="*60 + "\n")

face_bbox = None
last_detection_time = 0
detection_interval = 1.0  # Check every 1 second

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ih, iw, _ = frame.shape
        current_time = time.time()
        
        # Detect faces periodically
        if current_time - last_detection_time >= detection_interval:
            threading.Thread(
                target=lambda: globals().update({'face_bbox': detect_and_check_face(frame.copy())}),
                daemon=True
            ).start()
            last_detection_time = current_time

        # Draw bounding box if face detected
        if face_bbox is not None:
            x1, y1, x2, y2 = face_bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

        counter += 1

        # UI feedback
        if face_match:
            text = f"MATCH! {matched_person}"
            color = (0, 255, 0)
        elif face_bbox is not None:
            text = "NO MATCH!"
            color = (0, 0, 255)
        else:
            text = "NO FACE"
            color = (0, 0, 255)

        cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
        
        # Show authorized faces count
        auth_text = f"Authorized: {len(authorized_faces)} faces"
        cv2.putText(frame, auth_text, (20, ih - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow("Face Recognition System", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

except KeyboardInterrupt:
    print("\n\n⚠️  Program interrupted by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Face Recognition System stopped")