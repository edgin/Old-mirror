import cv2
import numpy as np
import socket
import pickle
import threading
from controller import Controller

class WebInterface:
    def __init__(self):
        self.controller = Controller()
        self.cap = None
        self.stream_socket = None
        self.stream_thread = None
        self.streaming = False
        self.camera_available = True
        
    def initialize_camera(self):
        """Initialize camera connection"""
        self.cap = self.controller.get_effect_engine().init_camera()
        if not self.cap:
            print("Warning: Could not open camera.")
            self.camera_available = False
            return False
        self.camera_available = True
        return True
    
    def start_streaming(self, host='0.0.0.0', port=9999):
        """Start video streaming server"""
        try:
            self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.stream_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.stream_socket.bind((host, port))
            self.stream_socket.listen(5)
            self.streaming = True
            self.stream_thread = threading.Thread(target=self._stream_frames)
            self.stream_thread.daemon = True
            self.stream_thread.start()
            print(f"Streaming started on {host}:{port}")
        except Exception as e:
            print(f"Failed to start streaming: {e}")
    
    def stop_streaming(self):
        """Stop video streaming"""
        self.streaming = False
        if self.stream_socket:
            self.stream_socket.close()
        if self.stream_thread:
            self.stream_thread.join()
    
    def _stream_frames(self):
        """Internal method to stream frames"""
        while self.streaming:
            try:
                # Accept client connection
                client_socket, address = self.stream_socket.accept()
                print(f"Client connected from {address}")
                
                while self.streaming:
                    # Process frame 
                    result = self.process_frame()
                    if result is None:
                        break
                        
                    # Draw OSD panel (if enabled)
                    result = self.draw_panel(result)
                    
                    # Serialize frame
                    frame_data = pickle.dumps(result)
                    frame_size = len(frame_data)
                    
                    # Send frame size first
                    client_socket.send(frame_size.to_bytes(4, byteorder='big'))
                    
                    # Send frame data
                    client_socket.sendall(frame_data)
                    
                    # Small delay to control frame rate
                    cv2.waitKey(1)
                    
                client_socket.close()
                
            except Exception as e:
                print(f"Streaming error: {e}")
                if self.streaming:
                    continue
                break
    
    def process_frame(self):
        """Capture and process a single frame"""
        if not self.cap:
            # Create a dummy frame when no camera is available
            if not self.camera_available:
                dummy_frame = np.ones((480, 640, 3), dtype=np.uint8) * 127  # Gray frame
                return self.controller.get_effect_engine().process_frame(dummy_frame)
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return None
            
        # Apply effect to current frame
        result = self.controller.get_effect_engine().process_frame(frame)
        return result
    
    def draw_panel(self, frame):
        """Draw OSD panel on frame"""
        height, width = frame.shape[:2]
        
        # Only draw panel if enabled and camera is available
        if not self.controller.show_panel or not self.camera_available:
            return frame
            
        # Panel dimensions
        panel_width = int(width * 0.4)
        panel_height = int(height * 0.3)
        panel_x = int((width - panel_width) / 2)
        panel_y = int((height - panel_height) / 10)
        
        # Draw white rectangle as panel background
        cv2.rectangle(frame, (panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height), (255, 255, 255), -1)
        
        # Get parameters for current effect
        effect_params = self.controller.get_effect_engine().get_current_params()
        param_list = effect_params["values"]
        
        # Draw effect name at top
        cv2.putText(frame, f"Effect: {effect_params['name']}", 
                    (panel_x + 10, panel_y + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        
        # Draw parameters
        param_y_offset = 50
        for i, param in enumerate(param_list):
            text = f"{param['name']}: {param['value']}"
            color = (255, 0, 0) if i == self.controller.selected_param else (0, 0, 0)
            cv2.putText(frame, text, (panel_x + 10, panel_y + param_y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Draw slider
            slider_width = panel_width - 100
            slider_x_start = panel_x + 100
            cv2.rectangle(frame, (slider_x_start, panel_y + param_y_offset - 10), 
                          (slider_x_start + slider_width, panel_y + param_y_offset - 5), 
                          (180, 180, 180), -1)
            
            # Draw current value position
            slider_position = int((param['value'] - param['min']) / (param['max'] - param['min']) * slider_width)
            cv2.rectangle(frame, (slider_x_start + slider_position - 2, panel_y + param_y_offset - 15),
                          (slider_x_start + slider_position + 2, panel_y + param_y_offset - 3), color, -1)
            
            param_y_offset += 30
        
        return frame
    
    def handle_key_input(self, key):
        """Handle keyboard input through controller"""
        return self.controller.handle_key_input(key)
    
    def get_current_state(self):
        """Get current application state for display"""
        return self.controller.get_current_state()
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_streaming()
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def is_camera_available(self):
        """Check if camera is available"""
        return self.camera_available