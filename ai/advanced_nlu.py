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

@dataclass
class Intent:
    type: IntentType
    action: str
    entities: Dict[str, str]
    confidence: float
    original_text: str

@dataclass
class StructuredResponse:
    intent: Intent
    response: str
    actions: List[Dict]
    follow_up: Optional[str]

class AdvancedNLU:
    def __init__(self):
        self.intent_patterns = {
            # Command patterns
            IntentType.COMMAND: [
                r'(?:open|launch|start)\s+(.+)',
                r'(?:close|shutdown|exit)\s+(.+)',
                r'(?:play|pause|stop|resume)\s+(.+)',
                r'(?:search|find|look for)\s+(.+)',
                r'(?:show|display)\s+(.+)',
                r'(?:increase|decrease|mute|unmute)\s+(.+)',
            ],
            
            # Question patterns
            IntentType.QUESTION: [
                r'(?:what|who|where|when|why|how)\s+(.+)',
                r'(.+)\s+(?:is|are|was|were)\s+(.+)',
                r'(.+)\s+(?:do|does|did)\s+(.+)',
                r'(.+)\s+(?:can|could|will|would)\s+(.+)',
                r'tell\s+me\s+about\s+(.+)',
                r'explain\s+(.+)',
                r'describe\s+(.+)',
            ],
            
            # Search patterns
            IntentType.SEARCH: [
                r'search\s+(?:for|on)\s+(.+)',
                r'google\s+(.+)',
                r'find\s+(?:information|about)\s+(.+)',
                r'look\s+up\s+(.+)',
            ],
            
            # Automation patterns
            IntentType.AUTOMATION: [
                r'(?:start|run|execute)\s+(?:automation|routine)\s+(.+)',
                r'(?:quick|fast)\s+(.+)',
                r'morning\s+routine',
                r'work\s+mode',
                r'entertainment\s+mode',
                r'trading\s+routine',
            ],
            
            # Information patterns
            IntentType.INFORMATION: [
                r'(?:what|who)\s+is\s+(.+)',
                r'(?:tell|explain)\s+me\s+about\s+(.+)',
                r'(?:describe|define)\s+(.+)',
                r'(?:history|story|background)\s+of\s+(.+)',
            ],
        }
        
        self.entity_extractors = {
            'application': [
                'youtube', 'spotify', 'chrome', 'firefox', 'edge', 'vs code', 
                'notepad', 'discord', 'teams', 'zoom', 'tradingview', 'gmail',
                'word', 'excel', 'powerpoint', 'photoshop', 'vlc'
            ],
            'website': [
                'google', 'youtube', 'facebook', 'twitter', 'instagram', 
                'linkedin', 'github', 'stackoverflow', 'reddit'
            ],
            'media_type': [
                'song', 'music', 'video', 'movie', 'playlist', 'album'
            ],
            'action': [
                'open', 'close', 'play', 'pause', 'stop', 'search', 'find',
                'show', 'hide', 'start', 'stop', 'increase', 'decrease'
            ],
            'quantity': [
                'volume', 'brightness', 'speed'
            ]
        }
    
    def parse_intent(self, text: str) -> Intent:
        """Parse user input to determine intent and extract entities"""
        text = text.lower().strip()
        
        best_intent = None
        best_confidence = 0.0
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.match(pattern, text, re.IGNORECASE)
                if match:
                    confidence = self._calculate_confidence(text, pattern, match)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        entities = self._extract_entities(text, match)
                        best_intent = Intent(
                            type=intent_type,
                            action=match.group(1) if match.groups() else text,
                            entities=entities,
                            confidence=confidence,
                            original_text=text
                        )
        
        # Default to conversation if no intent matched
        if best_intent is None:
            best_intent = Intent(
                type=IntentType.CONVERSATION,
                action=text,
                entities={},
                confidence=0.5,
                original_text=text
            )
        
        return best_intent
    
    def _calculate_confidence(self, text: str, pattern: str, match: re.Match) -> float:
        """Calculate confidence score for intent matching"""
        base_confidence = 0.8
        
        # Boost confidence for exact matches
        if match.group(0) == text:
            base_confidence += 0.2
        
        # Check for keywords
        keyword_boost = 0
        for entity_type, keywords in self.entity_extractors.items():
            for keyword in keywords:
                if keyword in text:
                    keyword_boost += 0.05
        
        return min(base_confidence + keyword_boost, 1.0)
    
    def _extract_entities(self, text: str, match: re.Match) -> Dict[str, str]:
        """Extract entities from the matched text"""
        entities = {}
        
        # Extract application/website names
        for entity_type, keywords in self.entity_extractors.items():
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
        
        return entities
    
    def generate_structured_response(self, intent: Intent) -> StructuredResponse:
        """Generate a structured response based on intent"""
        
        if intent.type == IntentType.COMMAND:
            return self._handle_command_intent(intent)
        elif intent.type == IntentType.QUESTION:
            return self._handle_question_intent(intent)
        elif intent.type == IntentType.SEARCH:
            return self._handle_search_intent(intent)
        elif intent.type == IntentType.AUTOMATION:
            return self._handle_automation_intent(intent)
        elif intent.type == IntentType.INFORMATION:
            return self._handle_information_intent(intent)
        else:
            return self._handle_conversation_intent(intent)
    
    def _handle_command_intent(self, intent: Intent) -> StructuredResponse:
        """Handle command intents like 'open youtube'"""
        action = intent.action
        entities = intent.entities
        
        # Multi-step command handling
        if 'open' in action and 'youtube' in action:
            if 'song' in action or 'music' in action or 'play' in action:
                return StructuredResponse(
                    intent=intent,
                    response="I'll open YouTube and help you play a song. What would you like to listen to?",
                    actions=[
                        {"type": "open_website", "url": "https://www.youtube.com"},
                        {"type": "wait", "seconds": 2},
                        {"type": "search_youtube", "query": entities.get('quoted_text', 'popular music')}
                    ],
                    follow_up="What song or artist would you like to search for?"
                )
            else:
                return StructuredResponse(
                    intent=intent,
                    response="Opening YouTube for you.",
                    actions=[{"type": "open_website", "url": "https://www.youtube.com"}],
                    follow_up=None
                )
        
        # Generic application opening
        if 'application' in entities:
            app = entities['application']
            return StructuredResponse(
                intent=intent,
                response=f"Opening {app.title()} for you.",
                actions=[{"type": "open_app", "app": app}],
                follow_up=None
            )
        
        return StructuredResponse(
            intent=intent,
            response=f"I'll help you {action}.",
            actions=[{"type": "execute_command", "command": action}],
            follow_up=None
        )
    
    def _handle_question_intent(self, intent: Intent) -> StructuredResponse:
        """Handle question intents like 'who is the founder of Pakistan'"""
        question = intent.action
        
        # Check for specific knowledge questions
        if 'founder of pakistan' in question:
            return StructuredResponse(
                intent=intent,
                response="Quaid-e-Azam Muhammad Ali Jinnah is the founder of Pakistan. He is known as the Father of the Nation and led the Pakistan Movement.",
                actions=[],
                follow_up="Would you like to know more about Pakistan's history?"
            )
        
        if 'capital of pakistan' in question:
            return StructuredResponse(
                intent=intent,
                response="Islamabad is the capital of Pakistan. It was built in the 1960s to replace Karachi as the capital.",
                actions=[],
                follow_up="Would you like to know about other major cities in Pakistan?"
            )
        
        # Generic question handling - pass to AI
        return StructuredResponse(
            intent=intent,
            response=None,  # Will be handled by AI
            actions=[{"type": "ai_query", "query": question}],
            follow_up=None
        )
    
    def _handle_search_intent(self, intent: Intent) -> StructuredResponse:
        """Handle search intents"""
        query = intent.action
        
        return StructuredResponse(
            intent=intent,
            response=f"I'll search for {query} on Google.",
            actions=[
                {"type": "google_search", "query": query},
                {"type": "auto_click_result"}
            ],
            follow_up=None
        )
    
    def _handle_automation_intent(self, intent: Intent) -> StructuredResponse:
        """Handle automation intents"""
        automation_name = intent.action
        
        return StructuredResponse(
            intent=intent,
            response=f"Starting {automation_name} automation.",
            actions=[{"type": "run_automation", "name": automation_name}],
            follow_up=None
        )
    
    def _handle_information_intent(self, intent: Intent) -> StructuredResponse:
        """Handle information requests"""
        topic = intent.action
        
        return StructuredResponse(
            intent=intent,
            response=f"Let me get information about {topic} for you.",
            actions=[{"type": "ai_query", "query": f"Tell me about {topic}"}],
            follow_up=None
        )
    
    def _handle_conversation_intent(self, intent: Intent) -> StructuredResponse:
        """Handle general conversation"""
        return StructuredResponse(
            intent=intent,
            response=None,  # Will be handled by AI
            actions=[{"type": "ai_conversation", "message": intent.original_text}],
            follow_up=None
        )

# Global NLU instance
nlu_engine = AdvancedNLU()
