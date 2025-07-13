# ===================================================
# SECTION 1: Import Libraries
# ===================================================
import cv2
import time

# ===================================================
# SECTION 2: Feedback Display System
# ===================================================
class Overlay:
    """Handles real-time visual feedback"""
    
    def __init__(self):
        self.fps = 0
        self.prev_time = time.time()
        
    def update(self, frame, gestures):
        """Draw overlays on frame"""
        try:
            # FPS Calculation
            curr_time = time.time()
            self.fps = 1 / (curr_time - self.prev_time)
            self.prev_time = curr_time

            # Status text
            cv2.putText(frame, f"FPS: {int(self.fps)}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if gestures.get("blink", False):
                cv2.putText(frame, "BLINK DETECTED", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            return frame
        except Exception as e:
            print(f"Overlay error: {str(e)}")
            return frame