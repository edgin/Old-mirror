#!/usr/bin/env python3
"""
Client viewer for Old TV Mirror application.
This allows viewing the mirror stream from another laptop.
"""
import cv2
import socket
import pickle
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 client_viewer.py <server_ip_address>")
        print("Example: python3 client_viewer.py 192.168.1.100")
        return
    
    server_ip = sys.argv[1]
    port = 9999
    
    try:
        # Create socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")
        
        # Display video stream
        print("Press 'q' to quit")
        
        while True:
            # Receive frame size first (4 bytes)
            try:
                frame_size_data = client_socket.recv(4)
                if not frame_size_data:
                    break
                    
                frame_size = int.from_bytes(frame_size_data, byteorder='big')
                
                # Receive full frame data
                frame_data = b""
                while len(frame_data) < frame_size:
                    chunk = client_socket.recv(min(4096, frame_size - len(frame_data)))
                    if not chunk:
                        break
                    frame_data += chunk
                
                # Deserialize frame
                frame = pickle.loads(frame_data)
                
                # Display frame
                cv2.imshow('Old TV Mirror Remote View', frame)
                
                # Break on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            except Exception as e:
                print(f"Error receiving frame: {e}")
                break
                
    except Exception as e:
        print(f"Connection error: {e}")
        
    finally:
        try:
            client_socket.close()
            cv2.destroyAllWindows()
        except:
            pass
            
        print("Client disconnected")

if __name__ == "__main__":
    main()