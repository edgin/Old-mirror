# Old TV Mirror — Startup Instructions

This guide explains how to start Old TV Mirror after shutting it down.

## Services

| Service | Machine | Port |
|---|---|---:|
| USB camera server | Windows laptop | 8765 |
| Flask backend | Ubuntu VM (`zigmund`) | 5000 |
| React frontend (Vite) | Ubuntu VM (`zigmund`) | 3000 |

The FaceCam 1000X is connected to Windows. Its video is streamed to Ubuntu over Tailscale.

## 1. Start the Windows camera server

1. Make sure Tailscale is connected on the Windows laptop.
2. Open **Windows PowerShell**.
3. Go to the folder containing `camera_server.py`. If you saved it in your Windows user folder:

   ```powershell
   cd $HOME
   ```

4. Start the camera server:

   ```powershell
   py camera_server.py
   ```

Leave this PowerShell window open. You should see that the camera opened successfully and that the server is running at `http://100.69.74.51:8765`.

Check the server at <http://100.69.74.51:8765/health>. It should report `"status":"ok"`.

## 2. Start the Flask backend on Ubuntu

Open **Windows Terminal** and connect to the Ubuntu VM:

```bash
ssh lule@100.121.50.79
```

Then run:

```bash
cd ~/projects/old_mirror
source venv/bin/activate
python flask_web_interface.py
```

Keep this terminal open.

To check Flask, open a second SSH terminal and run:

```bash
curl -s http://localhost:5000/health
```

The response should report `"camera_connected":true` and `"status":"ok"`.

## 3. Start the React frontend on Ubuntu

Open a **second Windows Terminal** window and connect to Ubuntu:

```bash
ssh lule@100.121.50.79
```

Then run:

```bash
cd ~/projects/old_mirror/react-frontend
npm run dev -- --host 0.0.0.0
```

Keep this terminal open. Wait for Vite to report that it is ready and show the network address:

```text
http://100.121.50.79:3000/
```

## 4. Open the application

On the Windows laptop, open your browser at:

<http://100.121.50.79:3000/>

If the page is already open, refresh it with **Ctrl + F5**.

## Startup checklist

- [ ] Tailscale is connected on Windows and Ubuntu.
- [ ] Windows camera server is running on port `8765`.
- [ ] Ubuntu Flask backend is running on port `5000`.
- [ ] Ubuntu Vite frontend is running on port `3000`.
- [ ] Browser is open at `http://100.121.50.79:3000/`.

## Shut down

Stop each process in its own terminal by pressing **Ctrl + C**:

1. Windows PowerShell running `camera_server.py`
2. Ubuntu terminal running Flask
3. Ubuntu terminal running Vite

## Troubleshooting

### Camera is unavailable

- Confirm the USB camera is connected to Windows.
- Confirm the camera server is running and its `/health` endpoint reports `ok`.
- If Flask was started before the camera server, restart Flask after the camera server is up.

### Frontend does not load

- Confirm Vite is still running and reports the network address above.
- Confirm Tailscale is connected on both machines.
- Refresh the browser with **Ctrl + F5**.

A Vite warning about `configLoader: 'native'` is not necessarily a failure. If Vite reports that it is ready, continue.

## Useful addresses

| Purpose | Address |
|---|---|
| Windows camera health | <http://100.69.74.51:8765/health> |
| Windows camera stream | <http://100.69.74.51:8765/video_feed> |
| Ubuntu Flask health | <http://100.121.50.79:5000/health> |
| Old TV Mirror frontend | <http://100.121.50.79:3000/> |
