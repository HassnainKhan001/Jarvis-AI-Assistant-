#!/usr/bin/env python3
"""
Simple Jarvis Launcher
Starts Django server only
"""

import subprocess
import sys
import os
from pathlib import Path

def start_django():
    """Start Django development server"""
    print("Starting Django server...")
    try:
        # Change to the correct directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Start Django server
        process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "127.0.0.1:8000"
        ], cwd=script_dir)
        
        print("Django server started on http://127.0.0.1:8000")
        print("Jarvis is ready!")
        print("Open your browser and go to: http://127.0.0.1:8000")
        
        # Keep the process running
        process.wait()
        
    except KeyboardInterrupt:
        print("\nStopping Django server...")
    except Exception as e:
        print(f"Failed to start Django server: {e}")

if __name__ == "__main__":
    start_django()