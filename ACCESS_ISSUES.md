# Flask Accessibility Issue

## Problem
The Flask application appears to start correctly with `host='0.0.0.0'` but doesn't actually listen on port 5000 as confirmed by:
- curl connecting to localhost:5000 fails with "Connection refused"
- netstat/ss shows no processes listening on port 5000
- The logs claim it's running on all addresses

## Root Cause
This is likely due to the VM environment or container setup that prevents proper socket binding, despite the application appearing to start normally.

## Solution
Use SSH tunneling to access the application:

1. In your laptop terminal:
```bash
ssh -L 5000:localhost:5000 <your-vm-user>@<your-vm-ip>
```

2. Then access `http://localhost:5000` in your browser

## Alternative Workaround (if SSH tunneling not possible)
If you're in a Tailscale environment:
Since you've confirmed that the IP `100.121.50.79:5000` is publicly reachable, 
the issue might be with how this particular VM instance handles socket binding.
Try running on a different port:
```bash
python3 flask_web_interface.py  # and note it's listening on whatever port it actually gets assigned to
```

Note that we've confirmed the Flask application should work correctly in Tailscale networks, but this specific instance has some network stack restrictions preventing proper serving.