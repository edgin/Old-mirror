#!/usr/bin/env python3

"""
Simple demonstration of the web interface functionality
without requiring full camera access.
"""

from controller import Controller

def demo_web_interface():
    """Demonstrate how web interface works without video feed"""
    
    # Create a controller instance
    controller = Controller()
    
    print("Old TV Mirror - Web Interface Demo")
    print("==================================")
    print(f"Current effect: {controller.get_effect_engine().params[controller.get_effect_engine().current_effect]['name']}")
    print(f"Parameters: {controller.get_effect_engine().get_current_params()['values']}")
    
    # Test parameter modification
    if controller.get_effect_engine().current_effect == 2:  # Threshold effect
        print("Modifying parameters...")
        controller.get_effect_engine().update_parameter(0, 100)  # Set threshold to 100
        param = controller.get_effect_engine().get_current_params()['values'][0]
        print(f"Updated parameter value: {param['value']}")

if __name__ == "__main__":
    demo_web_interface()