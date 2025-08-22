"""
Memory management utilities for Local AI Companion
Handles long-term memory, user preferences, and conversation patterns
"""

import json
import os
from datetime import datetime
import logging

class MemoryManager:
    def __init__(self, memory_file):
        self.memory_file = memory_file
        self.logger = logging.getLogger(__name__)
        self.memory = self.load_memory()
    
    def load_memory(self):
        """Load memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading memory: {e}")
        
        return self.create_empty_memory()
    
    def create_empty_memory(self):
        """Create empty memory structure"""
        return {
            "user_preferences": {
                "preferred_name": "",
                "favorite_topics": [],
                "communication_style": "",
                "emotional_needs": []
            },
            "conversation_patterns": {
                "frequent_topics": {},
                "typical_mood": "",
                "conversation_times": [],
                "response_preferences": {}
            },
            "important_topics": [],
            "emotional_state_history": [],
            "personal_details": {
                "interests": [],
                "goals": [],
                "concerns": [],
                "relationships": {}
            },
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def save_memory(self):
        """Save memory to file"""
        try:
            self.memory["last_updated"] = datetime.now().isoformat()
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
            self.logger.info("Memory saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving memory: {e}")
    
    def add_emotional_state(self, mood, context=""):
        """Add emotional state to history"""
        emotional_entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": mood,
            "context": context
        }
        
        self.memory["emotional_state_history"].append(emotional_entry)
        
        # Keep only last 100 emotional states
        if len(self.memory["emotional_state_history"]) > 100:
            self.memory["emotional_state_history"] = self.memory["emotional_state_history"][-100:]
        
        self.save_memory()
    
    def add_important_topic(self, topic, importance_level=1):
        """Add important topic to memory"""
        topic_entry = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "importance_level": importance_level,
            "mentions": 1
        }
        
        # Check if topic already exists
        for existing_topic in self.memory["important_topics"]:
            if existing_topic["topic"].lower() == topic.lower():
                existing_topic["mentions"] += 1
                existing_topic["last_mentioned"] = datetime.now().isoformat()
                self.save_memory()
                return
        
        self.memory["important_topics"].append(topic_entry)
        self.save_memory()
    
    def update_conversation_pattern(self, topic, mood):
        """Update conversation patterns"""
        patterns = self.memory["conversation_patterns"]
        
        # Update frequent topics
        if topic in patterns["frequent_topics"]:
            patterns["frequent_topics"][topic] += 1
        else:
            patterns["frequent_topics"][topic] = 1
        
        # Update typical mood
        patterns["typical_mood"] = mood
        
        # Add conversation time
        patterns["conversation_times"].append(datetime.now().isoformat())
        
        # Keep only last 50 conversation times
        if len(patterns["conversation_times"]) > 50:
            patterns["conversation_times"] = patterns["conversation_times"][-50:]
        
        self.save_memory()
    
    def get_memory_summary(self):
        """Get a summary of memory contents"""
        return {
            "total_conversations": len(self.memory["conversation_patterns"]["conversation_times"]),
            "important_topics_count": len(self.memory["important_topics"]),
            "emotional_states_tracked": len(self.memory["emotional_state_history"]),
            "most_frequent_topics": sorted(
                self.memory["conversation_patterns"]["frequent_topics"].items(),
                key=lambda x: x[1], reverse=True
            )[:5],
            "recent_moods": [
                state["mood"] for state in self.memory["emotional_state_history"][-10:]
            ]
        }
