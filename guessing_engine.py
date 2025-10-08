#!/usr/bin/env python3
"""
Guessing Engine for AutoMind
Matches user features against car database and returns best matches
"""

import csv
from typing import Dict, List, Optional, Tuple


class GuessingEngine:
    """Engine to score and rank cars based on extracted features."""
    
    def __init__(self, data_file: str = "data/car_data.csv"):
        self.cars = []
        self.data_file = data_file
        self.load_cars()
    
    def load_cars(self):
        """Load car data from CSV file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.cars = list(reader)
            print(f"[Guessing Engine] Loaded {len(self.cars)} cars from database")
        except FileNotFoundError:
            print(f"[Guessing Engine] Error: Could not find {self.data_file}")
            self.cars = []
    
    def score_car(self, car: Dict[str, str], features: Dict[str, Optional[str]]) -> int:
        """
        Score a car based on how well it matches the extracted features.
        
        Args:
            car: Car data dictionary from dataset
            features: Extracted features from user input
            
        Returns:
            Score (higher is better match)
        """
        score = 0
        
        # Brand matching (highest priority - 30 points)
        if features.get('brand') and car.get('brand'):
            if features['brand'].lower() in car['brand'].lower() or \
               car['brand'].lower() in features['brand'].lower():
                score += 30
        
        # Body type matching (20 points)
        if features.get('type') and car.get('body_type'):
            if features['type'].lower() == car['body_type'].lower():
                score += 20
        
        # Fuel type matching (20 points)
        if features.get('fuel') and car.get('fuel_type'):
            if features['fuel'].lower() == car['fuel_type'].lower():
                score += 20
        
        # Price range matching (15 points)
        if features.get('price_range') and car.get('price_range'):
            if self._price_match(features['price_range'], car['price_range']):
                score += 15
        
        # Luxury status matching (15 points)
        if features.get('luxury') is not None and car.get('luxury'):
            car_luxury = car['luxury'].lower() == 'yes'
            if features['luxury'] == car_luxury:
                score += 15
        
        return score
    
    def _price_match(self, feature_price: str, car_price: str) -> bool:
        """Check if price ranges match."""
        # Normalize price formats
        feature_price = feature_price.lower().replace('_', '-')
        car_price = car_price.lower().replace('_', '-')
        
        # Direct match
        if feature_price in car_price or car_price in feature_price:
            return True
        
        # Handle "under" patterns
        if 'under' in feature_price:
            if 'under' in car_price:
                return True
            # "under_20L" should match "10-20L"
            if '10-20' in feature_price and '10-20' in car_price:
                return True
        
        return False
    
    def find_matches(self, features: Dict[str, Optional[str]], top_n: int = 5) -> List[Tuple[Dict, int]]:
        """
        Find top matching cars based on features.
        
        Args:
            features: Extracted features from user input
            top_n: Number of top matches to return
            
        Returns:
            List of (car, score) tuples, sorted by score descending
        """
        # Score all cars
        scored_cars = []
        for car in self.cars:
            score = self.score_car(car, features)
            if score > 0:  # Only include cars with some match
                scored_cars.append((car, score))
        
        # Sort by score (descending)
        scored_cars.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N
        return scored_cars[:top_n]
    
    def get_best_guess(self, features: Dict[str, Optional[str]]) -> Optional[Dict[str, str]]:
        """Get single best matching car."""
        matches = self.find_matches(features, top_n=1)
        if matches:
            return matches[0][0]
        return None
    
    def suggest_followup_question(self, features: Dict[str, Optional[str]]) -> str:
        """
        Suggest a follow-up question based on missing features.
        
        Args:
            features: Current extracted features
            
        Returns:
            Follow-up question string
        """
        # Check what's missing
        if not features.get('brand'):
            return "Which brand are you thinking of? (e.g., Toyota, Hyundai, Maruti)"
        
        if not features.get('type'):
            return "What type of car? (SUV, Sedan, or Hatchback)"
        
        if not features.get('fuel'):
            return "What fuel type? (Petrol, Diesel, or Electric)"
        
        if not features.get('price_range'):
            return "What's your budget range? (e.g., under 10 lakhs, 20-30 lakhs)"
        
        if features.get('luxury') is None:
            return "Are you looking for a luxury car or something more affordable?"
        
        return "Can you provide more details about the car?"
    
    def format_car_info(self, car: Dict[str, str]) -> str:
        """Format car information for display."""
        brand = car.get('brand', 'Unknown')
        model = car.get('model', 'Unknown')
        body_type = car.get('body_type', '')
        fuel = car.get('fuel_type', '')
        price = car.get('price_range', '').replace('_', ' ').replace('-', ' to ')
        
        info = f"{brand} {model}"
        details = []
        
        if body_type:
            details.append(body_type)
        if fuel:
            details.append(fuel)
        if price:
            details.append(f"Price: {price}")
        
        if details:
            info += f" ({', '.join(details)})"
        
        return info


def test_guessing_engine():
    """Test the guessing engine."""
    print("=" * 70)
    print("GUESSING ENGINE TEST")
    print("=" * 70)
    
    engine = GuessingEngine()
    
    # Test cases
    test_features = [
        {
            'brand': 'Toyota',
            'type': 'suv',
            'fuel': None,
            'price_range': 'under_20L',
            'luxury': None
        },
        {
            'brand': 'Maruti Suzuki',
            'type': 'hatchback',
            'fuel': 'petrol',
            'price_range': 'under_10L',
            'luxury': False
        },
        {
            'brand': None,
            'type': 'sedan',
            'fuel': 'electric',
            'price_range': None,
            'luxury': True
        }
    ]
    
    for i, features in enumerate(test_features, 1):
        print(f"\nTest {i}: Features = {features}")
        matches = engine.find_matches(features, top_n=3)
        
        print(f"Top {len(matches)} matches:")
        for car, score in matches:
            print(f"  Score {score}: {engine.format_car_info(car)}")
        
        if not matches:
            question = engine.suggest_followup_question(features)
            print(f"  No strong matches. Follow-up: {question}")
        
        print("-" * 70)


if __name__ == "__main__":
    test_guessing_engine()
