from datetime import datetime, timedelta
from typing import Dict, Optional
import logging
import os

class SecurityManager:
    def __init__(self):
        self.request_logs: Dict[str, list] = {}
        self.setup_logging()
        
    def setup_logging(self):
        """Setup security logging"""
        logging.basicConfig(
            filename='security.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def check_rate_limit(self, session_id: str, max_requests: int = 10, window_minutes: int = 60) -> bool:
        """Check if request is within rate limits"""
        now = datetime.now()
        window_start = now - timedelta(minutes=window_minutes)
        
        # Clean old requests
        if session_id in self.request_logs:
            self.request_logs[session_id] = [
                timestamp for timestamp in self.request_logs[session_id]
                if timestamp > window_start
            ]
        else:
            self.request_logs[session_id] = []
            
        # Check rate limit
        if len(self.request_logs[session_id]) >= max_requests:
            logging.warning(f"Rate limit exceeded for session {session_id}")
            return False
            
        # Add new request
        self.request_logs[session_id].append(now)
        return True
        
    def log_security_event(self, event_type: str, details: str, session_id: Optional[str] = None):
        """Log security-related events"""
        logging.info(f"Security Event - Type: {event_type}, Session: {session_id}, Details: {details}") 