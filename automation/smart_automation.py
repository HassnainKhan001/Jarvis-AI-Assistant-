import time
import pyautogui
import subprocess
import webbrowser
import threading
import json
import os
from datetime import datetime, timedelta
import logging

class SmartAutomation:
    def __init__(self):
        self.automations = {}
        self.running_automations = {}
        self.scheduled_tasks = {}
        self.load_automations()
        
        # Setup logging
        logging.basicConfig(
            filename='automation.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def load_automations(self):
        """Load predefined automations"""
        self.automations = {
            # Trading automation
            "trading_routine": {
                "description": "Open all trading apps and websites",
                "actions": [
                    {"type": "open_website", "url": "https://www.tradingview.com"},
                    {"type": "wait", "seconds": 2},
                    {"type": "open_app", "app": "chrome"},
                    {"type": "wait", "seconds": 1},
                    {"type": "search_google", "query": "market news today"},
                    {"type": "wait", "seconds": 3},
                    {"type": "auto_click_result"}
                ]
            },
            
            # Morning routine
            "morning_routine": {
                "description": "Start your day with essential apps",
                "actions": [
                    {"type": "open_app", "app": "chrome"},
                    {"type": "wait", "seconds": 2},
                    {"type": "open_website", "url": "https://gmail.com"},
                    {"type": "wait", "seconds": 3},
                    {"type": "open_app", "app": "spotify"},
                    {"type": "open_website", "url": "https://news.google.com"}
                ]
            },
            
            # Work setup
            "work_setup": {
                "description": "Setup workspace for productivity",
                "actions": [
                    {"type": "open_app", "app": "code"},
                    {"type": "wait", "seconds": 2},
                    {"type": "open_app", "app": "chrome"},
                    {"type": "wait", "seconds": 1},
                    {"type": "open_website", "url": "https://github.com"},
                    {"type": "open_app", "app": "discord"},
                    {"type": "volume_up", "times": 3}
                ]
            },
            
            # Entertainment setup
            "entertainment_setup": {
                "description": "Setup entertainment apps",
                "actions": [
                    {"type": "open_app", "app": "spotify"},
                    {"type": "wait", "seconds": 2},
                    {"type": "open_website", "url": "https://www.youtube.com"},
                    {"type": "volume_up", "times": 5}
                ]
            },
            
            # System cleanup
            "system_cleanup": {
                "description": "Perform system cleanup",
                "actions": [
                    {"type": "show_desktop"},
                    {"type": "wait", "seconds": 1},
                    {"type": "open_app", "app": "taskmgr"},
                    {"type": "wait", "seconds": 2},
                    {"type": "message", "text": "System cleanup started. Check Task Manager."}
                ]
            }
        }
    
    def execute_automation(self, automation_name, delay=0):
        """Execute a predefined automation"""
        if automation_name not in self.automations:
            return f"Automation '{automation_name}' not found."
        
        def run_automation():
            if delay > 0:
                time.sleep(delay)
            
            automation = self.automations[automation_name]
            logging.info(f"Starting automation: {automation_name}")
            
            for i, action in enumerate(automation["actions"]):
                try:
                    self.execute_action(action)
                    logging.info(f"Action {i+1}/{len(automation['actions'])} completed")
                except Exception as e:
                    logging.error(f"Action {i+1} failed: {e}")
            
            logging.info(f"Automation '{automation_name}' completed")
            return f"Automation '{automation_name}' completed successfully!"
        
        # Run in separate thread
        thread = threading.Thread(target=run_automation, daemon=True)
        thread.start()
        self.running_automations[automation_name] = thread
        
        return f"Starting automation: {automation['description']}"
    
    def execute_action(self, action):
        """Execute a single action"""
        action_type = action["type"]
        
        if action_type == "open_app":
            self.open_application(action["app"])
        
        elif action_type == "open_website":
            webbrowser.open(action["url"])
        
        elif action_type == "wait":
            time.sleep(action["seconds"])
        
        elif action_type == "search_google":
            self.search_and_click(action["query"])
        
        elif action_type == "auto_click_result":
            self.auto_click_search_result()
        
        elif action_type == "volume_up":
            times = action.get("times", 1)
            for _ in range(times):
                pyautogui.press('volumeup')
        
        elif action_type == "volume_down":
            times = action.get("times", 1)
            for _ in range(times):
                pyautogui.press('volumedown')
        
        elif action_type == "mute":
            pyautogui.press('volumemute')
        
        elif action_type == "show_desktop":
            pyautogui.hotkey('win', 'd')
        
        elif action_type == "message":
            print(f"Jarvis: {action['text']}")
        
        elif action_type == "type_text":
            pyautogui.write(action["text"], interval=0.05)
        
        elif action_type == "key_combination":
            keys = action["keys"].split('+')
            if len(keys) == 2:
                pyautogui.hotkey(keys[0], keys[1])
            elif len(keys) == 3:
                pyautogui.hotkey(keys[0], keys[1], keys[2])
    
    def open_application(self, app_name):
        """Open an application"""
        app_commands = {
            "chrome": "chrome",
            "firefox": "firefox",
            "edge": "msedge",
            "code": "code",
            "spotify": "spotify",
            "discord": "discord",
            "taskmgr": "taskmgr",
            "notepad": "notepad",
            "cmd": "cmd"
        }
        
        command = app_commands.get(app_name.lower(), app_name)
        
        try:
            subprocess.Popen([command], shell=True)
        except Exception as e:
            # Fallback to Windows Search
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write(app_name, interval=0.01)
            time.sleep(0.6)
            pyautogui.press('enter')
    
    def search_and_click(self, query):
        """Search Google and auto-click first result"""
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        time.sleep(3)
        self.auto_click_search_result()
    
    def auto_click_search_result(self):
        """Auto-click first search result"""
        try:
            pyautogui.press('tab', presses=5, interval=0.2)
            time.sleep(0.5)
            pyautogui.press('enter')
        except Exception as e:
            logging.error(f"Auto-click failed: {e}")
    
    def create_custom_automation(self, name, description, actions):
        """Create a custom automation"""
        self.automations[name] = {
            "description": description,
            "actions": actions
        }
        self.save_automations()
        return f"Custom automation '{name}' created successfully!"
    
    def schedule_automation(self, automation_name, schedule_time):
        """Schedule an automation to run at a specific time"""
        if automation_name not in self.automations:
            return f"Automation '{automation_name}' not found."
        
        def scheduled_run():
            while True:
                current_time = datetime.now().strftime("%H:%M")
                if current_time == schedule_time:
                    self.execute_automation(automation_name)
                    time.sleep(60)  # Wait 1 minute to avoid multiple runs
                time.sleep(30)  # Check every 30 seconds
        
        thread = threading.Thread(target=scheduled_run, daemon=True)
        thread.start()
        self.scheduled_tasks[automation_name] = {"time": schedule_time, "thread": thread}
        
        return f"Automation '{automation_name}' scheduled for {schedule_time}"
    
    def save_automations(self):
        """Save automations to file"""
        try:
            with open('custom_automations.json', 'w') as f:
                json.dump(self.automations, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save automations: {e}")
    
    def load_custom_automations(self):
        """Load custom automations from file"""
        try:
            if os.path.exists('custom_automations.json'):
                with open('custom_automations.json', 'r') as f:
                    custom = json.load(f)
                    self.automations.update(custom)
        except Exception as e:
            logging.error(f"Failed to load custom automations: {e}")
    
    def get_automation_list(self):
        """Get list of available automations"""
        return list(self.automations.keys())
    
    def get_automation_info(self, automation_name):
        """Get information about a specific automation"""
        if automation_name in self.automations:
            return self.automations[automation_name]
        return None

# Global automation instance
automation_engine = SmartAutomation()
