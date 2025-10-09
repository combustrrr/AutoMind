#!/usr/bin/env python3
"""
ML-Powered Guessing Engine for AutoMind
Uses trained ML model for car predictions with confidence scores
"""

import csv
import pickle
import os
from typing import Dict, List, Optional, Tuple


class MLGuessingEngine:
    """ML-powered engine to predict cars from user queries."""
    
    def __init__(self, 
                 data_file: str = "data/car_data.csv",
                 model_file: str = "data/ml_model.pkl",
                 vectorizer_file: str = "data/vectorizer.pkl"):
        self.data_file = data_file
        self.model_file = model_file
        self.vectorizer_file = vectorizer_file
        
        self.cars = []
        self.car_map = {}  # Map car labels to car data
        self.model = None
        self.vectorizer = None
        self.ml_available = False
        
        self.load_cars()
        self.load_ml_model()
    
    def load_cars(self):
        """Load car data from CSV."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.cars = list(reader)
            
            # Create car map: label -> car data
            for car in self.cars:
                label = f"{car['brand']}_{car['model']}".replace(' ', '_').lower()
                self.car_map[label] = car
            
            print(f"[ML Engine] Loaded {len(self.cars)} cars from database")
        except FileNotFoundError:
            print(f"[ML Engine] Error: Could not find {self.data_file}")
            self.cars = []
    
    def load_ml_model(self):
        """Load trained ML model and vectorizer."""
        try:
            if os.path.exists(self.model_file) and os.path.exists(self.vectorizer_file):
                with open(self.model_file, 'rb') as f:
                    self.model = pickle.load(f)
                
                with open(self.vectorizer_file, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                
                self.ml_available = True
                print(f"[ML Engine] ML model loaded successfully")
                print(f"[ML Engine] Model can predict {len(self.model.classes_)} cars")
            else:
                print(f"[ML Engine] ML model files not found. Run 'python train_ml_model.py' first.")
                print(f"[ML Engine] Falling back to rule-based predictions")
                self.ml_available = False
        except Exception as e:
            print(f"[ML Engine] Error loading ML model: {e}")
            print(f"[ML Engine] Falling back to rule-based predictions")
            self.ml_available = False
    
    def predict_cars(self, query: str, top_n: int = 5) -> List[Tuple[Dict, float]]:
        """
        Predict cars using ML model.
        
        Args:
            query: User's natural language query
            top_n: Number of top predictions to return
            
        Returns:
            List of (car_data, confidence) tuples, sorted by confidence
        """
        if not self.ml_available:
            print("[ML Engine] ML not available, use rule-based guessing_engine.py")
            return []
        
        try:
            # Transform query to TF-IDF features
            query_vec = self.vectorizer.transform([query])
            
            # Get probability predictions for all classes
            probabilities = self.model.predict_proba(query_vec)[0]
            
            # Get top N predictions
            top_indices = probabilities.argsort()[-top_n:][::-1]
            
            results = []
            for idx in top_indices:
                car_label = self.model.classes_[idx]
                confidence = probabilities[idx]
                
                # Get car data from map
                if car_label in self.car_map:
                    car_data = self.car_map[car_label]
                    results.append((car_data, confidence))
            
            return results
        except Exception as e:
            print(f"[ML Engine] Prediction error: {e}")
            return []
    
    def format_prediction(self, car: Dict, confidence: float) -> str:
        """Format a single prediction for display."""
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
            details.append(f"₹{price}")
        
        if details:
            info += f" ({', '.join(details)})"
        
        return f"{info} - {confidence*100:.1f}% confidence"
    
    def display_predictions(self, query: str, predictions: List[Tuple[Dict, float]]):
        """Display predictions in a formatted way."""
        print(f"\n🔍 Query: '{query}'")
        print("=" * 70)
        
        if not predictions:
            print("No predictions available. Please train ML model first.")
            return
        
        print("\n🎯 ML Predictions:")
        print("-" * 70)
        
        for i, (car, confidence) in enumerate(predictions, 1):
            print(f"{i}. {self.format_prediction(car, confidence)}")
        
        # Show confidence distribution
        if predictions:
            top_confidence = predictions[0][1] * 100
            if top_confidence >= 70:
                confidence_msg = "🟢 High confidence"
            elif top_confidence >= 40:
                confidence_msg = "🟡 Medium confidence"
            else:
                confidence_msg = "🔴 Low confidence"
            
            print(f"\n{confidence_msg} (Top prediction: {top_confidence:.1f}%)")
        
        print("=" * 70)


def test_ml_engine():
    """Test ML guessing engine with sample queries."""
    print("=" * 70)
    print("  ML GUESSING ENGINE TEST")
    print("=" * 70)
    print()
    
    engine = MLGuessingEngine()
    
    if not engine.ml_available:
        print("❌ ML model not available. Please run:")
        print("   1. python generate_training_data.py")
        print("   2. python train_ml_model.py")
        return
    
    # Test queries
    test_queries = [
        "Toyota SUV under 20 lakhs",
        "electric car",
        "luxury sedan",
        "affordable hatchback under 10L",
        "sporty BMW",
        "family car from Maruti",
        "premium electric vehicle",
        "budget friendly Hyundai sedan",
    ]
    
    for query in test_queries:
        predictions = engine.predict_cars(query, top_n=3)
        engine.display_predictions(query, predictions)
        print()


if __name__ == "__main__":
    test_ml_engine()
