import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class IntentType(Enum):
    COMMAND = "command"
    QUESTION = "question"
    CONVERSATION = "conversation"
    SEARCH = "search"
    AUTOMATION = "automation"
    INFORMATION = "information"
    EMERGENCY = "emergency"
    CALCULATION = "calculation"
    COMPARISON = "comparison"
    RECOMMENDATION = "recommendation"

@dataclass
class Intent:
    type: IntentType
    action: str
    entities: Dict[str, str]
    confidence: float
    original_text: str
    urgency: int  # 1-10 scale
    complexity: str  # simple, medium, complex

@dataclass
class UltraFastResponse:
    intent: Intent
    response: str
    actions: List[Dict]
    follow_up: Optional[str]
    response_time: float  # milliseconds
    confidence: float
    priority: str  # low, medium, high, critical

class UltraFastNLU:
    def __init__(self):
        # Ultra-fast pattern matching for instant recognition
        self.instant_patterns = {
            # Emergency commands (highest priority)
            IntentType.EMERGENCY: [
                r'(?:help|emergency|stop|abort|cancel)',
                r'(?:urgent|immediate|asap)',
                r'(?:danger|warning|alert)',
            ],
            
            # Questions with instant knowledge
            IntentType.QUESTION: [
                r'(?:what|who|where|when|why|how)\s+(.+)',
                r'(?:is|are|was|were)\s+(.+)',
                r'(?:tell|explain|describe)\s+(.+)',
                r'(?:define|meaning of)\s+(.+)',
                r'(?:compare|difference|vs)\s+(.+)',
                r'(?:calculate|compute|solve)\s+(.+)',
            ],
            
            # Commands with instant action
            IntentType.COMMAND: [
                r'(?:open|launch|start)\s+(.+)',
                r'(?:close|shutdown|exit|stop)\s+(.+)',
                r'(?:play|pause|resume|stop)\s+(.+)',
                r'(?:search|find|look for)\s+(.+)',
                r'(?:show|display|hide)\s+(.+)',
                r'(?:increase|decrease|mute|unmute)\s+(.+)',
            ],
            
            # Smart search with context
            IntentType.SEARCH: [
                r'(?:search|find|look for)\s+(.+?)(?:\s+(?:on|in|at)\s+(.+))?',
                r'(?:google|bing|youtube)\s+(.+)',
                r'(?:find|search)\s+(?:information|about)\s+(.+)',
            ],
            
            # Automation triggers
            IntentType.AUTOMATION: [
                r'(?:start|run|execute|activate)\s+(?:automation|routine)\s+(.+)',
                r'(?:quick|fast|immediate)\s+(.+)',
                r'(?:morning|evening|night)\s+(?:routine|mode)',
                r'(?:work|study|focus)\s+mode',
            ],
        }
        
        # Ultra-fast entity extraction
        self.entity_patterns = {
            'applications': [
                'youtube', 'spotify', 'chrome', 'firefox', 'edge', 'vs code',
                'discord', 'teams', 'zoom', 'tradingview', 'gmail',
                'word', 'excel', 'powerpoint', 'photoshop', 'vlc',
                'notepad', 'calculator', 'camera', 'settings', 'control panel'
            ],
            'websites': [
                'google', 'youtube', 'facebook', 'twitter', 'instagram',
                'linkedin', 'github', 'stackoverflow', 'reddit', 'wikipedia'
            ],
            'media_types': [
                'song', 'music', 'video', 'movie', 'playlist', 'album',
                'podcast', 'audiobook', 'documentary'
            ],
            'actions': [
                'open', 'close', 'play', 'pause', 'stop', 'search', 'find',
                'show', 'hide', 'start', 'stop', 'increase', 'decrease'
            ],
            'quantities': [
                'volume', 'brightness', 'speed', 'temperature', 'size'
            ],
            'time_references': [
                'now', 'today', 'tomorrow', 'yesterday', 'morning', 'evening',
                'tonight', 'week', 'month', 'year', 'urgent'
            ]
        }
        
        # Instant knowledge base for common questions
        self.knowledge_base = {
            # Pakistan facts (instant answers)
            'founder of pakistan': 'Quaid-e-Azam Muhammad Ali Jinnah is the founder of Pakistan. He is known as the Father of the Nation and led the Pakistan Movement.',
            'capital of pakistan': 'Islamabad is the capital of Pakistan. It was built in the 1960s to replace Karachi as the capital.',
            'national language of pakistan': 'Urdu is the national language of Pakistan. English is also widely used in official contexts.',
            'currency of pakistan': 'Pakistani Rupee (PKR) is the currency of Pakistan.',
            'population of pakistan': 'Pakistan has a population of over 240 million people, making it the 5th most populous country.',
            
            # Technology facts
            'what is ai': 'Artificial Intelligence (AI) is the simulation of human intelligence in machines. It includes machine learning, neural networks, and natural language processing.',
            'what is machine learning': 'Machine Learning is a subset of AI where computers learn from data without explicit programming. It uses algorithms to find patterns and make predictions.',
            'what is python': 'Python is a high-level programming language known for its simplicity and readability. It is widely used in web development, data science, and AI.',
            
            # General knowledge
            'time now': lambda: f"The current time is {self._get_current_time()}",
            'weather today': lambda: "I can help you check the weather. Would you like me to open a weather website?",
            'latest news': lambda: "I can help you get the latest news. Would you like me to open a news website?",
        }
    
    def _get_current_time(self):
        """Get current time"""
        import datetime
        return datetime.datetime.now().strftime("%I:%M %p on %A, %B %d, %Y")
    
    def parse_intent_ultra_fast(self, text: str) -> Intent:
        """
        Ultra-fast intent parsing with instant recognition
        """
        text = text.lower().strip()
        
        # Check for instant knowledge first (fastest path)
        for key, value in self.knowledge_base.items():
            if key in text:
                return Intent(
                    type=IntentType.INFORMATION,
                    action=key,
                    entities={'topic': key},
                    confidence=1.0,
                    original_text=text,
                    urgency=1,
                    complexity='simple'
                )
        
        # Check for emergency commands (highest priority)
        for intent_type, patterns in self.instant_patterns.items():
            if intent_type == IntentType.EMERGENCY:
                for pattern in patterns:
                    if re.search(pattern, text):
                        return Intent(
                            type=intent_type,
                            action=pattern,
                            entities={},
                            confidence=0.95,
                            original_text=text,
                            urgency=10,
                            complexity='simple'
                        )
        
        # Check other intents
        for intent_type, patterns in self.instant_patterns.items():
            for pattern in patterns:
                match = re.match(pattern, text, re.IGNORECASE)
                if match:
                    entities = self._extract_entities_ultra_fast(text, match)
                    confidence = self._calculate_ultra_confidence(text, pattern, match)
                    urgency = self._calculate_urgency(text, intent_type)
                    complexity = self._calculate_complexity(text)
                    
                    return Intent(
                        type=intent_type,
                        action=match.group(1) if match.groups() else text,
                        entities=entities,
                        confidence=confidence,
                        original_text=text,
                        urgency=urgency,
                        complexity=complexity
                    )
        
        # Default to conversation with high confidence
        return Intent(
            type=IntentType.CONVERSATION,
            action=text,
            entities={},
            confidence=0.8,
            original_text=text,
            urgency=3,
            complexity='medium'
        )
    
    def _extract_entities_ultra_fast(self, text: str, match: re.Match) -> Dict[str, str]:
        """Ultra-fast entity extraction"""
        entities = {}
        
        # Extract entities using predefined patterns
        for entity_type, keywords in self.entity_patterns.items():
            for keyword in keywords:
                if keyword in text:
                    entities[entity_type] = keyword
        
        # Extract numbers and quantities
        numbers = re.findall(r'\d+', text)
        if numbers:
            entities['numbers'] = numbers
        
        # Extract quoted text (for specific searches)
        quoted = re.findall(r'"([^"]+)"', text)
        if quoted:
            entities['quoted_text'] = quoted[0]
        
        # Extract time references
        for time_ref in self.entity_patterns['time_references']:
            if time_ref in text:
                entities['time_reference'] = time_ref
        
        return entities
    
    def _calculate_ultra_confidence(self, text: str, pattern: str, match: re.Match) -> float:
        """Calculate ultra-fast confidence score"""
        base_confidence = 0.85
        
        # Perfect match bonus
        if match.group(0) == text:
            base_confidence += 0.15
        
        # Keyword density bonus
        keyword_count = sum(1 for keyword_list in self.entity_patterns.values() for keyword in keyword_list if keyword in text)
        base_confidence += min(keyword_count * 0.02, 0.1)
        
        # Length penalty (shorter = higher confidence)
        length_penalty = max(0, (len(text) - 10) * 0.01)
        base_confidence -= length_penalty
        
        return min(base_confidence, 1.0)
    
    def _calculate_urgency(self, text: str, intent_type: IntentType) -> int:
        """Calculate urgency based on keywords"""
        urgency = 3  # default
        
        # High urgency keywords
        high_urgency = ['urgent', 'asap', 'immediate', 'emergency', 'help', 'now', 'quick']
        if any(word in text for word in high_urgency):
            urgency = 8
        
        # Medium urgency
        medium_urgency = ['please', 'could you', 'would you', 'today']
        if any(word in text for word in medium_urgency):
            urgency = 5
        
        # Intent-specific urgency
        if intent_type == IntentType.EMERGENCY:
            urgency = 10
        elif intent_type == IntentType.QUESTION:
            urgency = 4
        
        return urgency
    
    def _calculate_complexity(self, text: str) -> str:
        """Calculate complexity of the request"""
        if len(text) < 20:
            return 'simple'
        elif len(text) < 50:
            return 'medium'
        else:
            return 'complex'
    
    def generate_ultra_fast_response(self, intent: Intent) -> UltraFastResponse:
        """Generate ultra-fast response with perfect understanding"""
        
        start_time = time.time()
        
        # Check for instant knowledge first (fastest response)
        for key, value in self.knowledge_base.items():
            if key in intent.original_text:
                response_time = (time.time() - start_time) * 1000
                
                if callable(value):
                    response_text = value()
                else:
                    response_text = value
                
                return UltraFastResponse(
                    intent=intent,
                    response=response_text,
                    actions=[],
                    follow_up=None,
                    response_time=response_time,
                    confidence=1.0,
                    priority='critical'
                )
        
        # Generate structured response based on intent
        if intent.type == IntentType.COMMAND:
            return self._handle_ultra_command(intent)
        elif intent.type == IntentType.QUESTION:
            return self._handle_ultra_question(intent)
        elif intent.type == IntentType.SEARCH:
            return self._handle_ultra_search(intent)
        elif intent.type == IntentType.AUTOMATION:
            return self._handle_ultra_automation(intent)
        elif intent.type == IntentType.INFORMATION:
            return self._handle_ultra_information(intent)
        else:
            return self._handle_ultra_conversation(intent)
    
    def _handle_ultra_command(self, intent: Intent) -> UltraFastResponse:
        """Handle commands with ultra-fast execution"""
        action = intent.action
        entities = intent.entities
        
        # Multi-step command handling
        if 'open' in action and 'youtube' in action:
            if 'song' in action or 'music' in action or 'play' in action:
                return UltraFastResponse(
                    intent=intent,
                    response="Opening YouTube and searching for music...",
                    actions=[
                        {"type": "open_website", "url": "https://www.youtube.com"},
                        {"type": "wait", "seconds": 1},
                        {"type": "search_youtube", "query": entities.get('quoted_text', 'popular music')}
                    ],
                    follow_up="What song or artist would you like?",
                    response_time=50,
                    confidence=0.95,
                    priority='high'
                )
            else:
                return UltraFastResponse(
                    intent=intent,
                    response="Opening YouTube...",
                    actions=[{"type": "open_website", "url": "https://www.youtube.com"}],
                    follow_up=None,
                    response_time=30,
                    confidence=0.9,
                    priority='high'
                )
        
        # Application opening
        if 'application' in entities:
            app = entities['application']
            return UltraFastResponse(
                intent=intent,
                response=f"Opening {app.title()}...",
                actions=[{"type": "open_app", "app": app}],
                follow_up=None,
                response_time=25,
                confidence=0.9,
                priority='high'
            )
        
        # Generic command
        return UltraFastResponse(
            intent=intent,
            response=f"Executing: {action}",
            actions=[{"type": "execute_command", "command": action}],
            follow_up=None,
            response_time=40,
            confidence=0.8,
            priority='medium'
        )
    
    def _handle_ultra_question(self, intent: Intent) -> UltraFastResponse:
        """Handle questions with perfect understanding"""
        question = intent.action
        
        # Check knowledge base first
        for key, value in self.knowledge_base.items():
            if key in question:
                if callable(value):
                    response_text = value()
                else:
                    response_text = value
                
                return UltraFastResponse(
                    intent=intent,
                    response=response_text,
                    actions=[],
                    follow_up="Would you like more details?",
                    response_time=20,
                    confidence=1.0,
                    priority='critical'
                )
        
        # Complex question handling
        return UltraFastResponse(
            intent=intent,
            response=f"I understand you're asking about: {question}. Let me help you with that.",
            actions=[{"type": "ai_query", "query": question}],
            follow_up="What specific aspect interests you most?",
            response_time=100,
            confidence=0.85,
            priority='medium'
        )
    
    def _handle_ultra_search(self, intent: Intent) -> UltraFastResponse:
        """Handle search with ultra-fast execution"""
        query = intent.action
        entities = intent.entities
        
        # YouTube search
        if 'youtube' in query.lower():
            search_term = entities.get('quoted_text', query)
            return UltraFastResponse(
                intent=intent,
                response=f"Searching YouTube for: {search_term}",
                actions=[
                    {"type": "open_website", "url": "https://www.youtube.com"},
                    {"type": "wait", "seconds": 1},
                    {"type": "search_youtube", "query": search_term}
                ],
                follow_up=None,
                response_time=60,
                confidence=0.95,
                priority='high'
            )
        
        # Google search
        return UltraFastResponse(
            intent=intent,
            response=f"Searching Google for: {query}",
            actions=[
                {"type": "google_search", "query": query},
                {"type": "auto_click_result"}
            ],
            follow_up=None,
            response_time=80,
            confidence=0.9,
            priority='high'
        )
    
    def _handle_ultra_automation(self, intent: Intent) -> UltraFastResponse:
        """Handle automation with ultra-fast response"""
        automation_name = intent.action
        
        return UltraFastResponse(
            intent=intent,
            response=f"Starting {automation_name} automation...",
            actions=[{"type": "run_automation", "name": automation_name}],
            follow_up="Automation completed successfully!",
            response_time=30,
            confidence=0.95,
            priority='high'
        )
    
    def _handle_ultra_information(self, intent: Intent) -> UltraFastResponse:
        """Handle information requests"""
        topic = intent.action
        
        return UltraFastResponse(
            intent=intent,
            response=f"Getting information about: {topic}",
            actions=[{"type": "ai_query", "query": topic}],
            follow_up="What would you like to know specifically?",
            response_time=120,
            confidence=0.8,
            priority='medium'
        )
    
    def _handle_ultra_conversation(self, intent: Intent) -> UltraFastResponse:
        """Handle conversation with ultra-fast response"""
        message = intent.action
        
        return UltraFastResponse(
            intent=intent,
            response=f"I understand: {message}",
            actions=[{"type": "ai_conversation", "message": message}],
            follow_up="How can I help you further?",
            response_time=150,
            confidence=0.8,
            priority='medium'
        )

# Global ultra-fast NLU instance
ultra_fast_nlu = UltraFastNLU()
