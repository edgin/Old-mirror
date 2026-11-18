# Old TV Mirror

A vintage-looking mirror application with visual effects that processes live camera feed in real-time and can be controlled remotely via web interface.

## Features

- Real-time camera feed processing with 4 different visual effects:
  - Fisheye distortion
  - Retro TV effect
  - Glitch effect
  - Sepia tone
- Interactive controls using keyboard
- Remote viewing from another laptop via web browser
- Streaming capabilities for remote monitoring
- Docker support for containerized deployment

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd old_mirror
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install system dependencies (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install libopencv-dev python3-opencv
```

## Quick Start

1. Run the main application:
```bash
python main.py
```
or with Flask web interface:
```bash
python flask_web_interface.py
```

2. Access the mirror from any device on the same network:
   - Direct streaming: connect to port 9999 using VLC or other TCP client
   - Web interface: open a browser and navigate to `http://[your-local-ip]:5000`

## Controls

- 1, 2, 3, 4: Select effect
- F: Show/hide panel
- Tab: Cycle through parameters
- Arrow keys: Adjust parameters
- R: Reset parameters
- Q: Quit

## Project Structure

```
old_mirror/
├── main.py                   # Main application entry point
├── web_interface.py          # Core video processing and streaming
├── flask_web_interface.py    # Web interface for remote control
├── controller.py             # Control logic and keyboard handling
├── effect_engine.py          # Visual effects processing
├── templates/                # HTML templates for web interface
├── client_viewer.py          # Client-side viewer (for testing)
├── demo_server.py            # Demo server for development
├── web_interface_demo.py     # Demo of web interface
├── test_server.py            # Test server for testing
├── start_application.sh      # Convenient startup script
├── Dockerfile               # Container definition
├── docker-compose.yml       # Multi-service container setup
└── requirements.txt         # Python dependencies
```

## How It Works

The application works with:
1. A live camera feed (using OpenCV)
2. Various visual effects applied in real-time
3. Interactive controls for tuning parameters
4. Remote streaming capabilities for viewing from another device

## Remote Access Instructions

For remote access, the application automatically discovers your local IP address and makes it available on your local network:
1. Run the main application: `python main.py` or `python flask_web_interface.py`
2. The web interface will be accessible at `http://[your-local-ip]:5000`
3. The streaming server will automatically start on port 9999
4. Connect from another laptop using any TCP client or VLC

## Docker Support

A complete Docker setup is available with docker-compose.yml:
```bash
docker-compose up --build
```

This creates a containerized version of the application with:
- Camera access via device mounting
- Web interface on port 5000
- Streaming on port 9999

## Troubleshooting

If you have camera issues, check:
1. Permissions - ensure your user has access to the camera
2. Device availability - verify `/dev/video0` or similar exists
3. System dependencies - make sure OpenCV is properly installed

See `camera_troubleshooting_guide.md` for detailed troubleshooting steps.

## Development

The project uses a modular design with separate modules for:
- Controller logic
- Effect processing  
- Web interface
- Streaming capabilities

Contributions are welcome! Please feel free to improve the documentation, add new effects, or enhance the user interface.