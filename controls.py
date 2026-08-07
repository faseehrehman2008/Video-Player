import tkinter as tk
from tkinter import ttk, filedialog

class ControlPanel:
    def __init__(self, parent, player):
        self.parent = parent
        self.player = player
        
        # Main control frame
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create controls
        self.create_controls()
        
    def create_controls(self):
        # Button frame
        button_frame = tk.Frame(self.frame)
        button_frame.pack()
        
        # Buttons
        self.open_btn = tk.Button(button_frame, text="📁 Open", 
                                  command=self.open_file, width=10)
        self.open_btn.pack(side=tk.LEFT, padx=2)
        
        self.play_btn = tk.Button(button_frame, text="▶ Play", 
                                  command=self.toggle_play, width=10)
        self.play_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_btn = tk.Button(button_frame, text="⏹ Stop", 
                                  command=self.stop, width=10)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        # Volume control
        tk.Label(button_frame, text="🔊").pack(side=tk.LEFT, padx=(20, 5))
        self.volume_var = tk.IntVar(value=50)
        self.volume_slider = tk.Scale(button_frame, from_=0, to=100, 
                                     orient=tk.HORIZONTAL, length=100,
                                     variable=self.volume_var,
                                     command=self.change_volume)
        self.volume_slider.pack(side=tk.LEFT, padx=5)
        
        # Speed control
        tk.Label(button_frame, text="Speed:").pack(side=tk.LEFT, padx=(20, 5))
        self.speed_var = tk.StringVar(value="1.0x")
        self.speed_combo = ttk.Combobox(button_frame, textvariable=self.speed_var,
                                        values=["0.5x", "0.75x", "1.0x", "1.25x", "1.5x", "2.0x"],
                                        width=6, state="readonly")
        self.speed_combo.pack(side=tk.LEFT, padx=5)
        self.speed_combo.bind('<<ComboboxSelected>>', self.change_speed)
        
    def open_file(self):
        """Open file dialog to select video"""
        filetypes = (
            ('Video files', '*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm'),
            ('All files', '*.*')
        )
        file_path = filedialog.askopenfilename(title='Select Video', 
                                              filetypes=filetypes)
        if file_path:
            self.player.load_video(file_path)
            
    def toggle_play(self):
        """Toggle play/pause"""
        if self.player.video_loaded:
            if self.player.is_playing:
                self.player.pause()
                self.play_btn.config(text="▶ Play")
            else:
                self.player.play()
                self.play_btn.config(text="⏸ Pause")
        else:
            self.open_file()
            
    def stop(self):
        """Stop video playback"""
        self.player.stop()
        self.play_btn.config(text="▶ Play")
        
    def change_volume(self, value):
        """Change volume level"""
        self.player.set_volume(int(value))
        
    def change_speed(self, event):
        """Change playback speed"""
        speed = float(self.speed_var.get().replace('x', ''))
        self.player.set_speed(speed)
        
    def update_play_button(self, playing):
        """Update play button state"""
        if playing:
            self.play_btn.config(text="⏸ Pause")
        else:
            self.play_btn.config(text="▶ Play")