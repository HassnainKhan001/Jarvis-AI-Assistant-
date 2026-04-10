#!/usr/bin/env python3
"""
Jarvis AI Assistant - Ultimate Launcher
Starts all Jarvis components with enhanced features
"""

import subprocess
import threading
import time
import sys
import os
from pathlib import Path

class JarvisLauncher:
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent
        
    def start_django_server(self):
        """Start Django development server"""
        print("🌐 Starting Django server...")
        try:
            process = subprocess.Popen(
                [sys.executable, "manage.py", "runserver"],
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(("Django Server", process))
            print("✅ Django server started on http://127.0.0.1:8000")
            return True
        except Exception as e:
            print(f"❌ Failed to start Django server: {e}")
            return False
    
    def start_face_detection_listener(self):
        """Start face detection and voice listener"""
        print("👤 Starting face detection and voice listener...")
        try:
            process = subprocess.Popen(
                [sys.executable, "simple_listener.py"],
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(("Face Detection Listener", process))
            print("✅ Face detection listener started")
            return True
        except Exception as e:
            print(f"❌ Failed to start face detection listener: {e}")
            return False
    
    def start_gui(self):
        """Start the GUI interface"""
        print("🖥️  Starting Jarvis GUI...")
        try:
            process = subprocess.Popen(
                [sys.executable, "gui/jarvis_gui.py"],
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(("GUI Interface", process))
            print("✅ GUI interface started")
            return True
        except Exception as e:
            print(f"❌ Failed to start GUI: {e}")
            return False
    
    def show_status(self):
        """Show status of all running processes"""
        print("\n📊 Jarvis System Status:")
        print("=" * 50)
        
        for name, process in self.processes:
            if process.poll() is None:
                print(f"✅ {name}: RUNNING")
            else:
                print(f"❌ {name}: STOPPED")
        
        print("=" * 50)
    
    def stop_all(self):
        """Stop all running processes"""
        print("\n🛑 Stopping all Jarvis components...")
        
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name}: Stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"🔥 {name}: Force killed")
            except Exception as e:
                print(f"❌ {name}: Error stopping - {e}")
        
        self.processes.clear()
        print("👋 All Jarvis components stopped")
    
    def run(self):
        """Main launcher function"""
        print("🚀 JARVIS AI ASSISTANT - ULTIMATE LAUNCHER")
        print("=" * 50)
        print("Starting all Jarvis components...")
        
        # Start components in order
        components = [
            ("Django Server", self.start_django_server),
            ("Face Detection", self.start_face_detection_listener),
            ("GUI Interface", self.start_gui),
        ]
        
        started = []
        for name, start_func in components:
            if start_func():
                started.append(name)
            time.sleep(2)  # Give each component time to start
        
        if started:
            print(f"\n🎉 Successfully started: {', '.join(started)}")
            print("\n📋 Available Features:")
            print("• 🤖 AI Chat Assistant")
            print("• 👤 Face Detection & Greeting")
            print("• 🔍 Smart Google Search with Auto-Click")
            print("• 📊 TradingView Integration")
            print("• ⚡ Smart Automations")
            print("• 🖥️  Beautiful GUI Interface")
            print("• 🎵 Voice Commands (coming soon)")
            print("• 🌍 Multi-language Support (coming soon)")
            
            print("\n📖 Quick Commands:")
            print("• 'search google for tradingview' - Auto-clicks to open TradingView")
            print("• 'list automations' - Shows available automations")
            print("• 'quick trading' - Starts trading routine")
            print("• 'morning routine' - Starts morning setup")
            print("• 'work mode' - Setup workspace")
            print("• 'open [app]' - Opens any application")
            
            print("\n🌐 Access Points:")
            print("• Web Interface: http://127.0.0.1:8000")
            print("• GUI Application: Separate window")
            print("• Face Detection: Always active")
            
            try:
                print("\n⌨️  Press Ctrl+C to stop all components...")
                while True:
                    time.sleep(1)
                    # Check if any process died
                    for name, process in self.processes:
                        if process.poll() is not None:
                            print(f"⚠️  {name} stopped unexpectedly")
                            
            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested...")
            finally:
                self.stop_all()
        else:
            print("❌ Failed to start any components")
            sys.exit(1)

def main():
    launcher = JarvisLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
