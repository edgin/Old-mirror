#!/usr/bin/env python3
"""
Test script for Flask web interface.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flask_web_interface import app
    print("✓ Flask app imported successfully")
    
    # Test that we can create an app instance
    with app.app_context():
        print("✓ Flask app context created successfully")
        
    print("✓ Flask web interface test passed!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print("Flask web interface is properly set up and ready to run.")