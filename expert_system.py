#!/usr/bin/env python3
"""
Expert System for Car Recommendation
Implements classic AI techniques: knowledge base, inference engine, rule-based reasoning
"""

import csv
import math
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict


class CarKnowledgeBase:
    """
    Knowledge Base: Stores facts and rules about cars
    Implements knowledge representation using frames (car attributes)
    """
    
    def __init__(self, csv_file: str = "data/car_data.csv"):
        self.cars = []
        self.all_cars = {}  # Car ID -> car dict
        self.attributes = {}  # Attribute -> possible values
        self.car_attributes = {}  # Car ID -> attributes dict
        self.load_knowledge_base(csv_file)
    
    def load_knowledge_base(self, csv_file: str):
        """Load car knowledge from CSV file"""
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                car_id = idx
                car_dict = {
                    'id': car_id,
                    'model': row['model'],
                    'brand': row['brand'],
                    'body_type': row['body_type'],
                    'fuel_type': row['fuel_type'],
                    'price_range': row['price_range'],
                    'luxury': row['luxury'],
                    'engine_cc': row.get('engine_cc', 'Unknown')
                }
                self.cars.append(car_dict)
                self.all_cars[car_id] = car_dict
                self.car_attributes[car_id] = {
                    'brand': row['brand'],
                    'body_type': row['body_type'],
                    'fuel_type': row['fuel_type'],
                    'price_range': row['price_range'],
                    'luxury': row['luxury']
                }
        
        # Build attribute index
        for car in self.cars:
            for attr in ['brand', 'body_type', 'fuel_type', 'price_range', 'luxury']:
                if attr not in self.attributes:
                    self.attributes[attr] = set()
                self.attributes[attr].add(car[attr])
        
        print(f"[Knowledge Base] Loaded {len(self.cars)} cars")
        print(f"[Knowledge Base] Attributes: {list(self.attributes.keys())}")
    
    def get_attribute_values(self, attribute: str) -> Set[str]:
        """Get all possible values for an attribute"""
        return self.attributes.get(attribute, set())
    
    def get_cars_by_attribute(self, attribute: str, value: str) -> List[Dict]:
        """Get all cars matching a specific attribute value"""
        return [car for car in self.cars 
                if car.get(attribute) == value]


class BeliefState:
    """
    Maintains belief state about which cars are still possible
    Handles uncertainty and updates probabilities based on answers
    """
    
    def __init__(self, all_cars: List[Dict]):
        # Initialize with equal probability for all cars
        self.possible_cars = set(car['id'] for car in all_cars)
        self.all_cars = {car['id']: car for car in all_cars}
        self.known_attributes = {}  # Attribute -> value pairs we know
        self.confidence_scores = {car['id']: 1.0 for car in all_cars}
    
    def update_belief(self, attribute: str, value: str):
        """
        Update belief state based on new information
        Implements uncertainty handling and belief propagation
        """
        self.known_attributes[attribute] = value
        
        # Remove cars that don't match
        matching_cars = set()
        for car_id in self.possible_cars:
            car = self.all_cars[car_id]
            if car.get(attribute) == value:
                matching_cars.add(car_id)
                # Increase confidence for matching cars
                self.confidence_scores[car_id] *= 1.5
            else:
                # Decrease confidence for non-matching cars
                self.confidence_scores[car_id] *= 0.1
        
        self.possible_cars = matching_cars
        
        # Normalize confidence scores
        if self.possible_cars:
            total = sum(self.confidence_scores[cid] for cid in self.possible_cars)
            if total > 0:
                for car_id in self.possible_cars:
                    self.confidence_scores[car_id] /= total
    
    def get_top_candidates(self, n: int = 5) -> List[Tuple[Dict, float]]:
        """Get top N car candidates with confidence scores"""
        if not self.possible_cars:
            return []
        
        candidates = []
        for car_id in self.possible_cars:
            car = self.all_cars[car_id]
            confidence = self.confidence_scores.get(car_id, 0.0)
            candidates.append((car, confidence))
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:n]
    
    def get_possible_count(self) -> int:
        """Get count of possible cars remaining"""
        return len(self.possible_cars)
    
    def is_determined(self) -> bool:
        """Check if we've narrowed down to a single car"""
        return len(self.possible_cars) == 1


class InferenceEngine:
    """
    Inference Engine: Uses forward chaining to reason through questions
    Implements optimal question selection using information gain
    """
    
    def __init__(self, knowledge_base: CarKnowledgeBase):
        self.kb = knowledge_base
        self.asked_attributes = set()
    
    def calculate_information_gain(self, attribute: str, 
                                   possible_cars: Set[int]) -> float:
        """
        Calculate information gain for asking about an attribute
        Uses entropy-based measure to find most informative question
        """
        if not possible_cars or attribute in self.asked_attributes:
            return 0.0
        
        # Get distribution of values for this attribute among possible cars
        value_counts = defaultdict(int)
        for car_id in possible_cars:
            car = self.kb.car_attributes[car_id]
            value = car.get(attribute)
            if value:
                value_counts[value] += 1
        
        # Calculate entropy before asking
        total = len(possible_cars)
        if total == 0:
            return 0.0
        
        # Current entropy
        current_entropy = 0.0
        for count in value_counts.values():
            if count > 0:
                p = count / total
                current_entropy -= p * math.log2(p) if p > 0 else 0
        
        # Expected entropy after asking (weighted by value frequency)
        expected_entropy = 0.0
        for value, count in value_counts.items():
            p_value = count / total
            # Entropy of subset with this value would be 0 (all same value)
            # But we need to consider how many cars remain
            subset_entropy = 0.0  # Simplified: perfect split
            expected_entropy += p_value * subset_entropy
        
        # Information gain
        return current_entropy - expected_entropy
    
    def select_next_question(self, belief_state: BeliefState) -> Optional[str]:
        """
        Forward chaining: Select the most informative question to ask next
        Implements AI search strategy for optimal question selection
        """
        if belief_state.is_determined():
            return None
        
        # Calculate information gain for each unasked attribute
        gains = {}
        for attribute in self.kb.attributes.keys():
            if attribute not in self.asked_attributes:
                gain = self.calculate_information_gain(
                    attribute, belief_state.possible_cars
                )
                gains[attribute] = gain
        
        if not gains:
            return None
        
        # Select attribute with highest information gain
        best_attribute = max(gains.items(), key=lambda x: x[1])[0]
        self.asked_attributes.add(best_attribute)
        
        return best_attribute
    
    def apply_rule(self, rule: str, facts: Dict) -> bool:
        """
        Apply inference rule to determine if condition is met
        Implements rule-based reasoning
        """
        # Example rules:
        # "IF price_range = under_10L AND luxury = No THEN budget_car = True"
        # This is a simplified rule engine for demonstration
        if rule == "budget_car":
            return facts.get('price_range') == 'under_10L' and facts.get('luxury') == 'No'
        elif rule == "luxury_car":
            return facts.get('luxury') == 'Yes'
        elif rule == "family_car":
            return facts.get('body_type') in ['SUV', 'Sedan']
        return False
    
    def forward_chain(self, belief_state: BeliefState) -> Dict[str, bool]:
        """
        Forward chaining inference
        Derive new facts from known attributes using rules
        """
        inferred_facts = {}
        
        # Apply rules based on known attributes
        facts = belief_state.known_attributes
        
        # Rule 1: Budget car identification
        inferred_facts['is_budget'] = self.apply_rule('budget_car', facts)
        
        # Rule 2: Luxury car identification
        inferred_facts['is_luxury'] = self.apply_rule('luxury_car', facts)
        
        # Rule 3: Family car identification
        inferred_facts['is_family'] = self.apply_rule('family_car', facts)
        
        return inferred_facts


class ExpertSystem:
    """
    Main Expert System that coordinates knowledge base, inference engine, and belief state
    Implements complete AI reasoning system for car recommendation
    """
    
    def __init__(self, csv_file: str = "data/car_data.csv"):
        self.kb = CarKnowledgeBase(csv_file)
        self.inference_engine = InferenceEngine(self.kb)
        self.belief_state = BeliefState(self.kb.cars)
        self.question_history = []
    
    def reset(self):
        """Reset the expert system for a new session"""
        self.belief_state = BeliefState(self.kb.cars)
        self.inference_engine.asked_attributes = set()
        self.question_history = []
    
    def ask_question(self) -> Optional[Tuple[str, List[str]]]:
        """
        Generate next question using inference engine
        Returns (attribute_name, possible_values) or None if done
        """
        attribute = self.inference_engine.select_next_question(self.belief_state)
        
        if attribute is None:
            return None
        
        # Get possible values for this attribute from remaining cars
        possible_values = set()
        for car_id in self.belief_state.possible_cars:
            car = self.kb.all_cars[car_id]
            value = car.get(attribute)
            if value:
                possible_values.add(value)
        
        return (attribute, sorted(list(possible_values)))
    
    def process_answer(self, attribute: str, value: str):
        """
        Process user's answer and update belief state
        Implements belief update mechanism
        """
        self.belief_state.update_belief(attribute, value)
        self.question_history.append((attribute, value))
        
        # Run forward chaining to infer new facts
        inferred = self.inference_engine.forward_chain(self.belief_state)
        
        return inferred
    
    def get_recommendation(self) -> Optional[Tuple[Dict, float]]:
        """
        Get final car recommendation with confidence score
        """
        candidates = self.belief_state.get_top_candidates(n=1)
        if candidates:
            return candidates[0]
        return None
    
    def get_top_candidates(self, n: int = 5) -> List[Tuple[Dict, float]]:
        """Get top N candidates with confidence scores"""
        return self.belief_state.get_top_candidates(n)
    
    def get_status(self) -> Dict:
        """Get current status of reasoning process"""
        return {
            'possible_cars': self.belief_state.get_possible_count(),
            'asked_questions': len(self.question_history),
            'is_determined': self.belief_state.is_determined(),
            'known_attributes': dict(self.belief_state.known_attributes)
        }


# Demo/Test function
def demo_expert_system():
    """Demonstrate the expert system"""
    print("=" * 70)
    print("  EXPERT SYSTEM DEMO - AI Reasoning for Car Recommendation")
    print("=" * 70)
    print("\nThis expert system uses:")
    print("  • Knowledge Base (car facts and attributes)")
    print("  • Inference Engine (forward chaining)")
    print("  • Information Gain (optimal question selection)")
    print("  • Belief State (uncertainty handling)")
    print("=" * 70)
    
    # Create expert system
    es = ExpertSystem()
    
    print(f"\n[Expert System] Initialized with {len(es.kb.cars)} cars")
    print(f"[Expert System] Attributes available: {list(es.kb.attributes.keys())}")
    
    # Simulate a conversation
    print("\n" + "=" * 70)
    print("  SIMULATION: Finding a car through AI reasoning")
    print("=" * 70)
    
    # Question 1
    question = es.ask_question()
    if question:
        attr, values = question
        print(f"\n[AI] Question 1: What is the {attr}?")
        print(f"     Options: {values}")
        # Simulate answer
        answer = values[0]
        print(f"[User] Answer: {answer}")
        inferred = es.process_answer(attr, answer)
        status = es.get_status()
        print(f"[AI] Narrowed down to {status['possible_cars']} cars")
        print(f"[AI] Inferred facts: {inferred}")
    
    # Question 2
    question = es.ask_question()
    if question:
        attr, values = question
        print(f"\n[AI] Question 2: What is the {attr}?")
        print(f"     Options: {values}")
        answer = values[0] if values else None
        if answer:
            print(f"[User] Answer: {answer}")
            inferred = es.process_answer(attr, answer)
            status = es.get_status()
            print(f"[AI] Narrowed down to {status['possible_cars']} cars")
            print(f"[AI] Inferred facts: {inferred}")
    
    # Get recommendations
    print("\n" + "=" * 70)
    print("  TOP RECOMMENDATIONS")
    print("=" * 70)
    
    candidates = es.get_top_candidates(n=5)
    for i, (car, confidence) in enumerate(candidates, 1):
        print(f"\n{i}. {car['brand']} {car['model']}")
        print(f"   Confidence: {confidence*100:.1f}%")
        print(f"   Type: {car['body_type']}, Fuel: {car['fuel_type']}")
        print(f"   Price: {car['price_range']}, Luxury: {car['luxury']}")
    
    print("\n" + "=" * 70)
    print("✅ Expert System demonstrates:")
    print("  ✓ Knowledge Representation (car attributes as frames)")
    print("  ✓ Inference Engine (forward chaining)")
    print("  ✓ Information Gain (optimal question selection)")
    print("  ✓ Belief State Management (uncertainty handling)")
    print("  ✓ Rule-Based Reasoning (car classification rules)")
    print("=" * 70)


if __name__ == "__main__":
    demo_expert_system()
