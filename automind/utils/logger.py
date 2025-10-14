"""Session logging utility for tracking user interactions and AI processing."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class SessionLogger:
    """Handles logging of user sessions for both guessing and recommendation modes."""
    
    def __init__(self, mode: str = "guessing"):
        """Initialize logger.
        
        Args:
            mode: Either 'guessing' or 'recommendation'
        """
        self.mode = mode
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.interactions: List[Dict[str, Any]] = []
        self.log_dir = Path("logs") / mode if mode == "recommendation" else Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"{self._get_filename_prefix()}_{self.session_id}.json"
    
    def _get_filename_prefix(self) -> str:
        """Get filename prefix based on mode."""
        return "recommendation" if self.mode == "recommendation" else "session"
    
    def log_question(self, question: str, answer: str, value: Any):
        """Log a question-answer pair (guessing mode).
        
        Args:
            question: The question text
            answer: The answer label
            value: The answer value
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "value": str(value)
        }
        self.interactions.append(entry)
        self._save()
    
    def log_result(self, result: str, guessed_car: str, actual_car: Optional[str] = None):
        """Log the final result (guessing mode).
        
        Args:
            result: 'correct' or 'incorrect'
            guessed_car: The car the AI guessed
            actual_car: The actual car (if incorrect)
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "result": result,
            "guessed_car": guessed_car
        }
        if actual_car:
            entry["actual_car"] = actual_car
        
        self.interactions.append(entry)
        self._save()
    
    def log_preferences(self, preferences: Dict[str, Any]):
        """Log user preferences (recommendation mode).
        
        Args:
            preferences: Dictionary of user preferences
        """
        self.preferences = preferences
        self._save()
    
    def log_recommendations(self, recommendations: List[Dict[str, Any]], ai_info: Dict[str, Any]):
        """Log recommendation results with AI processing info.
        
        Args:
            recommendations: List of recommended cars
            ai_info: Dictionary containing AI processing information
        """
        self.recommendations = {
            'total_matches': len(recommendations),
            'top_10': [
                {
                    'rank': i+1,
                    'model': car['model'],
                    'score': car['score'],
                    'brand': car['brand'],
                    'body_type': car['body_type'],
                    'fuel_type': car['fuel_type']
                }
                for i, car in enumerate(recommendations[:10])
            ]
        }
        self.ai_processing = ai_info
        self._save()
    
    def _save(self):
        """Save current session to file."""
        data = {
            "session_id": self.session_id,
            "mode": self.mode,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.mode == "guessing":
            data["interactions"] = self.interactions
        else:  # recommendation
            if hasattr(self, 'preferences'):
                data["preferences"] = self.preferences
            if hasattr(self, 'recommendations'):
                data["results"] = self.recommendations
            if hasattr(self, 'ai_processing'):
                data["ai_processing"] = self.ai_processing
        
        with open(self.log_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_log_path(self) -> str:
        """Get the path to the log file.
        
        Returns:
            String path to log file
        """
        return str(self.log_file)
    
    def get_interactions(self) -> List[Dict[str, Any]]:
        """Get all interactions.
        
        Returns:
            List of interaction dictionaries
        """
        return self.interactions


__all__ = ['SessionLogger']
