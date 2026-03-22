import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class RecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")
        self.root.geometry("250x120")
        self.process = None
        self.recording = False

        self.btn_record = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.btn_record.pack(pady=10)

        self.btn_stop = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.btn_stop.pack(pady=5)

        self.status = tk.Label(root, text="")
        self.status.pack(pady=5)

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        self.btn_record.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.status.config(text="Recording...")

        self.thread = threading.Thread(target=self._record)
        self.thread.daemon = True
        self.thread.start()

    def _record(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"recording_{timestamp}.mp4"
        # Use the exact device name (no quotes)
        audio_device = "Microphone (Realtek(R) Audio)"

        cmd = [
            "ffmpeg",
            "-f", "gdigrab",
            "-framerate", "30",
            "-i", "desktop",
            "-f", "dshow",
            "-i", f"audio={audio_device}",   # <-- key: no quotes
            "-c:v", "libx264",
            "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",
            output
        ]

        try:
            self.process = subprocess.Popen(cmd)
            self.process.wait()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self._reset_buttons(output))

    def stop_recording(self):
        if self.process and self.recording:
            self.process.terminate()
            self.recording = False

    def _reset_buttons(self, filename):
        self.btn_record.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.recording = False
        self.status.config(text=f"Saved: {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderApp(root)
    root.mainloop()