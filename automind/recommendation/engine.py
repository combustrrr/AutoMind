"""Recommendation engine for car suggestions based on user preferences."""

from typing import Any, Dict, List
from ..expert_system import CarExpertSystem


class RecommendationEngine:
    """Content-based recommendation engine using expert system."""
    
    # Preference mapping to database attributes
    PREFERENCE_MAPPING = {
        'brand': {
            'Toyota': 'toyota', 'Honda': 'honda', 'Maruti Suzuki': 'maruti suzuki',
            'Hyundai': 'hyundai', 'Mahindra': 'mahindra', 'Tata': 'tata',
            'Mercedes-Benz': 'mercedes-benz', 'BMW': 'bmw', 'Audi': 'audi'
        },
        'body_type': {
            'Hatchback': 'hatchback', 'Sedan': 'sedan', 'SUV': 'suv', 'MUV': 'muv'
        },
        'fuel_type': {
            'Petrol': 'petrol', 'Diesel': 'diesel', 'Electric': 'electric',
            'CNG': 'cng', 'Hybrid': 'hybrid'
        },
        'era': {
            'Current (2020+)': 'current',
            'Recent (2015-2019)': 'recent',
            'Older (2010-2014)': 'older',
            'Classic (Pre-2010)': 'classic'
        },
        'budget': {
            'Under 5 Lakhs': 'below_5l', '5-10 Lakhs': '5-10l',
            '10-20 Lakhs': '10-20l', '20-30 Lakhs': '20-30l',
            'Above 30 Lakhs': 'above_30l'
        },
        'luxury': {
            'Yes, luxury/premium': True, 'No, practical': False
        }
    }
    
    def __init__(self, strategy: str = "entropy"):
        """Initialize recommendation engine.
        
        Args:
            strategy: AI strategy to use ('entropy' or 'gini')
        """
        self.strategy = strategy
        self.expert_system = None
    
    def get_recommendations(self, preferences: Dict[str, str]) -> List[Dict[str, Any]]:
        """Get car recommendations based on user preferences.
        
        This method demonstrates Content-Based Filtering AI:
        1. Parse user preferences
        2. Map preferences to database attributes
        3. Apply preferences as high-confidence evidence to expert system
        4. Update belief state probabilities for all 1,050 cars
        5. Rank cars by match score
        6. Return top matches
        
        Args:
            preferences: Dictionary of user preferences
            
        Returns:
            List of recommended cars with scores and details
        """
        # Initialize expert system for this recommendation
        self.expert_system = CarExpertSystem(strategy=self.strategy)
        
        # Apply preferences as evidence
        self._apply_preferences(preferences)
        
        # Get top recommendations
        recommendations = self.expert_system.hypotheses(10)
        
        # Enrich with details
        enriched = self._enrich_recommendations(recommendations)
        
        return enriched
    
    def _apply_preferences(self, preferences: Dict[str, str]):
        """Apply user preferences as evidence to expert system.
        
        Args:
            preferences: User preference dictionary
        """
        for pref_key, pref_value in preferences.items():
            if pref_value == "Any":
                continue
            
            if pref_key not in self.PREFERENCE_MAPPING:
                continue
            
            if pref_value not in self.PREFERENCE_MAPPING[pref_key]:
                continue
            
            mapped_value = self.PREFERENCE_MAPPING[pref_key][pref_value]
            
            # Find the corresponding question and submit answer
            self._submit_preference(pref_key, mapped_value)
    
    def _submit_preference(self, attribute: str, value: Any):
        """Submit a preference as an answer to the expert system.
        
        Args:
            attribute: Attribute name (may need mapping)
            value: Attribute value
        """
        # Map 'budget' to 'price_range' for expert system
        if attribute == 'budget':
            attribute = 'price_range'
        
        # Find the question for this attribute
        for question in self.expert_system.engine.question_bank:
            if question.attribute == attribute:
                try:
                    self.expert_system.submit_answer(question.id, value, confidence=1.0)
                except Exception:
                    pass  # Skip if submission fails
                break
    
    def _enrich_recommendations(self, recommendations: List[tuple]) -> List[Dict[str, Any]]:
        """Enrich recommendations with car details.
        
        Args:
            recommendations: List of (model, probability) tuples
            
        Returns:
            List of enriched car dictionaries
        """
        enriched = []
        
        for model, prob in recommendations:
            if prob <= 0.01:  # Only show if >1% probability
                continue
            
            details = self.expert_system.describe_model(model)
            
            enriched.append({
                'model': model,
                'score': prob,
                'brand': details.get('brand', 'N/A'),
                'body_type': details.get('body_type', 'N/A'),
                'fuel_type': details.get('fuel_type', 'N/A'),
                'price_range': details.get('price_range', 'N/A'),
                'luxury': details.get('luxury', False),
                'engine_cc': details.get('engine_cc', 'N/A'),
                'usage_profile': details.get('usage_profile', 'N/A')
            })
        
        return enriched
    
    def get_ai_processing_info(self) -> Dict[str, Any]:
        """Get information about AI processing for logging.
        
        Returns:
            Dictionary containing AI algorithm and steps
        """
        return {
            'algorithm': 'Content-based filtering with multi-criteria matching',
            'strategy': self.strategy,
            'steps': [
                '1. Parse user preferences',
                '2. Map preferences to database attributes',
                '3. Apply preferences as high-confidence evidence',
                '4. Update belief state probabilities for all 1,050 cars',
                '5. Rank cars by match score',
                '6. Return top 10 matches'
            ],
            'ai_concepts_used': [
                'Expert System reasoning',
                'Content-based recommendation',
                'Multi-criteria decision making',
                'Probability-based ranking',
                'Attribute matching',
                f'{self.strategy.title()} strategy for optimization'
            ]
        }


__all__ = ['RecommendationEngine']
