#!/usr/bin/env python3
"""
Flask web interface for Old TV Mirror application.
This enables remote viewing and control of the application from another laptop via browser.
"""

import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify, request
from threading import Thread, Lock
import base64
import time
from controller import Controller
from effect_engine import EffectEngine

app = Flask(__name__)

# Global variables for video streaming and application state
controller = None
cap = None
current_frame = None
frame_lock = Lock()
is_streaming = False
stream_thread = None
camera_available = False
camera_access_allowed = True  # Flag to indicate if camera access is allowed
camera_list = []  # List of available cameras

def detect_cameras():
    """Detect available cameras in the system"""
    global camera_list
    
    camera_list = []
    max_test = 10  # Test first 10 indices
    
    print('Detecting cameras...')
    
    for i in range(max_test):
        try:
            cap_test = cv2.VideoCapture(i)
            if cap_test.isOpened():
                print(f'Camera detected at index {i}')
                camera_list.append(i)
                cap_test.release()
            else:
                print(f'No camera at index {i}')
        except Exception as e:
            print(f'Error accessing camera at index {i}: {e}')
    
    if camera_list:
        print(f'Found cameras: {camera_list}')
    else:
        print('No cameras detected')
        
    return camera_list


REMOTE_CAMERA_URL = "http://100.69.74.51:8765/video_feed"


def initialize_camera():
    """Initialize connection to the remote Windows USB camera."""
    global cap, controller, camera_available

    controller = Controller()

    try:
        print(f"Connecting to remote camera: {REMOTE_CAMERA_URL}")

        cap = controller.get_effect_engine().init_camera(
            REMOTE_CAMERA_URL
        )

        if cap is None or not cap.isOpened():
            print("Error: Could not connect to remote camera.")
            camera_available = False
            return False

        camera_available = True

        print("Remote camera successfully initialized!")
        return True

    except Exception as e:
        print(f"Error initializing remote camera: {e}")
        camera_available = False
        return False




def stream_video():
    """Background thread for video streaming"""
    global current_frame, frame_lock, is_streaming, camera_available
    
    while is_streaming:
        if camera_available and cap and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Apply effect to current frame
                result = controller.get_effect_engine().process_frame(frame)
                
                with frame_lock:
                    current_frame = result.copy()
        else:
            # Even without camera, we should still allow the interface to work
            time.sleep(0.03)  # ~30 FPS

def generate_frames():
    """Generate video frames for streaming"""
    global current_frame, frame_lock
    
    while True:
        with frame_lock:
            if current_frame is not None:
                # Convert frame to JPEG
                ret, buffer = cv2.imencode('.jpg', current_frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            else:
                # Send a black frame if no data
                black_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                ret, buffer = cv2.imencode('.jpg', black_frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming endpoint"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control/<action>')
def control(action):
    """Handle remote control commands"""
    global controller
    
    try:
        if not controller:
            return jsonify({"error": "Controller not initialized"}), 400
            
        if action == 'next_effect':
            # Simulate pressing keys
            controller.handle_key_input(ord('2'))  # Next effect (this will be adjusted accordingly)
        elif action == 'prev_effect':
            # Simulate pressing keys
            controller.handle_key_input(ord('1'))  # Previous effect
        elif action == 'toggle_panel':
            controller.handle_key_input(ord('f'))
        elif action == 'reset':
            controller.handle_key_input(ord('r'))
            
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/control/keyboard', methods=['POST'])
def control_keyboard():
    """Handle keyboard control commands via POST"""
    global controller
    
    try:
        if not controller:
            return jsonify({"error": "Controller not initialized"}), 400
            
        data = request.get_json()
        key = data.get('key')
        
        if key:
            # Convert key to ord value or handle special keys
            if isinstance(key, str) and len(key) == 1:
                controller.handle_key_input(ord(key))
            elif key.lower() == 'f':
                controller.handle_key_input(ord('f'))
            elif key.lower() == 'r':
                controller.handle_key_input(ord('r'))
            elif key == 'prev':
                controller.handle_key_input(ord('1'))
            elif key == 'next':
                controller.handle_key_input(ord('2'))
            
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/control/update_param', methods=['POST'])
def update_param():
    """Update an effect parameter from the React frontend."""
    global controller

    if controller is None:
        return jsonify({"error": "Controller not initialized"}), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    if 'param_name' not in data or 'value' not in data:
        return jsonify({"error": "Missing parameter data"}), 400

    param_name = data['param_name']
    value = data['value']

    if not isinstance(param_name, str):
        return jsonify({"error": "Parameter name must be a string"}), 400

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return jsonify({"error": "Value must be numeric"}), 400

    try:
        effect_engine = controller.get_effect_engine()
        params = effect_engine.get_current_params().get("values", [])

        # Find the numeric index expected by EffectEngine
        param_index = next(
            (
                i for i, param in enumerate(params)
                if param["name"] == param_name
            ),
            None
        )

        if param_index is None:
            return jsonify({"error": "Unknown parameter"}), 400

        effect_engine.update_parameter(param_index, value)

        # Return the actual value after min/max clamping
        updated_value = params[param_index]["value"]

        return jsonify({
            "status": "success",
            "param_name": param_name,
            "value": updated_value
        })

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        app.logger.exception("Failed to update effect parameter")
        return jsonify({"error": "Parameter update failed"}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "camera_connected": camera_available,
        "cameras_found": camera_list
    })

@app.route('/current_effect')
def current_effect():
    """Get current effect information"""
    global controller
    
    try:
        if not controller:
            return jsonify({"error": "Controller not initialized"}), 400
            
        effect_params = controller.get_effect_engine().get_current_params()
        return jsonify({
            "current_effect": effect_params["name"],
            "effect_parameters": effect_params["values"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cameras')
def get_cameras():
    """Get list of available cameras"""
    detect_cameras()
    return jsonify({
        "available_cameras": camera_list,
        "camera_count": len(camera_list)
    })

@app.route('/')
def index():
    """Main web page"""
    return render_template('index.html', 
                          camera_available=camera_available,
                          host=request.host.split(':')[0] if ':' in request.host else request.host,
                          port=request.host.split(':')[1] if ':' in request.host else 5000)

if __name__ == '__main__':
    # Initialize the app
    if not initialize_camera():
        print("Warning: Camera initialization failed, but application will continue to run.")
    
    # Start video streaming thread
    is_streaming = True
    stream_thread = Thread(target=stream_video)
    stream_thread.daemon = True
    stream_thread.start()
    
    print("Flask web interface started. Visit http://localhost:5000 to view the application.")
    print("For secure access, use Tailscale Serve with:")
    print("  tailscale serve https+insecure://localhost:5000")
    print("")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
