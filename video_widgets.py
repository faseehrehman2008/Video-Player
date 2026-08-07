import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

class VideoWidget:
    def __init__(self, parent, width=800, height=600):
        self.parent = parent
        self.width = width
        self.height = height
        
        # Create frame for video
        self.frame = tk.Frame(parent, bg='black', width=width, height=height)
        self.frame.pack_propagate(False)
        
        # Video display label
        self.video_label = tk.Label(self.frame, bg='black')
        self.video_label.pack(expand=True, fill=tk.BOTH)
        
        # Placeholder text
        self.show_placeholder()
        
    def show_placeholder(self):
        """Show placeholder when no video is loaded"""
        placeholder = Image.new('RGB', (self.width, self.height), color='black')
        self.update_frame(placeholder)
        
    def update_frame(self, image):
        """Update the displayed frame"""
        if isinstance(image, np.ndarray):
            # Convert OpenCV image to PIL
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
        
        # Resize to fit frame
        image.thumbnail((self.width, self.height), Image.Resampling.LANCZOS)
        
        # Create PhotoImage
        photo = ImageTk.PhotoImage(image)
        
        # Update label
        self.video_label.config(image=photo)
        self.video_label.image = photo
        
    def resize(self, width, height):
        """Resize the video widget"""
        self.width = width
        self.height = height
        self.frame.config(width=width, height=height)