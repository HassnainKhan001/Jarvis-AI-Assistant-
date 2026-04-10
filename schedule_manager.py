import json
import os
import threading
import time
from datetime import datetime

try:
    import pyttsx3
    VOICE_ENGINE = "pyttsx3"
except Exception:
    VOICE_ENGINE = "none"

try:
    from plyer import notification
    NOTIF_AVAILABLE = True
except Exception:
    NOTIF_AVAILABLE = False

SCHEDULE_FILE = os.path.join(os.path.dirname(__file__), "hasnain_schedule.json")

class ScheduleManager:
    def __init__(self):
        self.schedule = []
        self.reminded = set()
        self.load_schedule()

    def load_schedule(self):
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.schedule = data.get("schedule", [])
        except Exception:
            self.schedule = []

    def speak(self, text):
        if VOICE_ENGINE == "pyttsx3":
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass

    def notify(self, title, message):
        if NOTIF_AVAILABLE:
            try:
                notification.notify(title=title, message=message, timeout=8)
            except Exception:
                pass

    def get_current_time(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        period = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour}:{minute:02d} {period}"

    def get_current_task(self):
        self.load_schedule()
        now = datetime.now()
        current_mins = now.hour * 60 + now.minute

        current_task = None
        next_task = None
        next_diff = 9999

        for item in self.schedule:
            try:
                t = datetime.strptime(item["time"], "%H:%M")
                task_mins = t.hour * 60 + t.minute
                end_mins = task_mins + item.get("duration_mins", 60)

                if task_mins <= current_mins < end_mins:
                    current_task = item

                diff = task_mins - current_mins
                if 0 < diff < next_diff:
                    next_diff = diff
                    next_task = item
            except Exception:
                continue

        return current_task, next_task, next_diff

    def handle_query(self, prompt):
        p = prompt.lower().strip()

        time_keywords = ["kya time", "kia time", "time kya", "time batao", "time ho raha", "what time", "kitne baje"]
        schedule_keywords = ["schedule", "aaj ka plan", "aaj kya", "din ka plan", "day plan"]
        current_keywords = ["ab kya", "abhi kya", "kya karna", "kya karo", "next kya", "agla kaam", "kya kerna"]
        reminder_keywords = ["reminder shuru", "reminder start", "reminders on"]

        if any(k in p for k in time_keywords):
            current, nxt, diff = self.get_current_task()
            t = self.get_current_time()
            reply = f"Jarvis: Sir, abhi {t} baj rahe hain."
            if current:
                reply += f" Aur abhi aapka kaam hai: {current['task']}."
            if nxt:
                reply += f" Agla kaam '{nxt['task']}' {diff} minute mein hai."
            return reply

        if any(k in p for k in current_keywords):
            current, nxt, diff = self.get_current_task()
            if current:
                reply = f"Jarvis: Sir, abhi aapko '{current['task']}' karna chahiye."
                if current.get("notes"):
                    reply += f" Note: {current['notes']}"
                if nxt:
                    reply += f" Uske baad {diff} minute mein '{nxt['task']}' hai."
                return reply
            elif nxt:
                return f"Jarvis: Sir, abhi koi active task nahi. {diff} minute mein '{nxt['task']}' shuru hoga."
            else:
                return "Jarvis: Sir, aaj ke liye koi aur tasks schedule nahi hain. Free time enjoy karein!"

        if any(k in p for k in schedule_keywords):
            self.load_schedule()
            if not self.schedule:
                return "Jarvis: Sir, abhi schedule file empty hai."
            reply = "Jarvis: Aaj ka schedule yeh hai, sir:\n"
            for item in self.schedule:
                try:
                    t = datetime.strptime(item["time"], "%H:%M")
                    hour = t.hour
                    period = "AM" if hour < 12 else "PM"
                    display = hour if hour <= 12 else hour - 12
                    if display == 0:
                        display = 12
                    reply += f"  {display}:{t.minute:02d} {period} — {item['task']}"
                    if item.get("priority") == "critical":
                        reply += " [IMPORTANT]"
                    reply += "\n"
                except Exception:
                    continue
            return reply.strip()

        if any(k in p for k in reminder_keywords):
            self.start_reminder_loop()
            return "Jarvis: Sir, reminder system shuru ho gaya. Main aapko har kaam se 5 minute pehle bataunga."

        return None

    def reminder_loop(self):
        while True:
            try:
                self.load_schedule()
                now = datetime.now()
                current_mins = now.hour * 60 + now.minute

                for item in self.schedule:
                    try:
                        t = datetime.strptime(item["time"], "%H:%M")
                        task_mins = t.hour * 60 + t.minute
                        diff = task_mins - current_mins
                        key = f"{item['time']}_{item['task']}"

                        if diff == 5 and key not in self.reminded:
                            msg = f"5 minute mein: {item['task']}"
                            self.notify("Jarvis Reminder", msg)
                            self.speak(f"Sir, 5 minute mein {item['task']} shuru hoga.")
                            self.reminded.add(key)

                        if diff == 0 and f"now_{key}" not in self.reminded:
                            msg = f"Ab karo: {item['task']}"
                            self.notify("Jarvis — Ab Karo!", msg)
                            self.speak(f"Sir, ab {item['task']} karna hai.")
                            self.reminded.add(f"now_{key}")

                    except Exception:
                        continue

                # Reset reminded set daily at midnight
                if now.hour == 0 and now.minute == 0:
                    self.reminded.clear()

            except Exception:
                pass

            time.sleep(60)

    def start_reminder_loop(self):
        t = threading.Thread(target=self.reminder_loop, daemon=True)
        t.start()


# Instance — yeh zaroori hai
schedule_manager = ScheduleManager()