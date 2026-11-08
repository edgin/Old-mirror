import cv2
from effect_engine import EffectEngine

class Controller:
    def __init__(self):
        self.effect_engine = EffectEngine()
        self.show_panel = False
        self.selected_param = 0
        self.key_mapping = {
            ord('1'): 1,
            ord('2'): 2,
            ord('3'): 3,
            ord('4'): 4,
            ord('q'): ord('q'),
            ord('Q'): ord('q'),
            ord('f'): ord('f'),
            ord('F'): ord('f'),
            ord('\t'): ord('\t'),  # Tab
            27: 27,  # Escape
            83: 83,  # Right arrow
            81: 81,  # Left arrow
        }
    
    def handle_key_input(self, key):
        """Process keyboard input events"""
        # Handle global keys (non-effect-specific)
        if key == ord('q') or key == ord('Q'):
            return 'quit'
            
        elif key == ord('f') or key == ord('F'):
            self.show_panel = not self.show_panel
            self.selected_param = 0
            return 'panel_toggle'
            
        elif key == 27:  # Escape key
            self.show_panel = False
            self.selected_param = 0
            return 'panel_hide'
            
        elif key == ord('r') or key == ord('R'):
            # Reset parameters for current effect
            self.effect_engine.reset_parameters()
            return 'param_reset'
            
        else:
            # Handle effect selection
            if key in self.key_mapping and self.key_mapping[key] in [1,2,3,4]:
                self.effect_engine.select_effect(self.key_mapping[key])
                return 'effect_select'
         
        # Handle parameter adjustment with arrow keys
        if self.show_panel:  # Only process when panel is visible
            effect_params = self.effect_engine.get_current_params()
            if len(effect_params["values"]) > 0:
                param_list = effect_params["values"]
                param = param_list[self.selected_param]
                
                # Check for shift key modifier (key 16777248 is Shift in OpenCV)
                is_shift_down = False
                if key == 16777248:  # This is the shift key
                    is_shift_down = True
                    
                adjust_value = 0.1 if is_shift_down else 1
                
                if key == 83:  # Right arrow
                    new_value = min(param["max"], param["value"] + adjust_value)
                    self.effect_engine.update_parameter(self.selected_param, new_value)
                    return 'param_adjust'
                    
                elif key == 81:  # Left arrow
                    new_value = max(param["min"], param["value"] - adjust_value)
                    self.effect_engine.update_parameter(self.selected_param, new_value)
                    return 'param_adjust'
                
                elif key == 9:  # Tab key to cycle parameters
                    self.selected_param = (self.selected_param + 1) % len(param_list)
                    return 'param_cycle'
        
        return None
    
    def get_current_state(self):
        """Get current application state"""
        return {
            'current_effect': self.effect_engine.current_effect,
            'show_panel': self.show_panel,
            'selected_param': self.selected_param,
            'params': self.effect_engine.params
        }
    
    def set_show_panel(self, show):
        """Set panel visibility"""
        self.show_panel = show
    
    def get_effect_engine(self):
        """Get reference to effect engine"""
        return self.effect_engine