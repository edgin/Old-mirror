import cv2
import numpy as np
from web_interface import WebInterface

def main():
    # Create web interface instance
    web_interface = WebInterface()
    
    # Initialize camera
    if not web_interface.initialize_camera():
        print("Warning: No camera available. Running in simulation mode.")
        # Continue with limited functionality
    else:
        print("Camera initialized successfully!")
    
    # Start streaming server (will be accessible from other laptops)
    web_interface.start_streaming()
    
    print("Old TV Mirror started!")
    print("Controls:")
    print("- 1, 2, 3, 4: Select effect")
    print("- F: Show/hide panel")
    print("- Tab: Cycle through parameters")
    print("- Arrow keys: Adjust parameters")
    print("- R: Reset parameters")
    print("- Q: Quit")
    
    try:
        while True:
            # Process frame
            result = web_interface.process_frame()
            if result is None and not web_interface.is_camera_available():
                # If no camera available, simulate a gray frame (should be handled in process_frame now)
                # But we can still show something for testing
                pass  # The processing should handle this through process_frame() method
                
            if result is None:
                break
                
            # Draw OSD panel (if enabled)
            result = web_interface.draw_panel(result)
                
            # Show the result
            cv2.imshow('Old TV Mirror', result)

            key = cv2.waitKey(1) & 0xFF

            # Handle key input through controller
            action = web_interface.handle_key_input(key)
            if action == 'quit':
                break
                
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        # Cleanup resources
        web_interface.cleanup()

if __name__ == "__main__":
    main()