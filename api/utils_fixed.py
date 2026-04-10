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

load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=AI_API_KEY)

# Conversation history for context
conversation_history = []

def process_query(prompt, retries=3):
    """
    Process the user query using advanced NLU and AI
    """
    if not AI_API_KEY or AI_API_KEY == "your_api_key_here":
        return "Jarvis: I need a valid API key in the .env file to think."

    # First, use advanced NLU to understand the intent
    intent = nlu_engine.parse_intent(prompt)
    structured_response = nlu_engine.generate_structured_response(intent)
    
    # Execute the structured response
    return execute_structured_response(structured_response, prompt)

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
