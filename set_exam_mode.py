"""
Quick script to set camera mode to EXAM for phone detection
"""
import requests

BACKEND_API = "http://localhost:8000/api"

def set_exam_mode(camera_id="CAM001"):
    """Set camera to EXAM mode"""
    try:
        response = requests.post(
            f"{BACKEND_API}/camera-mode",
            json={"camera_id": camera_id, "mode": "EXAM"}
        )
        if response.status_code == 200:
            print(f"✅ Camera {camera_id} set to EXAM mode!")
            print(f"📱 Phone detection is now ACTIVE")
            print(f"🔥 Show phone to camera - instant alert will trigger!")
        else:
            print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure backend is running!")

if __name__ == "__main__":
    set_exam_mode()
