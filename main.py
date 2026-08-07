import tkinter as tk
from tkinter import ttk
import sys
import os

# Import modules
from video_widgets import VideoWidget
from player import VideoPlayer
from controls import ControlPanel
from utils import format_time, get_supported_formats

class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Video Player")
        self.root.geometry("900x700")
        self.root.minsize(600, 500)
        
        # Configure style
        self.setup_styles()
        
        # Create video widget
        self.video_widget = VideoWidget(self.root, width=850, height=550)
        self.video_widget.frame.pack(padx=10, pady=(10, 5))
        
        # Progress bar and time display
        self.create_progress_bar()
        
        # Create player
        self.player = VideoPlayer(
            self.video_widget,
            status_callback=self.update_status
        )
        self.player.on_time_update = self.update_time_display
        self.player.on_frame_update = self.update_progress
        
        # Create control panel
        self.controls = ControlPanel(self.root, self.player)
        
        # Status bar
        self.create_status_bar()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_styles(self):
        """Setup application styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.root.configure(bg='#2b2b2b')
        
    def create_progress_bar(self):
        """Create progress bar and time display"""
        progress_frame = tk.Frame(self.root, bg='#2b2b2b')
        progress_frame.pack(fill=tk.X, padx=20, pady=(5, 10))
        
        # Time label
        self.time_label = tk.Label(progress_frame, text="00:00 / 00:00", 
                                   bg='#2b2b2b', fg='white', font=('Arial', 10))
        self.time_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Progress slider
        self.progress_var = tk.DoubleVar()
        self.progress_slider = tk.Scale(progress_frame, from_=0, to=1000, 
                                       orient=tk.HORIZONTAL, length=700,
                                       variable=self.progress_var,
                                       bg='#2b2b2b', fg='white',
                                       highlightthickness=0,
                                       command=self.seek_video)
        self.progress_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Duration label
        self.duration_label = tk.Label(progress_frame, text="", 
                                       bg='#2b2b2b', fg='white', font=('Arial', 10))
        self.duration_label.pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, 
                                   relief=tk.SUNKEN, anchor=tk.W,
                                   bg='#3c3c3c', fg='white',
                                   font=('Arial', 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<space>', lambda e: self.controls.toggle_play())
        self.root.bind('<Escape>', lambda e: self.controls.stop())
        self.root.bind('<Left>', lambda e: self.seek_video(self.progress_var.get() - 10))
        self.root.bind('<Right>', lambda e: self.seek_video(self.progress_var.get() + 10))
        self.root.bind('<Up>', lambda e: self.controls.volume_slider.set(
            min(100, self.controls.volume_slider.get() + 10)
        ))
        self.root.bind('<Down>', lambda e: self.controls.volume_slider.set(
            max(0, self.controls.volume_slider.get() - 10)
        ))
        self.root.bind('<o>', lambda e: self.controls.open_file())
        self.root.bind('<O>', lambda e: self.controls.open_file())
        
    def seek_video(self, value):
        """Seek video to position"""
        if isinstance(value, str):
            value = float(value)
        position = value / 1000.0
        self.player.seek(position)
        
    def update_progress(self, position):
        """Update progress bar"""
        self.progress_var.set(position * 1000)
        
    def update_time_display(self, current_time, total_time):
        """Update time display"""
        current_str = format_time(current_time)
        total_str = format_time(total_time)
        self.time_label.config(text=f"{current_str} / {total_str}")
        
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        
    def on_closing(self):
        """Handle window close"""
        self.player.cleanup()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()