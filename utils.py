import os
import time
from pathlib import Path
import cv2  # Add this import

def get_file_size(file_path):
    """Get file size in human readable format"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def get_video_duration(cap):
    """Get video duration in seconds from VideoCapture object"""
    if cap:
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if fps > 0:
            return frame_count / fps
    return 0

def get_video_duration_from_path(file_path):
    """Get video duration in seconds from file path"""
    cap = cv2.VideoCapture(file_path)
    if cap.isOpened():
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        if fps > 0:
            return frame_count / fps
    return 0

def format_time(seconds):
    """Format seconds to HH:MM:SS"""
    if seconds < 0:
        seconds = 0
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"

def get_supported_formats():
    """Get list of supported video formats"""
    return ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v', '.3gp']

def is_video_file(file_path):
    """Check if file is a supported video format"""
    ext = os.path.splitext(file_path)[1].lower()
    return ext in get_supported_formats()

def get_video_info(file_path):
    """Get comprehensive video information"""
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        return None
    
    info = {
        'path': file_path,
        'filename': os.path.basename(file_path),
        'file_size': get_file_size(file_path),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'codec': int(cap.get(cv2.CAP_PROP_FOURCC)),
    }
    
    # Calculate duration
    if info['fps'] > 0:
        info['duration'] = info['frame_count'] / info['fps']
        info['duration_formatted'] = format_time(info['duration'])
    else:
        info['duration'] = 0
        info['duration_formatted'] = "00:00"
    
    cap.release()
    return info

def get_frame_at_time(cap, time_seconds):
    """Get frame at specific time in seconds"""
    if not cap or not cap.isOpened():
        return None
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        return None
    
    frame_number = int(time_seconds * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    return frame if ret else None