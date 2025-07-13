# ===================================================
# SECTION 1: Import Libraries
# ===================================================
import dlib
import cv2
import imutils
from imutils.video import VideoStream

# ===================================================
# SECTION 2: Face Tracking System
# ===================================================
class FaceTracker:
    """Real-time facial landmark detection"""
    
    def __init__(self, config):
        print(f"Initializing tracker with config: {config}")  # Debug line
        print(f"Webcam index type: {type(config['webcam_index'])}")  # Check type
        
        try:
            self.detector = dlib.get_frontal_face_detector()
            self.predictor = dlib.shape_predictor(config["model_path"])
            self.vs = VideoStream(src=config["webcam_index"]).start()
            self.frame = None
        except Exception as e:
            raise RuntimeError(f"Tracker initialization failed: {str(e)}")

    def toggle_tracking(self):
        webcam_index = self.cam_selector.get()
        print(f"Webcam index type: {type(webcam_index)}")  # Should be str
        print(f"Webcam index value: {webcam_index}")  # Should be "0", "1", etc.
        webcam_index = int(webcam_index)  # Convert to int 

    def get_landmarks(self):
        """Detect facial landmarks in current frame"""
        self.frame = self.vs.read()
        if self.frame is None:
            return None
            
        try:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)
            if len(faces) == 0:
                return None
            return self.predictor(gray, faces[0])
        except Exception as e:
            print(f"Landmark detection error: {str(e)}")
            return None

    def release(self):
        """Release resources"""
        self.vs.stop()