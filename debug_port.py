import socket
import sys

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open on {host}")
            return True
        else:
            print(f"Port {port} is closed on {host}")
            return False
    except Exception as e:
        print(f"Error checking port {port}: {e}")
        return False
    finally:
        sock.close()

# Check if localhost port 5000 is accessible
check_port('127.0.0.1', 5000)

# Check VM network interface 
check_port('192.168.0.34', 5000)
