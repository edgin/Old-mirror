# Old TV Mirror Application Architecture Plan

## Overview
This document outlines a plan to separate the current monolithic application into distinct layers for better maintainability and scalability. The application will be divided into three main components:

1. **Effect Logic Layer** (OpenCV-based)
2. **Control Layer** (Input handling)
3. **Presentation Layer** (Browser interface)

## Current Architecture
The existing implementation is a single-file Python application that combines:
- Video capture and processing using OpenCV
- Keyboard input handling 
- On-screen display (OSD) panel rendering
- All functionality in one script

## Proposed Separated Architecture

### 1. Effect Logic Layer (effect_engine.py)
**Responsibilities:**
- Webcam video capture
- Visual effect processing (grayscale, threshold, pixelation, noise)
- Frame processing and transformation
- Parameter management for effects

**Key Functions:**
```python
def process_frame(frame, effect_type, parameters):
    """Process a video frame with specified effect and parameters"""
    pass

def apply_grayscale(frame):
    """Apply grayscale effect"""
    pass

def apply_threshold(frame, threshold_value):
    """Apply threshold effect"""
    pass

def apply_pixelation(frame, pixel_size):
    """Apply pixelation effect"""
    pass

def apply_noise(frame, noise_intensity):
    """Apply noise effect"""
    pass
```

**Dependencies:** OpenCV, NumPy

### 2. Control Layer (controller.py)
**Responsibilities:**
- Handle keyboard and mouse input events
- Process effect selection and parameter adjustments
- Manage application state (current effect, parameters, show_panel flag)
- Communicate with effect layer and presentation layer

**Key Functions:**
```python
def handle_key_input(key):
    """Process keyboard input events"""
    pass

def update_parameter(effect_id, param_index, value):
    """Update parameter values"""
    pass

def select_effect(effect_id):
    """Select different visual effect"""
    pass
```

### 3. Presentation Layer (web_interface.py / web_server.py)
**Responsibilities:**
- Serve the web interface via HTTP server
- Handle WebSocket connections for real-time video streaming
- Display user controls in browser
- Send control commands from browser to controller

**Key Features:**
- HTTP server with Flask/Django
- WebSockets for video transmission
- Browser-based UI components
- Responsive design for different screen sizes

## Communication Flow
```
[Browser Interface] <---> [Web Server] <---> [Controller] <---> [Effect Engine]
                              ^                            ^
                              |                            |
                    [User Interaction]    [Keyboard/Mouse Input]
```

## Implementation Benefits
1. **Modularity**: Each component can be developed, tested, and maintained independently
2. **Scalability**: Easy to add new effects or control methods
3. **Testability**: Individual components can be unit tested
4. **Flexibility**: Can deploy different presentation layers (web, mobile, desktop)
5. **Maintainability**: Changes to one component don't affect others

## Next Steps
1. Create separate Python modules for each layer
2. Implement communication between layers using message passing or shared state
3. Set up web server for browser access
4. Develop WebSocket connections for video streaming
5. Create HTML/CSS/JavaScript frontend
6. Test complete separated architecture

## Timeline Estimate
- Effect Logic Layer: 1 day
- Control Layer: 1 day  
- Presentation Layer: 2 days
- Integration and Testing: 1 day
- Total: ~5 days

## Technical Considerations
- Maintain backward compatibility with existing keyboard controls
- Ensure real-time performance for video streaming
- Handle webcam access permissions in different environments
- Implement proper error handling for all components
- Design for easy deployment (Docker container support)