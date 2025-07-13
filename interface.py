# ===================================================
# SECTION 1: Import Libraries
# ===================================================
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import sys
from main import SmartCursor  # Modified main.py

# ===================================================
# SECTION 2: GUI Constants and Configuration
# ===================================================
FONT_PRIMARY = ("Segoe UI", 10)
COLOR_BG = "#f0f0f0"
UPDATE_INTERVAL_MS = 100

class SmartCursor:
    """Main GUI controller with threaded backend integration"""
    
    def __init__(self, root):
        # ===================================================
        # SECTION 3: GUI Initialization
        # ===================================================
        self.root = root
        self.root.title("Smart Cursor System")
        self.root.geometry("600x500")
        self.root.configure(bg=COLOR_BG)
        
        self.app = None
        self.running = False
        self.message_queue = queue.Queue()
        
        self._init_ui()
        self._start_polling()

    def toggle_tracking(self):
    #Handle start/stop of tracking thread
        if not self.running:
            try:
                # Ensure webcam_index is integer, not string
                webcam_index = int(self.cam_selector.get())
                self.app = SmartCursor(webcam_index)  # Pass as integer
                self._start_tracking()
            except ValueError as e:
                self.log(f"Invalid webcam index: {str(e)}", error=True)

    def _init_ui(self):
        # ===================================================
        # SECTION 4: UI Components
        # ===================================================
        # Webcam Selection
        self.cam_frame = ttk.LabelFrame(self.root, text="Webcam Configuration")
        self.cam_selector = ttk.Combobox(self.cam_frame, values=["0", "1", "2", "3"])
        self.cam_selector.current(0)
        self.cam_selector.pack(padx=10, pady=5)
        self.cam_frame.pack(fill="x", padx=10, pady=5)

        # Controls
        self.control_frame = ttk.LabelFrame(self.root, text="System Controls")
        self.btn_start = ttk.Button(self.control_frame, text="Start Tracking", command=self.toggle_tracking)
        self.btn_start.pack(side="left", padx=5)
        ttk.Button(self.control_frame, text="Exit", command=self.clean_shutdown).pack(side="right", padx=5)
        self.control_frame.pack(fill="x", padx=10, pady=5)

        # Sensitivity Controls
        self.sens_frame = ttk.LabelFrame(self.root, text="Sensitivity Settings")
        self.sens_slider = ttk.Scale(self.sens_frame, from_=0.5, to=3.0, command=self.update_sensitivity)
        self.sens_slider.set(1.5)
        self.sens_slider.pack(padx=10, pady=5, fill="x")
        self.sens_frame.pack(fill="x", padx=10, pady=5)

        # Gesture Toggles
        self.gesture_frame = ttk.LabelFrame(self.root, text="Gesture Controls")
        self.blink_toggle = ttk.Checkbutton(self.gesture_frame, text="Enable Blink Detection")
        self.blink_toggle.pack(side="left", padx=5)
        self.wink_toggle = ttk.Checkbutton(self.gesture_frame, text="Enable Wink Detection")
        self.wink_toggle.pack(side="left", padx=5)
        self.gesture_frame.pack(fill="x", padx=10, pady=5)

        # Status Log
        self.log_frame = ttk.LabelFrame(self.root, text="System Status")
        self.log_text = tk.Text(self.log_frame, height=8, state="disabled")
        self.scrollbar = ttk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.log_text.pack(fill="both", expand=True)
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # ===================================================
    # SECTION 5: Backend Integration
    # ===================================================
    def toggle_tracking(self):
        """Handle start/stop of tracking thread"""
        if not self.running:
            self._start_tracking()
        else:
            self._stop_tracking()

    def _start_tracking(self):
        """Initialize and start tracking thread"""
        try:
            self.app = SmartCursor(int(self.cam_selector.get()))
            self.thread = threading.Thread(target=self.app.run, daemon=True)
            self.running = True
            self.thread.start()
            self.btn_start.config(text="Stop Tracking")
            self.log("System STARTED")
        except Exception as e:
            self.log(f"Error: {str(e)}", error=True)

    def _stop_tracking(self):
        """Gracefully stop tracking"""
        self.running = False
        if self.app:
            self.app.tracker.release()
        self.btn_start.config(text="Start Tracking")
        self.log("System STOPPED")

    # ===================================================
    # SECTION 6: Utility Methods
    # ===================================================
    def update_sensitivity(self, val):
        """Handle sensitivity slider updates"""
        if self.app:
            self.app.cursor.sensitivity = float(val)

    def log(self, message, error=False):
        """Thread-safe logging to GUI"""
        self.message_queue.put((message, error))
        
    def _start_polling(self):
        """Periodic UI update from queue"""
        while not self.message_queue.empty():
            msg, err = self.message_queue.get()
            self.log_text.configure(state="normal")
            self.log_text.insert("end", f"{msg}\n")
            if err:
                self.log_text.tag_add("error", "end-1l", "end")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        self.root.after(UPDATE_INTERVAL_MS, self._start_polling)

    def clean_shutdown(self):
        """Ensure resources are released"""
        self._stop_tracking()
        self.root.destroy()

# ===================================================
# SECTION 7: Main Execution
# ===================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCursor(root)
    root.mainloop()