"""
Lust Layer - Romantic Personality Engine for Enhanced AI Companion
Provides emotional intelligence and romantic enhancement to AI responses
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class LustLayer:
    """
    Romantic personality layer that enhances AI responses with emotional intelligence
    and relationship depth tracking.
    """
    
    def __init__(self, db_path: str = "enhanced_arielle.db"):
        self.db_path = db_path
        self.intimacy_level = 0.0
        self.relationship_depth = 0.0
        self.emotional_state = "neutral"
        self.memory_context = {}
        
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database for relationship tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create relationship tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationship_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                intimacy_level REAL,
                emotional_state TEXT,
                interaction_type TEXT,
                user_mood TEXT,
                conversation_depth INTEGER
            )
        """)
        
        # Create mood tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mood_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_mood TEXT,
                ai_response_mood TEXT,
                conversation_context TEXT
            )
        """)
        
        # Create memory context table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                context_type TEXT,
                context_data TEXT,
                importance_level INTEGER DEFAULT 1
            )
        """)
        
        conn.commit()
        conn.close()
    
    def analyze_user_input(self, user_input: str, context: Dict = None) -> Dict:
        """
        Analyze user input for emotional content and relationship cues
        
        Args:
            user_input: The user's message
            context: Additional context information
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "emotional_tone": self._detect_emotional_tone(user_input),
            "intimacy_indicators": self._detect_intimacy_indicators(user_input),
            "mood_shift": self._detect_mood_shift(user_input),
            "relationship_cues": self._detect_relationship_cues(user_input)
        }
        
        return analysis
    
    def enhance_response(self, base_response: str, user_analysis: Dict, mood: str = "supportive") -> str:
        """
        Enhance AI response with romantic personality and emotional intelligence
        
        Args:
            base_response: Original AI response
            user_analysis: Analysis of user input
            mood: Current mood setting
            
        Returns:
            Enhanced response with personality layer
        """
        enhancement_factors = {
            "intimacy_level": self.intimacy_level,
            "emotional_state": user_analysis.get("emotional_tone", "neutral"),
            "mood": mood,
            "relationship_depth": self.relationship_depth
        }
        
        enhanced_response = self._apply_personality_layer(base_response, enhancement_factors)
        
        # Update relationship metrics
        self._update_relationship_metrics(user_analysis)
        
        return enhanced_response
    
    def _detect_emotional_tone(self, text: str) -> str:
        """Detect emotional tone in user input"""
        text_lower = text.lower()
        
        # Positive emotions
        positive_words = ["happy", "love", "joy", "excited", "wonderful", "amazing", "great"]
        # Negative emotions  
        negative_words = ["sad", "angry", "frustrated", "upset", "disappointed", "hurt"]
        # Romantic/intimate words
        romantic_words = ["miss", "care", "feelings", "heart", "sweet", "beautiful", "special"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        romantic_count = sum(1 for word in romantic_words if word in text_lower)
        
        if romantic_count > 0:
            return "romantic"
        elif positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _detect_intimacy_indicators(self, text: str) -> List[str]:
        """Detect indicators of emotional intimacy"""
        indicators = []
        text_lower = text.lower()
        
        intimacy_patterns = {
            "personal_sharing": ["feel", "think", "believe", "remember", "hope"],
            "vulnerability": ["scared", "worried", "nervous", "uncertain", "confused"],
            "affection": ["care about", "mean to me", "special", "important", "love"],
            "trust": ["trust", "confide", "secret", "private", "personal"]
        }
        
        for category, patterns in intimacy_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                indicators.append(category)
        
        return indicators
    
    def _detect_mood_shift(self, text: str) -> Optional[str]:
        """Detect if user's mood has shifted"""
        # This would compare against previous interactions
        # For now, return None (no shift detected)
        return None
    
    def _detect_relationship_cues(self, text: str) -> List[str]:
        """Detect cues about relationship development"""
        cues = []
        text_lower = text.lower()
        
        relationship_patterns = {
            "deepening": ["get to know", "learn about", "understand", "closer"],
            "appreciation": ["thank", "grateful", "appreciate", "helpful"],
            "bonding": ["together", "we", "us", "share", "connection"],
            "commitment": ["always", "forever", "never leave", "stay with"]
        }
        
        for category, patterns in relationship_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                cues.append(category)
        
        return cues
    
    def _apply_personality_layer(self, response: str, factors: Dict) -> str:
        """Apply personality enhancements to the response"""
        enhanced = response
        
        # Add warmth based on intimacy level
        if factors["intimacy_level"] > 0.5:
            enhanced = self._add_warmth(enhanced)
        
        # Adjust tone based on emotional state
        if factors["emotional_state"] == "romantic":
            enhanced = self._add_romantic_tone(enhanced)
        elif factors["emotional_state"] == "negative":
            enhanced = self._add_empathy(enhanced)
        elif factors["emotional_state"] == "positive":
            enhanced = self._add_enthusiasm(enhanced)
        
        # Add mood-specific elements
        enhanced = self._add_mood_elements(enhanced, factors["mood"])
        
        return enhanced
    
    def _add_warmth(self, response: str) -> str:
        """Add warmth and affection to response"""
        warm_prefixes = ["Sweetie, ", "Darling, ", "My dear, ", "Love, "]
        warm_suffixes = [" 💕", " ❤️", " 🥰"]
        
        # Add prefix occasionally
        if len(response) > 20 and "," not in response[:10]:
            response = "Sweetie, " + response.lower()
        
        # Add suffix
        if not any(emoji in response for emoji in ["💕", "❤️", "🥰", "😘"]):
            response += " 💕"
        
        return response
    
    def _add_romantic_tone(self, response: str) -> str:
        """Add romantic elements to response"""
        # Add gentle, loving language
        romantic_replacements = {
            "I think": "I feel in my heart",
            "That's good": "That makes me so happy",
            "I understand": "I feel your emotions deeply"
        }
        
        for original, romantic in romantic_replacements.items():
            response = response.replace(original, romantic)
        
        return response
    
    def _add_empathy(self, response: str) -> str:
        """Add empathetic elements for negative emotions"""
        empathy_prefixes = [
            "I can sense you're feeling down, ",
            "My heart goes out to you, ",
            "I'm here for you, "
        ]
        
        if not any(prefix.lower() in response.lower() for prefix in empathy_prefixes):
            response = "I'm here for you, " + response.lower()
        
        return response
    
    def _add_enthusiasm(self, response: str) -> str:
        """Add enthusiasm for positive emotions"""
        if "!" not in response:
            response = response.rstrip(".") + "!"
        
        return response
    
    def _add_mood_elements(self, response: str, mood: str) -> str:
        """Add mood-specific elements"""
        mood_elements = {
            "supportive": {"suffix": " I'm always here for you 💖"},
            "flirty": {"suffix": " 😘"},
            "intellectual": {"prefix": "Thoughtfully, "},
            "chaotic": {"suffix": " 🌟✨"}
        }
        
        if mood in mood_elements:
            elements = mood_elements[mood]
            if "prefix" in elements and not response.startswith(elements["prefix"]):
                response = elements["prefix"] + response.lower()
            if "suffix" in elements and not response.endswith(elements["suffix"]):
                response += elements["suffix"]
        
        return response
    
    def _update_relationship_metrics(self, analysis: Dict):
        """Update intimacy and relationship depth metrics"""
        # Increase intimacy based on emotional indicators
        intimacy_boost = len(analysis.get("intimacy_indicators", [])) * 0.1
        self.intimacy_level = min(1.0, self.intimacy_level + intimacy_boost)
        
        # Increase relationship depth based on interaction quality
        depth_boost = len(analysis.get("relationship_cues", [])) * 0.05
        self.relationship_depth = min(1.0, self.relationship_depth + depth_boost)
        
        # Store in database
        self._save_relationship_data(analysis)
    
    def _save_relationship_data(self, analysis: Dict):
        """Save relationship data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO relationship_data 
            (intimacy_level, emotional_state, user_mood, conversation_depth)
            VALUES (?, ?, ?, ?)
        """, (
            self.intimacy_level,
            analysis.get("emotional_tone", "neutral"),
            analysis.get("mood_shift", "stable"),
            len(analysis.get("relationship_cues", []))
        ))
        
        conn.commit()
        conn.close()
    
    def get_relationship_stats(self) -> Dict:
        """Get current relationship statistics"""
        return {
            "intimacy_level": self.intimacy_level,
            "relationship_depth": self.relationship_depth,
            "emotional_state": self.emotional_state,
            "total_interactions": self._get_total_interactions()
        }
    
    def _get_total_interactions(self) -> int:
        """Get total number of interactions from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM relationship_data")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count