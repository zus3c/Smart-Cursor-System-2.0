# ===================================================
# SECTION 1: Import Libraries
# ===================================================
import pyautogui
import numpy as np
import cv2

# ===================================================
# SECTION 2: Kalman Filter Implementation
# ===================================================
class KalmanFilter:
    """Smoothing filter for cursor movements"""
    
    def __init__(self, process_noise=1e-4, measurement_noise=1e-1):
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]], np.float32)
        self.kf.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]], np.float32)
        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * process_noise
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * measurement_noise

    def update(self, x, y):
        measurement = np.array([[x], [y]], dtype=np.float32)
        self.kf.correct(measurement)
        predicted = self.kf.predict()
        return (predicted[0][0], predicted[1][0])

# ===================================================
# SECTION 3: Cursor Controller
# ===================================================
class CursorController:
    """Handles mouse movement and actions"""
    
    def __init__(self, config):
        self.screen_w, self.screen_h = pyautogui.size()
        self.sensitivity = config["sensitivity"]
        self.filter = KalmanFilter() if config["smoothing"]["enabled"] else None

    def move(self, x, y):
        """Move cursor with optional smoothing"""
        try:
            if self.filter:
                x, y = self.filter.update(x, y)
            pyautogui.moveTo(
                x * self.sensitivity,
                y * self.sensitivity,
                duration=0
            )
        except pyautogui.FailSafeException:
            print("Cursor movement out of bounds")