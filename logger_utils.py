"""
Logging utilities for Local AI Companion
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO):
    """Setup logger with file and console handlers"""
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

class ConversationLogger:
    """Specialized logger for conversation tracking"""
    
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.conversation_log = os.path.join(log_dir, "conversations.jsonl")
        
    def log_conversation(self, user_message, assistant_response, mood, model_info):
        """Log a conversation exchange"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "assistant_response": assistant_response,
            "mood": mood,
            "model_info": model_info,
            "session_id": self.get_session_id()
        }
        
        try:
            with open(self.conversation_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            logging.error(f"Failed to log conversation: {e}")
    
    def get_session_id(self):
        """Get or create session ID"""
        # Simple session ID based on date
        return datetime.now().strftime('%Y%m%d')
