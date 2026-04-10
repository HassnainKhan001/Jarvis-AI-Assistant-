import os
import time
import subprocess
import webbrowser
import re
import pyautogui
from dotenv import load_dotenv
from google import genai
import threading
from automation.smart_automation import automation_engine
from ai.advanced_nlu import nlu_engine, StructuredResponse
from ai.ultra_fast_nlu import ultra_fast_nlu, UltraFastResponse
from schedule.professional_schedule_manager import professional_schedule

load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=AI_API_KEY)

# Conversation history for context
conversation_history = []

# Quota management
quota_usage = {
    "daily_requests": 0,
    "last_reset": time.strftime("%Y-%m-%d"),
    "quota_limit": 15,  # Conservative limit (free tier is 20)
    "quota_exceeded": False,
    "retry_after": 0
}

def check_quota():
    """Check if we've exceeded the API quota"""
    current_date = time.strftime("%Y-%m-%d")
    
    # Reset daily counter if it's a new day
    if quota_usage["last_reset"] != current_date:
        quota_usage["daily_requests"] = 0
        quota_usage["last_reset"] = current_date
        quota_usage["quota_exceeded"] = False
        quota_usage["retry_after"] = 0
    
    # Check if we need to wait for retry
    if quota_usage["retry_after"] > time.time():
        return False, f"Jarvis: I apologize, sir. I've reached my daily thinking limit. Please try again in {int((quota_usage['retry_after'] - time.time()) / 60)} minutes."
    
    # Check if we've exceeded the quota
    if quota_usage["daily_requests"] >= quota_usage["quota_limit"]:
        quota_usage["quota_exceeded"] = True
        # Set retry time to tomorrow
        tomorrow = time.time() + (24 * 60 * 60)  # 24 hours from now
        quota_usage["retry_after"] = tomorrow
        return False, "Jarvis: I apologize, sir. I've reached my daily thinking limit. I'll be ready again tomorrow. For now, I can help with basic tasks like telling time, opening websites, or checking your schedule."
    
    return True, "Quota available"

def increment_quota():
    """Increment the quota counter"""
    quota_usage["daily_requests"] += 1
    print(f"Quota usage: {quota_usage['daily_requests']}/{quota_usage['quota_limit']}")

def get_quota_status():
    """Get current quota status"""
    current_date = time.strftime("%Y-%m-%d")
    if quota_usage["last_reset"] != current_date:
        return f"Jarvis: Daily quota reset. Available: {quota_usage['quota_limit']}/{quota_usage['quota_limit']}"
    
    remaining = quota_usage["quota_limit"] - quota_usage["daily_requests"]
    return f"Jarvis: Quota status: {remaining}/{quota_usage['quota_limit']} requests remaining today."

def process_query(prompt, retries=3):
    """
    Process the user query using ULTRA-FAST NLU for instant response
    """
    if not AI_API_KEY or AI_API_KEY == "your_api_key_here":
        return "Jarvis: I need a valid API key in the .env file to think."

    prompt_lower = prompt.lower().strip()
    
    # Remove wake words
    clean_prompt = prompt_lower
    for wake_word in ["hey jarvis", "hi jarvis", "hello jarvis", "jarvis"]:
        if clean_prompt.startswith(wake_word):
            clean_prompt = clean_prompt[len(wake_word):].strip()
            while clean_prompt and clean_prompt[0] in ",.!?:\";'- ":
                clean_prompt = clean_prompt[1:]
            break
    clean_prompt = clean_prompt.strip()

    # --- INSTANT RESPONSES (Fastest Path) ---
    
    # Time questions
    if "what time" in clean_prompt:
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p on %A, %B %d, %Y")
        return f"Jarvis: ⏰ Current time: {current_time}"
    
    # Pakistan knowledge (instant)
    if "founder of pakistan" in clean_prompt:
        return "Jarvis: Quaid-e-Azam Muhammad Ali Jinnah is the founder of Pakistan. He is known as the Father of the Nation and led the Pakistan Movement."
    
    if "capital of pakistan" in clean_prompt:
        return "Jarvis: Islamabad is the capital of Pakistan. It was built in the 1960s to replace Karachi as the capital."
    
    # Help command (instant)
    if "help" in clean_prompt or "commands" in clean_prompt:
        return "Jarvis: I can help you with: time queries, system status, opening websites, schedule management, quota status, and general assistance. Try asking 'what time is it', 'system status', or 'quota status'."
    
    # Quota status (instant)
    if "quota status" in clean_prompt or "quota" in clean_prompt or "limit" in clean_prompt:
        return get_quota_status()
    
    # System status (instant)
    if "system status" in clean_prompt or "status" in clean_prompt:
        return "Jarvis: All systems operational, sir. Neural networks active, biometric scanners online, and voice recognition fully functional. Ready for your commands."
    
    # Performance metrics (instant)
    if "performance metrics" in clean_prompt or "performance" in clean_prompt:
        return "Jarvis: Current performance metrics are excellent, sir. Processing speed at peak capacity, response time under 30 milliseconds, and all systems functioning at optimal levels."
    
    # Self introduction (instant)
    if "tell me about yourself" in clean_prompt or "about yourself" in clean_prompt or "who are you" in clean_prompt:
        return "Jarvis: I am J.A.R.V.I.S., your advanced AI assistant, sir. I am designed to help you with professional schedule management, voice commands, and system monitoring. All systems are currently online and ready to assist you."
    
    # YouTube commands
    if "open youtube" in clean_prompt:
        webbrowser.open("https://www.youtube.com")
        return "Jarvis: Opening YouTube for you. ⚡"
    
    if "play" in clean_prompt and "youtube" in clean_prompt:
        search_term = clean_prompt.replace("play", "").replace("youtube", "").strip()
        if search_term:
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
            return f"Jarvis: Playing {search_term} on YouTube. ⚡"
        else:
            webbrowser.open("https://www.youtube.com")
            return "Jarvis: Opening YouTube. ⚡"
    
    # Google search
    if "search google" in clean_prompt:
        query = clean_prompt.replace("search google for", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Jarvis: Searching Google for {query}. ⚡"
    
    # WhatsApp
    if "open whatsapp" in clean_prompt:
        webbrowser.open("https://web.whatsapp.com")
        return "Jarvis: Opening WhatsApp. ⚡"
    
    # Application opening
    if clean_prompt.startswith("open "):
        app_name = clean_prompt[5:].strip()
        
        app_commands = {
            "chrome": "chrome",
            "firefox": "firefox", 
            "edge": "msedge",
            "spotify": "spotify",
            "discord": "discord",
            "notepad": "notepad",
            "cmd": "cmd"
        }
        
        command = app_commands.get(app_name.lower(), app_name)
        
        try:
            subprocess.Popen([command], shell=True)
            return f"Jarvis: Opening {app_name.title()}. ⚡"
        except Exception:
            # Fallback to Windows Search
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write(app_name, interval=0.01)
            time.sleep(0.6)
            pyautogui.press('enter')
            return f"Jarvis: Opening {app_name.title()}. ⚡"
    
    # --- SCHEDULE QUERIES (Professional Management) ---
    # Check for schedule queries specifically
    if any(phrase in clean_prompt for phrase in ["current task", "what should i do", "what's next", "today schedule", "productivity", "add task", "complete task"]):
        schedule_response = professional_schedule.handle_schedule_query(prompt)
        if schedule_response != "📅 I can help you with your schedule. Try: 'current task', 'today schedule', 'add task', 'productivity stats', or 'what time'":
            return f"Jarvis: {schedule_response}"
    
    # Check quota before making AI calls
    quota_available, quota_message = check_quota()
    if not quota_available:
        return quota_message
    
    # --- AI FALLBACK ---
    # Add user message to history
    conversation_history.append({"role": "user", "parts": [{"text": prompt}]})

    # Try AI for complex queries with timeout handling
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

    for model in models:
        for attempt in range(retries):
            try:
                # Use threading for timeout instead of signal (Windows compatible)
                import threading
                import queue
                
                result_queue = queue.Queue()
                
                def ai_call():
                    try:
                        response = client.models.generate_content(
                            model=model,
                            contents=conversation_history,
                            config={
                                "system_instruction": "You are Jarvis, a highly advanced, helpful, and slightly witty AI assistant inspired by Iron Man's Jarvis. Keep responses concise but insightful. Address the user respectfully as 'sir'. Do not use markdown formatting in responses.",
                                "max_output_tokens": 150,  # Further reduced for quota management
                            }
                        )
                        result_queue.put(("success", response.text))
                    except Exception as e:
                        result_queue.put(("error", str(e)))
                
                # Start AI call in thread
                thread = threading.Thread(target=ai_call)
                thread.daemon = True
                thread.start()
                
                # Wait for result with timeout
                try:
                    status, result = result_queue.get(timeout=5)  # Reduced timeout for quota management
                    
                    if status == "success":
                        # Increment quota usage
                        increment_quota()
                        
                        # Add assistant response to history
                        conversation_history.append({"role": "model", "parts": [{"text": result}]})
                        return result
                    else:
                        if attempt < retries - 1:
                            time.sleep(1)
                            continue
                        else:
                            return "Jarvis: I apologize, sir. The neural network is taking longer than expected. Let me assist you with something else."
                        
                except queue.Empty:
                    if attempt < retries - 1:
                        continue
                    else:
                        return "Jarvis: I apologize, sir. The neural network is taking longer than expected. Let me assist you with something else."
                        
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    # Mark quota as exceeded
                    quota_usage["quota_exceeded"] = True
                    quota_usage["retry_after"] = time.time() + (24 * 60 * 60)  # 24 hours from now
                    
                    if attempt < retries - 1:
                        time.sleep(1)  # Reduced wait time
                        continue
                    else:
                        return "Jarvis: I apologize, sir. I've reached my daily thinking limit. I'll be ready again tomorrow. For now, I can help with basic tasks like telling time, opening websites, or checking your schedule."
                elif "NOT_FOUND" in error_msg:
                    break
                elif "11001" in error_msg or "10060" in error_msg or "WinError" in error_msg:
                    return "Jarvis: Sir, I am having trouble connecting to the network right now."
                return f"Jarvis Error: {error_msg}"

    return "Jarvis: I'm processing your request, sir. Please give me a moment to think."

def execute_structured_response(structured_response: StructuredResponse, original_prompt: str) -> str:
    """
    Execute a structured response and handle the actions
    """
    # Execute all actions
    for action in structured_response.actions:
        execute_action(action)
    
    # If we have a predefined response, use it
    if structured_response.response:
        result = f"Jarvis: {structured_response.response}"
        
        # Add follow-up if available
        if structured_response.follow_up:
            result += f" {structured_response.follow_up}"
        
        return result
    
    # Otherwise, use AI for complex queries
    return process_with_ai(original_prompt)

def execute_action(action):
    """
    Execute a single action from the structured response
    """
    action_type = action.get("type")
    
    if action_type == "open_website":
        webbrowser.open(action["url"])
    
    elif action_type == "open_app":
        # Handle YouTube specifically
        if "youtube" in action.get("app", "").lower():
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube..."
        else:
            open_application(action["app"])
    
    elif action_type == "google_search":
        search_url = f"https://www.google.com/search?q={action['query']}"
        webbrowser.open(search_url)
    
    elif action_type == "auto_click_result":
        # Auto-click after a delay
        def click_after_delay():
            time.sleep(3)
            try:
                pyautogui.press('tab', presses=5, interval=0.2)
                time.sleep(0.5)
                pyautogui.press('enter')
            except:
                pass
        
        threading.Thread(target=click_after_delay, daemon=True).start()
    
    elif action_type == "search_youtube":
        # Search YouTube
        search_url = f"https://www.youtube.com/results?search_query={action['query']}"
        webbrowser.open(search_url)
    
    elif action_type == "wait":
        time.sleep(action["seconds"])
    
    elif action_type == "run_automation":
        automation_engine.execute_automation(action["name"])
    
    elif action_type == "ai_query":
        # This will be handled by the AI processing
        pass
    
    elif action_type == "ai_conversation":
        # This will be handled by the AI processing
        pass
    
    elif action_type == "execute_command":
        # Handle legacy commands
        pass  # Will be handled by the original system

def open_application(app_name):
    """Open an application by name"""
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
    except Exception:
        # Fallback to Windows Search
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(app_name, interval=0.01)
        time.sleep(0.6)
        pyautogui.press('enter')

def process_with_ai(prompt, retries=3):
    """
    Process the user query using Google Gemini API with retry logic.
    """
    prompt_lower = prompt.lower().strip()

    # Remove wake words and leading punctuation
    clean_prompt = prompt_lower
    for wake_word in ["hey jarvis", "hi jarvis", "hello jarvis", "jarvis"]:
        if clean_prompt.startswith(wake_word):
            clean_prompt = clean_prompt[len(wake_word):].strip()
            while clean_prompt and clean_prompt[0] in ",.!?:\";'- ":
                clean_prompt = clean_prompt[1:]
            break
            
    clean_prompt = clean_prompt.strip()

    # --- System Command Interception ---
    if "chatgpt" in clean_prompt or "chat gpt" in clean_prompt:
        webbrowser.open("https://chat.openai.com")
        return "Jarvis: Opening ChatGPT, sir."
        
    elif "antigravity" in clean_prompt:
        # A fun easter egg for Antigravity
        return "Jarvis: Antigravity is online and ready serving your requests, sir!"

    # --- Standard AI Chat (if no system command matched) ---

    # Add user message to history
    conversation_history.append({"role": "user", "parts": [{"text": prompt}]})

    # Models to try in order
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

    for model in models:
        for attempt in range(retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=conversation_history,
                    config={
                        "system_instruction": "You are Jarvis, a highly advanced, helpful, and slightly witty AI assistant inspired by Iron Man's Jarvis. You have full access to the user's local operating system via a backend automation engine. If the user asks to open settings, show the desktop, control volume, or lock the PC, you should confirm that you are doing it. Do not say you lack physical access, as your core is integrated with the system. Keep responses concise but insightful. Address the user respectfully. Do not use markdown formatting in responses.",
                        "max_output_tokens": 500,
                    }
                )
                result = response.text
                # Add assistant response to history
                conversation_history.append({"role": "model", "parts": [{"text": result}]})
                return result
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    if attempt < retries - 1:
                        time.sleep(15)  # Wait 15 seconds before retry
                        continue
                    break  # Try next model
                elif "NOT_FOUND" in error_msg:
                    break  # Skip to next model
                elif "11001" in error_msg or "10060" in error_msg or "WinError" in error_msg:
                    return "Jarvis: Sir, I am having trouble connecting to the network right now. Please check your internet connection."
                return f"Jarvis Error: {error_msg}"

    return "Jarvis: I'm currently rate-limited across all models. Please wait about 60 seconds and try again. This is a free-tier limitation."
