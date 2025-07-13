# ===================================================
# SECTION 1: Import Libraries
# ===================================================
from utils import eye_aspect_ratio, mouth_aspect_ratio

# ===================================================
# SECTION 2: Gesture Detection Engine
# ===================================================
class GestureDetector:
    """Recognizes facial gestures using EAR/MAR"""
    
    def __init__(self, config):
        self.thresholds = config["thresholds"]
        self.counters = {
            "blink": 0,
            "wink": 0,
            "mouth": 0
        }

    def detect(self, landmarks):
        """Main detection entry point"""
        try:
            left_eye = landmarks[36:42]
            right_eye = landmarks[42:48]
            mouth = landmarks[48:68]

            return {
                "blink": self._check_blink(left_eye, right_eye),
                "right_wink": self._check_wink(left_eye, right_eye),
                "mouth_open": self._check_mouth(mouth)
            }
        except IndexError:
            print("Invalid landmark indices")
            return {}

    def _check_blink(self, left_eye, right_eye):
        ear_left = eye_aspect_ratio(left_eye)
        ear_right = eye_aspect_ratio(right_eye)
        if (ear_left + ear_right)/2 < self.thresholds["ear_blink"]:
            self.counters["blink"] += 1
            if self.counters["blink"] >= 3:
                self.counters["blink"] = 0
                return True
        return False