# Remote Access Instructions

## Accessing the Application Remotely

Once the application is running, you can access it from other devices on the same network using these methods:

### Method 1: Direct Streaming
The streaming server will be available at:
```
http://[YOUR_SERVER_IP]:9999
```

### Method 2: Client Viewer Application
You can use the client viewer to connect:
```bash
python client_viewer.py [YOUR_SERVER_IP]
```

## Available IP Addresses on This System

Your system has the following IP addresses available:
- 192.168.0.34 (local network)
- 172.20.0.1 
- 172.18.0.1
- 172.17.0.1
- 172.19.0.1
- 172.21.0.1
- 100.121.50.79 (public network)

## Usage Example

To connect from another device:
1. Start the application on this machine
2. Use any device on the same network
3. Enter `http://192.168.0.34:9999` in your browser or client viewer
4. You should see the live stream with effects applied

## Controls Available

While running:
- 1, 2, 3, 4: Select effect  
- F: Show/hide panel
- Tab: Cycle through parameters
- Arrow keys: Adjust parameters
- R: Reset parameters
- Q: Quit

Note: The streaming will work even if no camera is physically connected.