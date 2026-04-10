from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import subprocess
import signal
import sys
from .utils import process_query

@csrf_exempt
def assistant_api(request):
    """
    API endpoint for interacting with Jarvis.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            if not prompt:
                return JsonResponse({'error': 'No prompt provided.'}, status=400)
            
            response_text = process_query(prompt)
            return JsonResponse({'response': response_text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

# --- Background Listener Management ---

LISTENER_PID_FILE = "listener_pid.txt"

@csrf_exempt
def toggle_listener(request):
    """
    Start or stop the standalone listener.py background process.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            should_run = data.get('enable', False)
            
            # Check if already running
            current_pid = None
            if os.path.exists(LISTENER_PID_FILE):
                with open(LISTENER_PID_FILE, "r") as f:
                    try:
                        current_pid = int(f.read().strip())
                    except ValueError:
                        pass

            if should_run:
                if current_pid:
                    # Still running?
                    try:
                        os.kill(current_pid, 0) # Signal 0 checks if it exists
                        return JsonResponse({'status': 'already_running', 'pid': current_pid})
                    except OSError:
                        pass # Process doesn't exist, proceed to start

                # Start listener.py
                # Use sys.executable to ensure we use the same Python environment
                # Use subprocess.Popen with creationflags=subprocess.CREATE_NEW_PROCESS_GROUP or DETACHED_PROCESS for Windows
                process = subprocess.Popen(
                    [sys.executable, "listener.py"],
                    cwd=os.getcwd(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
                )
                
                with open(LISTENER_PID_FILE, "w") as f:
                    f.write(str(process.pid))
                    
                return JsonResponse({'status': 'started', 'pid': process.pid})
            
            else:
                if current_pid:
                    try:
                        os.kill(current_pid, signal.SIGTERM)
                        if os.path.exists(LISTENER_PID_FILE):
                            os.remove(LISTENER_PID_FILE)
                        return JsonResponse({'status': 'stopped'})
                    except Exception:
                        # Fallback for Windows
                        os.system(f"taskkill /F /PID {current_pid}")
                        if os.path.exists(LISTENER_PID_FILE):
                            os.remove(LISTENER_PID_FILE)
                        return JsonResponse({'status': 'stopped'})
                return JsonResponse({'status': 'not_running'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    # GET status
    is_running = False
    if os.path.exists(LISTENER_PID_FILE):
        with open(LISTENER_PID_FILE, "r") as f:
            try:
                pid = int(f.read().strip())
                os.kill(pid, 0)
                is_running = True
            except (OSError, ValueError):
                pass
        
        # Additional health check: is the log file being updated?
        if is_running and os.path.exists("listener.log"):
            log_mtime = os.path.getmtime("listener.log")
            if time.time() - log_mtime > 600: # No log update for 10 minutes
                # It might be hung even if PID exists
                pass

    return JsonResponse({'is_running': is_running})
