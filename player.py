import cv2
import threading
import time
from utils import format_time, get_video_duration  # This now works

class VideoPlayer:
    def __init__(self, video_widget, status_callback=None):
        self.video_widget = video_widget
        self.status_callback = status_callback
        
        # Video state
        self.cap = None
        self.video_path = None
        self.video_loaded = False
        self.is_playing = False
        self.is_paused = False
        self.is_stopped = True
        
        # Playback properties
        self.fps = 0
        self.total_frames = 0
        self.duration = 0
        self.current_frame = 0
        self.playback_speed = 1.0
        self.volume = 50
        
        # Threading
        self.play_thread = None
        self.should_continue = False
        
        # Callbacks
        self.on_frame_update = None
        self.on_time_update = None
        
    def load_video(self, file_path):
        """Load a video file"""
        if self.is_playing:
            self.stop()
            
        self.cap = cv2.VideoCapture(file_path)
        
        if not self.cap.isOpened():
            self.update_status("Error: Could not open video file")
            return False
            
        self.video_path = file_path
        self.video_loaded = True
        self.is_stopped = True
        
        # Get video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = get_video_duration(self.cap)  # Using imported function
        
        # Display first frame
        ret, frame = self.cap.read()
        if ret:
            self.video_widget.update_frame(frame)
            self.current_frame = 0
            
        self.update_status(f"Loaded: {file_path.split('/')[-1]}")
        self.update_time_display()
        
        # Reset to beginning
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        return True
        
    def play(self):
        """Start video playback"""
        if not self.video_loaded:
            self.update_status("No video loaded")
            return
            
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.update_status("Resumed")
            return
            
        if self.is_stopped:
            self.is_stopped = False
            self.is_playing = True
            self.is_paused = False
            
            # Reset to beginning if at end
            if self.current_frame >= self.total_frames - 1:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.current_frame = 0
                
            self.should_continue = True
            self.play_thread = threading.Thread(target=self._play_loop)
            self.play_thread.daemon = True
            self.play_thread.start()
            
            self.update_status("Playing")
            
    def _play_loop(self):
        """Main playback loop running in separate thread"""
        frame_delay = 1.0 / self.fps if self.fps > 0 else 1/30
        
        while self.should_continue and not self.is_paused:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                
                if ret:
                    self.video_widget.update_frame(frame)
                    self.current_frame += 1
                    
                    # Update time display
                    current_time = self.current_frame / self.fps if self.fps > 0 else 0
                    self.update_time_display(current_time)
                    
                    # Call frame update callback
                    if self.on_frame_update:
                        self.on_frame_update(current_time / self.duration if self.duration > 0 else 0)
                    
                    # Wait for next frame (adjust for speed)
                    time.sleep(frame_delay / self.playback_speed)
                else:
                    # End of video
                    self.stop()
                    break
            else:
                break
                
    def pause(self):
        """Pause video playback"""
        if self.is_playing:
            self.is_paused = True
            self.is_playing = False
            self.update_status("Paused")
            
    def stop(self):
        """Stop video playback"""
        self.should_continue = False
        self.is_playing = False
        self.is_paused = False
        self.is_stopped = True
        
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.current_frame = 0
            
            # Show first frame
            ret, frame = self.cap.read()
            if ret:
                self.video_widget.update_frame(frame)
                
        self.update_status("Stopped")
        self.update_time_display()
        
    def seek(self, position):
        """Seek to position (0-1)"""
        if not self.video_loaded:
            return
            
        target_frame = int(position * self.total_frames)
        if target_frame >= self.total_frames:
            target_frame = self.total_frames - 1
            
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        self.current_frame = target_frame
        
        # Update display
        ret, frame = self.cap.read()
        if ret:
            self.video_widget.update_frame(frame)
            self.current_frame += 1
            
        # Update time
        current_time = self.current_frame / self.fps if self.fps > 0 else 0
        self.update_time_display(current_time)
        
    def set_volume(self, volume):
        """Set volume level (0-100)"""
        self.volume = volume
        # Note: This is a placeholder - actual volume control depends on implementation
        
    def set_speed(self, speed):
        """Set playback speed"""
        self.playback_speed = max(0.1, min(2.0, speed))
        
    def update_status(self, message):
        """Update status"""
        if self.status_callback:
            self.status_callback(message)
            
    def update_time_display(self, current_time=None):
        """Update time display"""
        if self.on_time_update:
            if current_time is None:
                current_time = 0
            total_time = self.duration
            self.on_time_update(current_time, total_time)
            
    def cleanup(self):
        """Clean up resources"""
        self.should_continue = False
        if self.cap:
            self.cap.release()
        if self.play_thread and self.play_thread.is_alive():
            self.play_thread.join(timeout=1)
            
    def get_video_info(self):
        """Get video information"""
        if not self.video_loaded:
            return None
            
        return {
            'path': self.video_path,
            'duration': self.duration,
            'fps': self.fps,
            'total_frames': self.total_frames,
            'current_frame': self.current_frame
        }