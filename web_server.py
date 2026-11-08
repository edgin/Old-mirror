"""
Network streaming server for Old TV Mirror application.
This enables remote viewing of the application from another laptop.
"""
import cv2
from controller import Controller
import threading
import socket
import pickle
import sys
import time

class NetworkServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.controller = Controller()
        self.cap = None
        self.is_running = False
        self.clients = []
        self.frame_lock = threading.Lock()
        
    def initialize_camera(self):
        """Initialize camera connection"""
        self.cap = self.controller.get_effect_engine().init_camera()
        if not self.cap:
            print("Error: Could not open camera.")
            return False
        return True
    
    def start_server(self):
        """Start the network server for video streaming"""
        print(f"Network server starting on {self.host}:{self.port}...")
        
        # Start camera initialization
        if not self.initialize_camera():
            return
            
        # Create socket server thread
        server_thread = threading.Thread(target=self._run_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Start video streaming thread
        stream_thread = threading.Thread(target=self._stream_video)
        stream_thread.daemon = True
        stream_thread.start()
        
        self.is_running = True
        print("Network server is running. Connect from remote laptop using: python3 client_viewer.py <IP_ADDRESS>")
        
    def _run_server(self):
        """Handle client connections"""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            print(f"Listening for connections on {self.host}:{self.port}")
            
            while self.is_running:
                try:
                    client_socket, addr = server_socket.accept()
                    print(f"Client connected from {addr}")
                    self.clients.append(client_socket)
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client, 
                        args=(client_socket,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except:
                    if self.is_running:
                        print("Error accepting connections")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server_socket.close()
            
    def _handle_client(self, client_socket):
        """Handle individual client interactions"""
        try:
            while self.is_running:
                # Send control commands
                command = client_socket.recv(1024)
                if not command:
                    break
                    
                command_str = command.decode('utf-8')
                print(f"Received command: {command_str}")
                
                # Process control commands (you can extend this logic)
                if command_str == 'quit':
                    break
                    
        except Exception as e:
            print(f"Client handling error: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            
    def _stream_video(self):
        """Stream video frames to all connected clients"""
        if not self.cap:
            return
            
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                # Process frame through effect engine
                processed_frame = self.controller.get_effect_engine().process_frame(frame)
                
                try:
                    # Send frame to all connected clients
                    with self.frame_lock:
                        frame_data = pickle.dumps(processed_frame)
                        for client in self.clients[:]:  # Copy list to avoid modification during iteration
                            try:
                                client.send(len(frame_data).to_bytes(4, byteorder='big'))
                                client.send(frame_data)
                            except:
                                # Remove stale clients
                                if client in self.clients:
                                    self.clients.remove(client)
                                    client.close()
                                
                except Exception as e:
                    print(f"Streaming error: {e}")
                    
            time.sleep(0.03)  # ~30 FPS
    
    def stop_server(self):
        """Stop the network server"""
        self.is_running = False
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        if self.cap:
            self.cap.release()
        print("Network server stopped")

# This file would typically be run as a separate process or integrated with
# Flask/Django for actual web serving functionality

# For running directly:
if __name__ == "__main__":
    server = NetworkServer()
    try:
        server.start_server()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Shutting down...")
        server.stop_server()