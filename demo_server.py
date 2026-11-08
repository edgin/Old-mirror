#!/usr/bin/env python3
"""
Demo server to show how the streaming would work without actual camera
"""
import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
from threading import Thread, Lock
import base64
import time
import random

app = Flask(__name__)

# Simulate frame data for demo purposes
current_frame = None
frame_lock = Lock()
is_streaming = False

def generate_demo_frames():
    """Generate demo video frames"""
    global current_frame, frame_lock, is_streaming
    
    while is_streaming:
        # Create a demo frame with some animation
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Draw animated pattern
        time_val = int(time.time() * 10) % 100
        cv2.circle(frame, (320 + int(100 * np.sin(time_val/10)), 240 + int(100 * np.cos(time_val/10))), 
                   50, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), -1)
        
        # Add some text
        cv2.putText(frame, "Old TV Mirror Demo", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Streaming Ready", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        with frame_lock:
            current_frame = frame.copy()
            
        # Encode frame as JPEG
        success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if success:
            # Convert to base64 for web streaming
            jpg_as_text = base64.b64encode(buffer).decode()
            yield (f"--frame\r\n"
                   f"Content-Type: image/jpeg\r\n\r\n" + jpg_as_text + "\r\n")
            
        time.sleep(0.1)  # ~10 FPS

def start_demo_stream():
    """Start demo streaming"""
    global is_streaming
    is_streaming = True
    
    # Start streaming in background thread
    stream_thread = Thread(target=generate_demo_frames)
    stream_thread.daemon = True
    stream_thread.start()
    
    print("Demo streaming started!")
    print("Access the demo at http://localhost:5000")
    return stream_thread

@app.route('/')
def index():
    """Main web page"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming endpoint"""
    # For demo, we'll use the demo streaming function
    def generate():
        while True:
            with frame_lock:
                if current_frame is not None:
                    # Encode frame as JPEG
                    success, buffer = cv2.imencode('.jpg', current_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    if success:
                        jpg_as_text = base64.b64encode(buffer).decode()
                        yield (f"--frame\r\n"
                               f"Content-Type: image/jpeg\r\n\r\n" + jpg_as_text + "\r\n")
            time.sleep(0.1)
            
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the demo
    start_demo_stream()
    
    print("Starting Flask server for demo...")
    print("Access the demo at http://localhost:5000")
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("Demo stopped")