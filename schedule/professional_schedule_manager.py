import json
import os
from datetime import datetime, time as dt_time
from typing import Dict, List, Optional

class ProfessionalScheduleManager:
    """
    Professional Schedule Manager for Jarvis
    Manages daily routines, tasks, and provides intelligent reminders
    """
    
    def __init__(self, schedule_file="hasnain_schedule.json"):
        self.schedule_file = schedule_file
        self.schedule_data = self._load_schedule()
        self.notifications = []
    
    def _load_schedule(self) -> Dict:
        """Load schedule from JSON file with error handling"""
        try:
            if os.path.exists(self.schedule_file):
                with open(self.schedule_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Validate data structure
                    if not self._validate_schedule_data(data):
                        print("⚠️  Schedule data corrupted, using default structure")
                        return self._get_default_schedule()
                    return data
            else:
                print("📝 Schedule file not found, creating new one")
                return self._get_default_schedule()
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return self._get_default_schedule()
        except Exception as e:
            print(f"❌ Error loading schedule: {e}")
            return self._get_default_schedule()
    
    def _validate_schedule_data(self, data: Dict) -> bool:
        """Validate schedule data structure"""
        required_keys = ["owner", "daily_routine", "weekly_extras", "custom_tasks"]
        return all(key in data for key in required_keys)
    
    def _get_default_schedule(self) -> Dict:
        """Get default schedule structure"""
        return {
            "owner": "Hasnain",
            "daily_routine": [],
            "weekly_extras": {
                "saturday": [],
                "sunday": []
            },
            "custom_tasks": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_schedule(self) -> bool:
        """Save schedule with backup and validation"""
        try:
            # Create backup
            if os.path.exists(self.schedule_file):
                backup_file = self.schedule_file.replace(".json", "_backup.json")
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(self.schedule_data, f, indent=2, ensure_ascii=False)
            
            # Save main file
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                self.schedule_data["last_updated"] = datetime.now().isoformat()
                json.dump(self.schedule_data, f, indent=2, ensure_ascii=False)
            
            print("✅ Schedule saved successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error saving schedule: {e}")
            return False
    
    def get_current_time_context(self) -> Dict:
        """Get current time context for intelligent responses"""
        now = datetime.now()
        return {
            "current_time": now.strftime("%H:%M"),
            "current_hour": now.hour,
            "current_day": now.strftime("%A"),
            "current_date": now.strftime("%Y-%m-%d"),
            "time_period": self._get_time_period(now.hour),
            "is_weekend": now.weekday() >= 5,  # Saturday=5, Sunday=6
            "is_morning": 6 <= now.hour < 12,
            "is_afternoon": 12 <= now.hour < 17,
            "is_evening": 17 <= now.hour < 21,
            "is_night": now.hour >= 21
        }
    
    def _get_time_period(self, hour: int) -> str:
        """Get time period description"""
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    def get_current_task(self) -> Optional[Dict]:
        """Get current or upcoming task with intelligent matching"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A").lower()
        context = self.get_current_time_context()
        
        # Check daily routine tasks
        for task in self.schedule_data.get("daily_routine", []):
            task_time = task.get("time", "")
            if task_time and current_time >= task_time:
                # Check if task is still relevant (within 2 hours)
                task_hour = int(task_time.split(":")[0])
                current_hour = context["current_hour"]
                
                if current_hour <= task_hour + 2:
                    return {
                        "task": task.get("task", "No task"),
                        "time": task_time,
                        "duration": task.get("duration_mins", 30),
                        "category": task.get("category", "general"),
                        "priority": task.get("priority", "medium"),
                        "notes": task.get("notes", ""),
                        "status": "current",
                        "time_remaining": self._calculate_time_remaining(task_time, current_time)
                    }
        
        # Check weekly extras
        weekly_extras = self.schedule_data.get("weekly_extras", {})
        if current_day in weekly_extras:
            for extra_task in weekly_extras[current_day]:
                task_time = extra_task.get("time", "")
                if task_time and current_time >= task_time:
                    task_hour = int(task_time.split(":")[0])
                    current_hour = context["current_hour"]
                    
                    if current_hour <= task_hour + 4:  # Longer window for weekly tasks
                        return {
                            "task": extra_task.get("task", "No task"),
                            "time": task_time,
                            "duration": extra_task.get("duration_mins", 60),
                            "category": "weekly_extra",
                            "priority": extra_task.get("priority", "medium"),
                            "notes": extra_task.get("notes", ""),
                            "status": "current",
                            "time_remaining": self._calculate_time_remaining(task_time, current_time)
                        }
        
        return None
    
    def _calculate_time_remaining(self, task_time: str, current_time: str) -> str:
        """Calculate remaining time for a task"""
        try:
            task_datetime = datetime.strptime(f"{datetime.now().strftime('%Y-%m-%d')} {task_time}", "%Y-%m-%d %H:%M")
            current_datetime = datetime.strptime(f"{datetime.now().strftime('%Y-%m-%d')} {current_time}", "%Y-%m-%d %H:%M")
            remaining = task_datetime - current_datetime
            
            if remaining.total_seconds() > 0:
                hours, remainder = divmod(remaining.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                return f"{int(hours)}h {int(minutes)}m"
            else:
                return "Overdue"
        except:
            return "Unknown"
    
    def get_today_schedule(self) -> Dict:
        """Get comprehensive today's schedule"""
        context = self.get_current_time_context()
        today_tasks = []
        
        # Add daily routine tasks
        for task in self.schedule_data.get("daily_routine", []):
            task_status = self._get_task_status(task, context)
            today_tasks.append({
                "time": task.get("time", "Unknown"),
                "task": task.get("task", "Unknown"),
                "category": task.get("category", "general"),
                "priority": task.get("priority", "medium"),
                "duration": task.get("duration_mins", 30),
                "notes": task.get("notes", ""),
                "status": task_status
            })
        
        # Add weekly extras for today
        weekly_extras = self.schedule_data.get("weekly_extras", {})
        if context["current_day"] in weekly_extras:
            for extra_task in weekly_extras[context["current_day"]]:
                task_status = self._get_task_status(extra_task, context)
                today_tasks.append({
                    "time": extra_task.get("time", "Unknown"),
                    "task": extra_task.get("task", "Unknown"),
                    "category": "weekly_extra",
                    "priority": extra_task.get("priority", "medium"),
                    "duration": extra_task.get("duration_mins", 60),
                    "notes": extra_task.get("notes", ""),
                    "status": task_status
                })
        
        # Add custom tasks for today
        for task in self.schedule_data.get("custom_tasks", []):
            task_status = self._get_task_status(task, context)
            today_tasks.append(task_status)
        
        return {
            "date": context["current_date"],
            "day": context["current_day"].title(),
            "current_time": context["current_time"],
            "time_period": context["time_period"],
            "context": context,
            "tasks": today_tasks,
            "summary": self._generate_day_summary(today_tasks, context),
            "owner": self.schedule_data.get("owner", "Hasnain")
        }
    
    def _get_task_status(self, task: Dict, context: Dict) -> str:
        """Determine task status based on time"""
        task_time = task.get("time", "")
        current_time = context["current_time"]
        
        if not task_time:
            return "pending"
        
        try:
            task_hour = int(task_time.split(":")[0])
            current_hour = context["current_hour"]
            
            if current_time >= task_time:
                if current_hour <= task_hour + 1:
                    return "current"
                elif current_hour <= task_hour + 2:
                    return "active"
                else:
                    return "missed"
            else:
                return "upcoming"
        except:
            return "unknown"
    
    def _generate_day_summary(self, tasks: List[Dict], context: Dict) -> str:
        """Generate intelligent summary of the day"""
        if not tasks:
            return f"No tasks scheduled for {context['current_day']}."
        
        completed = sum(1 for task in tasks if task.get("status") == "completed")
        current = sum(1 for task in tasks if task.get("status") == "current")
        pending = sum(1 for task in tasks if task.get("status") == "pending")
        
        total_tasks = len(tasks)
        
        if completed > 0:
            return f"Great progress! {completed}/{total_tasks} completed today."
        elif current > 0:
            return f"Good focus! {current}/{total_tasks} tasks in progress."
        elif pending > 0:
            return f"{pending}/{total_tasks} tasks remaining today."
        else:
            return f"{total_tasks} tasks scheduled for today."
    
    def add_task(self, task_data: Dict) -> tuple[bool, str]:
        """Add a new task with validation"""
        try:
            # Validate task data
            required_fields = ["task", "time", "duration_mins"]
            for field in required_fields:
                if field not in task_data:
                    return False, f"Missing required field: {field}"
            
            # Add default values
            task_data.setdefault("category", "custom")
            task_data.setdefault("priority", "medium")
            task_data.setdefault("notes", "")
            task_data.setdefault("created_date", datetime.now().isoformat())
            
            # Add to schedule
            self.schedule_data["custom_tasks"].append(task_data)
            success = self._save_schedule()
            
            if success:
                return True, f"Task '{task_data['task']}' added successfully for {task_data.get('time', 'unknown')}"
            else:
                return False, "Failed to save task"
                
        except Exception as e:
            return False, f"Error adding task: {str(e)}"
    
    def update_task(self, task_index: int, updated_data: Dict) -> tuple[bool, str]:
        """Update an existing task"""
        try:
            custom_tasks = self.schedule_data.get("custom_tasks", [])
            if 0 <= task_index < len(custom_tasks):
                # Update task with new data
                custom_tasks[task_index].update(updated_data)
                custom_tasks[task_index]["updated_date"] = datetime.now().isoformat()
                
                success = self._save_schedule()
                if success:
                    return True, f"Task updated successfully"
                else:
                    return False, "Failed to save updated task"
            else:
                return False, "Task index out of range"
        except Exception as e:
            return False, f"Error updating task: {str(e)}"
    
    def complete_task(self, task_index: int) -> tuple[bool, str]:
        """Mark a task as completed"""
        try:
            custom_tasks = self.schedule_data.get("custom_tasks", [])
            if 0 <= task_index < len(custom_tasks):
                custom_tasks[task_index]["status"] = "completed"
                custom_tasks[task_index]["completed_date"] = datetime.now().isoformat()
                
                success = self._save_schedule()
                if success:
                    return True, f"Task '{custom_tasks[task_index]['task']}' marked as completed"
                else:
                    return False, "Failed to save task completion"
            else:
                return False, "Task index out of range"
        except Exception as e:
            return False, f"Error completing task: {str(e)}"
    
    def get_productivity_insights(self) -> Dict:
        """Get productivity insights and analytics"""
        custom_tasks = self.schedule_data.get("custom_tasks", [])
        
        total_tasks = len(custom_tasks)
        completed_tasks = sum(1 for task in custom_tasks if task.get("status") == "completed")
        
        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Task distribution by category
        categories = {}
        for task in custom_tasks:
            category = task.get("category", "general")
            categories[category] = categories.get(category, 0) + 1
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completion_rate,
            "categories": categories,
            "last_updated": self.schedule_data.get("last_updated")
        }
    
    def handle_schedule_query(self, query: str) -> str:
        """Handle schedule-related queries with intelligent responses"""
        query_lower = query.lower().strip()
        context = self.get_current_time_context()
        
        # Current task queries
        if any(phrase in query_lower for phrase in ["current task", "what should i do", "what's next", "what's upcoming"]):
            current_task = self.get_current_task()
            if current_task:
                return f"📋 Current Task: {current_task['task']} ({current_task['time']}) - {current_task['notes']}. Time remaining: {current_task.get('time_remaining', 'N/A')}"
            else:
                return f"✅ No current task. You're free! Next task starts at {self._get_next_task_time()}"
        
        # Today's schedule queries
        if any(phrase in query_lower for phrase in ["today schedule", "what's today", "show today", "today's tasks"]):
            today_schedule = self.get_today_schedule()
            return f"📅 Today's Schedule ({today_schedule['day']}):\n{self._format_today_tasks(today_schedule['tasks'])}"
        
        # Task management queries
        if "add task" in query_lower:
            return "📝 To add a task, please provide: task name, time, and duration (optional). Example: 'Add task: Complete project report at 14:00'"
        
        if "complete task" in query_lower:
            return "✅ To complete a task, say: 'Complete task: [task name or number]'"
        
        # Productivity queries
        if any(phrase in query_lower for phrase in ["productivity", "progress", "how am i doing", "stats"]):
            insights = self.get_productivity_insights()
            return f"📊 Productivity Insights: {insights['completed_tasks']}/{insights['total_tasks']} tasks completed ({insights['completion_rate']:.1f}% completion rate)"
        
        # Time-based queries
        if "what time" in query_lower:
            return f"⏰ Current time: {context['current_time']} ({context['time_period'].title()})"
        
        return "📅 I can help you with your schedule. Try: 'current task', 'today schedule', 'add task', 'productivity stats', or 'what time'"
    
    def _get_next_task_time(self) -> str:
        """Get time of next scheduled task"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # Check all tasks for next time
        all_tasks = []
        
        # Add daily routine tasks
        for task in self.schedule_data.get("daily_routine", []):
            task_time = task.get("time", "")
            if task_time and task_time > current_time:
                all_tasks.append(task_time)
        
        # Add weekly extras
        weekly_extras = self.schedule_data.get("weekly_extras", {})
        current_day = now.strftime("%A").lower()
        if current_day in weekly_extras:
            for extra_task in weekly_extras[current_day]:
                task_time = extra_task.get("time", "")
                if task_time and task_time > current_time:
                    all_tasks.append(task_time)
        
        # Add custom tasks
        for task in self.schedule_data.get("custom_tasks", []):
            task_time = task.get("time", "")
            if task_time and task_time > current_time:
                all_tasks.append(task_time)
        
        if all_tasks:
            return min(all_tasks)
        else:
            return "No upcoming tasks"
    
    def _format_today_tasks(self, tasks: List[Dict]) -> str:
        """Format today's tasks for display"""
        if not tasks:
            return "No tasks scheduled"
        
        formatted_tasks = []
        for task in tasks:
            status_icon = "✅" if task.get("status") == "completed" else "🔄" if task.get("status") == "current" else "⏳"
            time_info = f" ({task.get('time_remaining', '')})" if task.get('time_remaining') else ""
            
            formatted_tasks.append(
                f"{status_icon} {task.get('time', '???:??')} - {task.get('task', 'Unknown Task')}{time_info} [{task.get('priority', 'M').upper()}]"
            )
        
        return "\n".join(formatted_tasks)

# Global professional schedule manager instance
professional_schedule = ProfessionalScheduleManager()
