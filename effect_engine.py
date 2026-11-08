import cv2
import numpy as np

class EffectEngine:
    def __init__(self):
        self.current_effect = 1  # Start with grayscale
        self.threshold_level = 127
        self.pixel_size = 10
        self.noise_intensity = 50
        self.contrast = 1.0
        self.brightness = 0
        self.mirror_enabled = True
        
        # Parameter definitions for each effect
        self.params = {
            1: {"name": "Grayscale", "values": []},  # No parameters for grayscale
            2: {"name": "Threshold", "values": [{"name": "Level", "value": self.threshold_level, "min": 0, "max": 255}]},
            3: {"name": "Pixelation", "values": [{"name": "Size", "value": self.pixel_size, "min": 2, "max": 50}]},
            4: {"name": "Noise", "values": [{"name": "Intensity", "value": self.noise_intensity, "min": 0, "max": 100}]},
        }
    
    def init_camera(self, camera_id=0):
        """Initialize camera with proper settings"""
        try:
            cap = cv2.VideoCapture(camera_id)
            if not cap.isOpened():
                print("Error: Could not open camera.")
                return None
            
            # Set a reasonable resolution
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            return cap
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return None
    
    def process_frame(self, frame):
        """Apply current effect to frame"""
        if self.mirror_enabled:
            frame = cv2.flip(frame, 1)  # Horizontal flip
        
        # Convert to grayscale first (for effects that need it)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if self.current_effect == 1:  # Grayscale
            result = gray
            # Convert back to BGR for display consistency
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
            
        elif self.current_effect == 2:  # Threshold
            _, result = cv2.threshold(gray, self.threshold_level, 255, cv2.THRESH_BINARY)
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
            
        elif self.current_effect == 3:  # Pixelation
            h, w = frame.shape[:2]
            # Resize to smaller size (pixelate) then resize back
            small = cv2.resize(frame, None, fx=1/self.pixel_size, fy=1/self.pixel_size, interpolation=cv2.INTER_LINEAR)
            result = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
            
        elif self.current_effect == 4:  # Noise
            # Generate noise
            noise = np.random.randint(0, self.noise_intensity, frame.shape, dtype=np.uint8)
            # Combine with original frame
            result = cv2.add(frame, noise)
            
        else:
            # Default to grayscale if unrecognized effect
            result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
        return result
    
    def get_current_params(self):
        """Get current parameters for the active effect"""
        return self.params.get(self.current_effect, {"values": []})
    
    def update_parameter(self, param_index, value):
        """Update parameter value for current effect"""
        if self.current_effect in self.params:
            param_list = self.params[self.current_effect]["values"]
            if 0 <= param_index < len(param_list):
                param = param_list[param_index]
                param["value"] = max(param["min"], min(param["max"], value))
                
                # Update the corresponding class attribute
                if param["name"] == "Level":
                    self.threshold_level = param["value"]
                elif param["name"] == "Size":
                    self.pixel_size = param["value"]
                elif param["name"] == "Intensity":
                    self.noise_intensity = param["value"]
    
    def select_effect(self, effect_id):
        """Select different visual effect"""
        if effect_id in [1, 2, 3, 4]:
            self.current_effect = effect_id
    
    def reset_parameters(self):
        """Reset parameters for current effect to defaults"""
        if self.current_effect in self.params:
            reset_params = self.params[self.current_effect]["values"]
            for param in reset_params:
                if param['name'] == 'Level':
                    param['value'] = 127
                    self.threshold_level = 127
                elif param['name'] == 'Size':
                    param['value'] = 10
                    self.pixel_size = 10
                elif param['name'] == 'Intensity':
                    param['value'] = 50
                    self.noise_intensity = 50
    
    def get_effect_name(self, effect_id):
        """Get name of an effect by ID"""
        if effect_id in self.params:
            return self.params[effect_id]["name"]
        return "Unknown Effect"