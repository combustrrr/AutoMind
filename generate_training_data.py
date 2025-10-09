#!/usr/bin/env python3
"""
Training Data Generator for AutoMind ML
Generates synthetic training data from car database for ML model training
"""

import csv
import json
import random
from typing import List, Dict, Tuple


class TrainingDataGenerator:
    """Generate training data from car database."""
    
    def __init__(self, data_file: str = "data/car_data.csv"):
        self.data_file = data_file
        self.cars = []
        self.load_cars()
        
        # Templates for generating natural language descriptions
        self.templates = {
            'brand_focused': [
                "{brand} car",
                "{brand} vehicle",
                "I want a {brand}",
                "Looking for {brand}",
                "Show me {brand} options",
            ],
            'type_focused': [
                "{type}",
                "{type} car",
                "I need a {type}",
                "Looking for a {type}",
                "{type} vehicle",
            ],
            'fuel_focused': [
                "{fuel} car",
                "{fuel} vehicle",
                "I want {fuel}",
                "{fuel} powered car",
            ],
            'price_focused': [
                "car {price}",
                "vehicle {price}",
                "{price} car",
                "budget {price}",
            ],
            'combined': [
                "{brand} {type}",
                "{brand} {type} {fuel}",
                "{type} {fuel}",
                "{brand} {fuel}",
                "{luxury} {brand} {type}",
                "{luxury} {type} {fuel}",
                "{brand} {type} {price}",
                "{type} {fuel} {price}",
                "{luxury} {brand} {type} {price}",
                "{brand} {type} {fuel} {price}",
            ],
            'natural': [
                "reliable {brand} {type} with good {fuel} efficiency",
                "affordable {type} from {brand}",
                "I want a {luxury} {brand} {type}",
                "looking for {luxury} {type} {price}",
                "{brand} {type} that's {luxury} and {fuel}",
                "family {type} from {brand}",
                "sporty {brand} {type}",
                "comfortable {type} {price}",
                "{fuel} {type} with good features",
                "{brand} car {price} range",
            ]
        }
        
        # Synonyms for variety
        self.synonyms = {
            'suv': ['SUV', 'crossover', 'sport utility', '4x4'],
            'sedan': ['sedan', 'saloon', 'four-door'],
            'hatchback': ['hatchback', 'hatch', 'compact car'],
            'petrol': ['petrol', 'gasoline', 'gas'],
            'diesel': ['diesel'],
            'electric': ['electric', 'EV', 'battery', 'zero-emission'],
            'luxury': ['luxury', 'premium', 'high-end', 'expensive'],
            'budget': ['affordable', 'cheap', 'budget', 'economical'],
        }
    
    def load_cars(self):
        """Load car data from CSV."""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.cars = list(reader)
        print(f"[Data Generator] Loaded {len(self.cars)} cars")
    
    def get_luxury_label(self, car: Dict) -> str:
        """Determine luxury label for a car."""
        if car['luxury'].lower() == 'yes':
            return random.choice(self.synonyms['luxury'])
        else:
            return random.choice(self.synonyms['budget'])
    
    def get_price_description(self, price_range: str) -> str:
        """Convert price range to natural description."""
        price_map = {
            'under_10L': random.choice(['under 10 lakhs', 'below 10L', 'within 10 lakhs budget']),
            '10-20L': random.choice(['10 to 20 lakhs', 'between 10-20L', 'around 15 lakhs']),
            '20-30L': random.choice(['20 to 30 lakhs', 'between 20-30L', 'around 25 lakhs']),
            'above_30L': random.choice(['above 30 lakhs', 'over 30L', 'premium price range']),
        }
        return price_map.get(price_range, price_range)
    
    def generate_description(self, car: Dict) -> str:
        """Generate a natural language description for a car."""
        # Prepare car features
        features = {
            'brand': car['brand'],
            'model': car['model'],
            'type': random.choice(self.synonyms.get(car['body_type'].lower(), [car['body_type']])),
            'fuel': random.choice(self.synonyms.get(car['fuel_type'].lower(), [car['fuel_type']])),
            'price': self.get_price_description(car['price_range']),
            'luxury': self.get_luxury_label(car),
        }
        
        # Choose template category (weighted towards combined/natural)
        category = random.choices(
            ['brand_focused', 'type_focused', 'fuel_focused', 'price_focused', 'combined', 'natural'],
            weights=[1, 1, 1, 1, 3, 4]
        )[0]
        
        template = random.choice(self.templates[category])
        
        try:
            description = template.format(**features)
            return description
        except KeyError:
            # Fallback to simple description
            return f"{features['brand']} {features['type']}"
    
    def generate_training_data(self, samples_per_car: int = 5) -> List[Tuple[str, str]]:
        """
        Generate training data.
        
        Args:
            samples_per_car: Number of description variants per car
            
        Returns:
            List of (description, car_label) tuples
        """
        training_data = []
        
        for car in self.cars:
            # Create unique label for each car
            car_label = f"{car['brand']}_{car['model']}".replace(' ', '_').lower()
            
            # Generate multiple descriptions for this car
            for _ in range(samples_per_car):
                description = self.generate_description(car)
                training_data.append((description, car_label))
        
        print(f"[Data Generator] Generated {len(training_data)} training samples")
        return training_data
    
    def save_training_data(self, training_data: List[Tuple[str, str]], output_file: str = "data/training_data.json"):
        """Save training data to JSON file."""
        data = {
            'samples': [{'text': text, 'label': label} for text, label in training_data],
            'num_samples': len(training_data),
            'num_classes': len(set(label for _, label in training_data))
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"[Data Generator] Saved {len(training_data)} samples to {output_file}")
        print(f"[Data Generator] Number of classes: {data['num_classes']}")


def main():
    """Generate and save training data."""
    print("=" * 70)
    print("  AUTOMIND ML - TRAINING DATA GENERATION")
    print("=" * 70)
    print()
    
    # Generate training data
    generator = TrainingDataGenerator()
    
    # Create 10 samples per car (49 cars × 10 = 490 samples)
    training_data = generator.generate_training_data(samples_per_car=10)
    
    # Display sample data
    print("\nSample training data:")
    print("-" * 70)
    for i, (text, label) in enumerate(random.sample(training_data, min(10, len(training_data))), 1):
        print(f"{i}. '{text}' → {label}")
    print("-" * 70)
    
    # Save to file
    generator.save_training_data(training_data)
    
    print("\n✅ Training data generation complete!")
    print("\nNext steps:")
    print("  1. Review: cat data/training_data.json | less")
    print("  2. Train model: python train_ml_model.py")


if __name__ == "__main__":
    main()
