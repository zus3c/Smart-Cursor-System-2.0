# ===================================================
# SECTION 1: Main Application Controller
# ===================================================
from tracking import FaceTracker
from cursor_control import CursorController
from gestures import GestureDetector
from overlay import Overlay
from config import load_config
import threading

class SmartCursor:
    """Central controller for facial tracking system"""
    
    def __init__(self, webcam_index=0):
        self.config = load_config()
        self.config['webcam_index'] = webcam_index
        self.tracker = FaceTracker(self.config)
        self.cursor = CursorController(self.config)
        self.gestures = GestureDetector(self.config)
        self.overlay = OverlaySystem()
        self.running = False

    def start_tracking(self):
        """Initialize tracking thread"""
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        """Main processing loop"""
        while self.running:
            frame = self.tracker.get_frame()
            landmarks = self.tracker.get_landmarks()
            
            if landmarks:
                gestures = self.gestures.detect(landmarks)
                self.cursor.update_position(landmarks[30])
                self.overlay.update(frame, gestures)

    def stop_tracking(self):
        """Graceful shutdown"""
        self.running = False
        self.tracker.release()