import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
import json
import time
import pyautogui
from PIL import Image, ImageTk
import os
import sys

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis AI Assistant - Advanced Interface")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Color scheme
        self.colors = {
            'bg': '#1a1a2e',
            'fg': '#eee',
            'accent': '#16213e',
            'button': '#0f3460',
            'button_hover': '#533483',
            'success': '#00ff00',
            'error': '#ff0000',
            'warning': '#ffa500'
        }
        
        # Initialize components
        self.setup_styles()
        self.create_widgets()
        self.setup_status_checker()
        
    def setup_styles(self):
        """Setup custom styles for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=self.colors['bg'], 
                       foreground=self.colors['fg'],
                       font=('Arial', 24, 'bold'))
        
        style.configure('Custom.TButton',
                       background=self.colors['button'],
                       foreground=self.colors['fg'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10, 'bold'))
        
        style.map('Custom.TButton',
                 background=[('active', self.colors['button_hover'])])
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title Section
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="🤖 JARVIS AI ASSISTANT", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        self.status_label = tk.Label(title_frame, text="🔴 OFFLINE", 
                                    bg=self.colors['bg'], fg=self.colors['error'],
                                    font=('Arial', 12, 'bold'))
        self.status_label.pack(side=tk.RIGHT)
        
        # Main content area
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Commands
        left_panel = tk.Frame(content_frame, bg=self.colors['accent'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_command_panel(left_panel)
        
        # Right panel - Chat and Output
        right_panel = tk.Frame(content_frame, bg=self.colors['accent'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_chat_panel(right_panel)
        
        # Bottom control panel
        self.create_control_panel(main_frame)
    
    def create_command_panel(self, parent):
        """Create the command panel with quick actions"""
        # Panel title
        cmd_title = tk.Label(parent, text="⚡ QUICK COMMANDS", 
                           bg=self.colors['accent'], fg=self.colors['fg'],
                           font=('Arial', 14, 'bold'))
        cmd_title.pack(pady=10)
        
        # Search commands
        search_frame = tk.LabelFrame(parent, text="🔍 Search & Open", 
                                    bg=self.colors['accent'], fg=self.colors['fg'],
                                    font=('Arial', 10, 'bold'))
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        commands = [
            ("🌐 Open Google", "open google"),
            ("📊 TradingView", "search google for tradingview"),
            ("🎵 YouTube", "open youtube"),
            ("💬 ChatGPT", "open chatgpt"),
            ("📧 Gmail", "open gmail")
        ]
        
        for text, command in commands:
            btn = tk.Button(search_frame, text=text, 
                          command=lambda c=command: self.execute_command(c),
                          bg=self.colors['button'], fg=self.colors['fg'],
                          font=('Arial', 9), relief=tk.FLAT, cursor='hand2')
            btn.pack(fill=tk.X, padx=5, pady=2)
        
        # System commands
        system_frame = tk.LabelFrame(parent, text="⚙️ System Control", 
                                    bg=self.colors['accent'], fg=self.colors['fg'],
                                    font=('Arial', 10, 'bold'))
        system_frame.pack(fill=tk.X, padx=10, pady=5)
        
        system_commands = [
            ("🖥️ Show Desktop", "desktop"),
            ("🔒 Lock PC", "lock"),
            ("🔊 Volume Up", "volume up"),
            ("🔉 Volume Down", "volume down"),
            ("🔇 Mute", "mute")
        ]
        
        for text, command in system_commands:
            btn = tk.Button(system_frame, text=text,
                          command=lambda c=command: self.execute_command(c),
                          bg=self.colors['button'], fg=self.colors['fg'],
                          font=('Arial', 9), relief=tk.FLAT, cursor='hand2')
            btn.pack(fill=tk.X, padx=5, pady=2)
    
    def create_chat_panel(self, parent):
        """Create the chat interface"""
        # Chat display
        chat_frame = tk.Frame(parent, bg=self.colors['accent'])
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat title
        chat_title = tk.Label(chat_frame, text="💬 JARVIS CHAT", 
                            bg=self.colors['accent'], fg=self.colors['fg'],
                            font=('Arial', 14, 'bold'))
        chat_title.pack(pady=(0, 10))
        
        # Chat history
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            bg=self.colors['bg'], 
            fg=self.colors['fg'],
            font=('Consolas', 10),
            wrap=tk.WORD,
            height=20
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Add welcome message
        self.add_chat_message("Jarvis", "Welcome! I'm Jarvis, your AI assistant. How can I help you today?", "system")
        
        # Command input
        input_frame = tk.Frame(chat_frame, bg=self.colors['accent'])
        input_frame.pack(fill=tk.X)
        
        self.command_entry = tk.Entry(input_frame, 
                                     bg=self.colors['bg'], 
                                     fg=self.colors['fg'],
                                     font=('Arial', 11),
                                     insertbackground=self.colors['fg'])
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.command_entry.bind('<Return>', lambda e: self.send_command())
        
        send_btn = tk.Button(input_frame, text="🚀 SEND",
                           command=self.send_command,
                           bg=self.colors['button'], fg=self.colors['fg'],
                           font=('Arial', 10, 'bold'), relief=tk.FLAT, cursor='hand2')
        send_btn.pack(side=tk.RIGHT)
    
    def create_control_panel(self, parent):
        """Create the bottom control panel"""
        control_frame = tk.Frame(parent, bg=self.colors['accent'])
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Voice control
        voice_btn = tk.Button(control_frame, text="🎤 Voice Control",
                            command=self.toggle_voice_control,
                            bg=self.colors['button'], fg=self.colors['fg'],
                            font=('Arial', 10, 'bold'), relief=tk.FLAT, cursor='hand2')
        voice_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Face detection
        self.face_btn = tk.Button(control_frame, text="👤 Face Detection: OFF",
                                 command=self.toggle_face_detection,
                                 bg=self.colors['button'], fg=self.colors['fg'],
                                 font=('Arial', 10, 'bold'), relief=tk.FLAT, cursor='hand2')
        self.face_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Settings
        settings_btn = tk.Button(control_frame, text="⚙️ Settings",
                               command=self.open_settings,
                               bg=self.colors['button'], fg=self.colors['fg'],
                               font=('Arial', 10, 'bold'), relief=tk.FLAT, cursor='hand2')
        settings_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Clear chat
        clear_btn = tk.Button(control_frame, text="🗑️ Clear Chat",
                            command=self.clear_chat,
                            bg=self.colors['warning'], fg=self.colors['fg'],
                            font=('Arial', 10, 'bold'), relief=tk.FLAT, cursor='hand2')
        clear_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def add_chat_message(self, sender, message, msg_type="user"):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        
        if msg_type == "user":
            self.chat_display.insert(tk.END, f"[{timestamp}] You: {message}\n\n", "user")
            self.chat_display.tag_config("user", foreground=self.colors['success'])
        elif msg_type == "jarvis":
            self.chat_display.insert(tk.END, f"[{timestamp}] Jarvis: {message}\n\n", "jarvis")
            self.chat_display.tag_config("jarvis", foreground=self.colors['fg'])
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n", "system")
            self.chat_display.tag_config("system", foreground=self.colors['warning'])
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_command(self):
        """Send command to Jarvis"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        self.add_chat_message("You", command, "user")
        self.command_entry.delete(0, tk.END)
        
        # Execute command in separate thread
        threading.Thread(target=self.execute_command, args=(command,), daemon=True).start()
    
    def execute_command(self, command):
        """Execute a Jarvis command"""
        try:
            url = "http://127.0.0.1:8000/api/ask"
            headers = {"Content-Type": "application/json"}
            payload = {"prompt": command}
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response received")
                self.add_chat_message("Jarvis", reply, "jarvis")
            else:
                error_msg = f"Error: HTTP {response.status_code}"
                self.add_chat_message("Jarvis", error_msg, "jarvis")
                
        except requests.exceptions.ConnectionError:
            error_msg = "Cannot connect to Jarvis server. Please ensure Django server is running."
            self.add_chat_message("Jarvis", error_msg, "jarvis")
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.add_chat_message("Jarvis", error_msg, "jarvis")
    
    def toggle_voice_control(self):
        """Toggle voice control"""
        messagebox.showinfo("Voice Control", "Voice control feature coming soon!")
    
    def toggle_face_detection(self):
        """Toggle face detection"""
        if hasattr(self, 'face_detection_active') and self.face_detection_active:
            self.face_detection_active = False
            self.face_btn.config(text="👤 Face Detection: OFF")
            self.add_chat_message("Jarvis", "Face detection deactivated.", "system")
        else:
            self.face_detection_active = True
            self.face_btn.config(text="👤 Face Detection: ON")
            self.add_chat_message("Jarvis", "Face detection activated. I'll greet you when I see your face!", "system")
    
    def open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo("Settings", "Settings panel coming soon!")
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_chat_message("Jarvis", "Chat cleared. How can I help you?", "system")
    
    def setup_status_checker(self):
        """Setup periodic status checking"""
        def check_server_status():
            while True:
                try:
                    response = requests.get("http://127.0.0.1:8000", timeout=2)
                    if response.status_code == 200:
                        self.status_label.config(text="🟢 ONLINE", fg=self.colors['success'])
                    else:
                        self.status_label.config(text="🟡 WARNING", fg=self.colors['warning'])
                except:
                    self.status_label.config(text="🔴 OFFLINE", fg=self.colors['error'])
                
                time.sleep(5)
        
        threading.Thread(target=check_server_status, daemon=True).start()

def main():
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
