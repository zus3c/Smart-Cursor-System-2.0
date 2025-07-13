# ===================================================
# SECTION 1: Import Libraries
# ===================================================
import numpy as np

# ===================================================
# SECTION 2: Geometric Calculations
# ===================================================
def eye_aspect_ratio(eye_landmarks):
    """Calculate Eye Aspect Ratio (EAR)"""
    try:
        vertical1 = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        vertical2 = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        horizontal = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        return (vertical1 + vertical2) / (2.0 * horizontal)
    except Exception as e:
        print(f"EAR calculation error: {str(e)}")
        return 0.0

def mouth_aspect_ratio(mouth_landmarks):
    """Calculate Mouth Aspect Ratio (MAR)"""
    try:
        vertical = np.linalg.norm(mouth_landmarks[13] - mouth_landmarks[19])
        horizontal = np.linalg.norm(mouth_landmarks[0] - mouth_landmarks[6])
        return vertical / horizontal
    except Exception as e:
        print(f"MAR calculation error: {str(e)}")
        return 0.0