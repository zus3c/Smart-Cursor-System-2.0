# ===================================================
# SECTION 1: Import Libraries
# ===================================================
import json
import sys

# ===================================================hook-dlib.py
# SECTION 2: Configuration Loader
# ===================================================
class load_config:
    """Handles configuration loading and validation"""
    
    DEFAULT_CONFIG = {
        "model_path": "shape_predictor_68_face_landmarks.dat",
        "webcam_index": 0,
        "sensitivity": 1.0
    }

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        
    def load(self):
        """Load and validate configuration"""
        try:
            with open(self.config_path) as f:
                user_config = json.load(f)
                self._validate_config(user_config)
                self.config.update(user_config)
                return self.config
        except FileNotFoundError:
            sys.exit(f"Config file {self.config_path} not found")
        except json.JSONDecodeError:
            sys.exit(f"Invalid JSON in {self.config_path}")

    def _validate_config(self, config):
        """Validate configuration structure"""
        required_keys = {"model_path", "sensitivity", "thresholds"}
        if not required_keys.issubset(config.keys()):
            sys.exit("Invalid configuration structure")