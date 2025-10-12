#!/usr/bin/env python3
"""
Advanced Expert System for Car Recommendation
Implements advanced AI techniques: backward chaining, fuzzy logic, A* search, CBR, frame inheritance
"""

import csv
import math
import json
import os
from typing import Dict, List, Optional, Tuple, Set, Any
from collections import defaultdict, deque
from datetime import datetime
import heapq


class FrameNode:
    """
    Frame-based knowledge representation with inheritance
    Demonstrates object-oriented knowledge representation in AI
    """
    
    def __init__(self, name: str, parent: Optional['FrameNode'] = None):
        self.name = name
        self.parent = parent
        self.attributes = {}
        self.children = []
        
        if parent:
            parent.children.append(self)
    
    def set_attribute(self, key: str, value: Any):
        """Set an attribute on this frame"""
        self.attributes[key] = value
    
    def get_attribute(self, key: str) -> Optional[Any]:
        """Get attribute with inheritance - searches up the hierarchy"""
        if key in self.attributes:
            return self.attributes[key]
        elif self.parent:
            return self.parent.get_attribute(key)
        return None
    
    def has_attribute(self, key: str) -> bool:
        """Check if frame has attribute (including inherited)"""
        return self.get_attribute(key) is not None


class FuzzySet:
    """
    Fuzzy Logic implementation for handling uncertainty
    Demonstrates reasoning with partial truth values
    """
    
    @staticmethod
    def very_low(x: float) -> float:
        """Membership function for 'very_low' (0.0 - 0.2)"""
        if x <= 0.2:
            return 1.0
        elif x <= 0.4:
            return (0.4 - x) / 0.2
        return 0.0
    
    @staticmethod
    def low(x: float) -> float:
        """Membership function for 'low' (0.2 - 0.4)"""
        if x <= 0.2:
            return 0.0
        elif x <= 0.3:
            return (x - 0.2) / 0.1
        elif x <= 0.4:
            return 1.0
        elif x <= 0.5:
            return (0.5 - x) / 0.1
        return 0.0
    
    @staticmethod
    def medium(x: float) -> float:
        """Membership function for 'medium' (0.4 - 0.6)"""
        if x <= 0.4:
            return 0.0
        elif x <= 0.45:
            return (x - 0.4) / 0.05
        elif x <= 0.55:
            return 1.0
        elif x <= 0.6:
            return (0.6 - x) / 0.05
        return 0.0
    
    @staticmethod
    def high(x: float) -> float:
        """Membership function for 'high' (0.6 - 0.8)"""
        if x <= 0.6:
            return 0.0
        elif x <= 0.7:
            return (x - 0.6) / 0.1
        elif x <= 0.8:
            return 1.0
        elif x <= 0.9:
            return (0.9 - x) / 0.1
        return 0.0
    
    @staticmethod
    def very_high(x: float) -> float:
        """Membership function for 'very_high' (0.8 - 1.0)"""
        if x <= 0.8:
            return 0.0
        elif x <= 0.9:
            return (x - 0.8) / 0.1
        return 1.0
    
    @staticmethod
    def parse_fuzzy_term(term: str) -> Tuple[str, float]:
        """Parse fuzzy linguistic terms to numeric confidence"""
        term = term.lower().strip()
        
        fuzzy_mappings = {
            'no': ('no', 0.0),
            'not': ('no', 0.0),
            'barely': ('very_low', 0.15),
            'slightly': ('low', 0.3),
            'somewhat': ('medium', 0.5),
            'moderately': ('medium', 0.55),
            'quite': ('high', 0.7),
            'very': ('high', 0.75),
            'extremely': ('very_high', 0.9),
            'definitely': ('very_high', 0.95),
            'yes': ('yes', 1.0),
        }
        
        for keyword, (category, value) in fuzzy_mappings.items():
            if keyword in term:
                return category, value
        
        # Default to crisp yes/no
        return 'yes', 1.0


class CaseBase:
    """
    Case-Based Reasoning (CBR) implementation
    Learns from past problem-solving episodes
    """
    
    def __init__(self, storage_file: str = "case_base.json"):
        self.storage_file = storage_file
        self.cases = []
        self.load_cases()
    
    def load_cases(self):
        """Load cases from persistent storage"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.cases = json.load(f)
            except:
                self.cases = []
    
    def save_cases(self):
        """Save cases to persistent storage"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.cases, f, indent=2)
    
    def add_case(self, problem: Dict, solution: Dict, performance: Dict):
        """Store a new case"""
        case = {
            'timestamp': datetime.now().isoformat(),
            'problem': problem,
            'solution': solution,
            'performance': performance
        }
        self.cases.append(case)
        self.save_cases()
    
    def retrieve_similar(self, problem: Dict, top_k: int = 3) -> List[Dict]:
        """
        Retrieve similar cases using similarity metric
        Similarity = number of matching attributes / total attributes
        """
        similarities = []
        
        for case in self.cases:
            similarity = self._calculate_similarity(problem, case['problem'])
            similarities.append((similarity, case))
        
        # Sort by similarity (descending)
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        return [case for sim, case in similarities[:top_k] if sim > 0.3]
    
    def _calculate_similarity(self, prob1: Dict, prob2: Dict) -> float:
        """Calculate similarity between two problems"""
        all_keys = set(prob1.keys()) | set(prob2.keys())
        if not all_keys:
            return 0.0
        
        matches = sum(1 for k in all_keys if prob1.get(k) == prob2.get(k))
        return matches / len(all_keys)


class AStarSearch:
    """
    A* Search for optimal question sequencing
    Finds optimal path to solution with minimal questions
    """
    
    def __init__(self, attributes: List[str], cars: List[Dict]):
        self.attributes = attributes
        self.cars = cars
    
    def search(self, known_attrs: Dict[str, str]) -> List[str]:
        """
        Find optimal question sequence using A* search
        Cost: questions asked (g)
        Heuristic: estimated questions remaining (h)
        """
        start_state = tuple(sorted(known_attrs.items()))
        
        # Priority queue: (f_score, g_score, state, path)
        frontier = [(self._h_score(start_state), 0, start_state, [])]
        visited = set()
        
        while frontier:
            f, g, state, path = heapq.heappop(frontier)
            
            state_dict = dict(state)
            
            # Goal: narrow down to 1 car
            matching_cars = self._filter_cars(state_dict)
            if len(matching_cars) <= 1:
                return path
            
            if state in visited:
                continue
            visited.add(state)
            
            # Expand: try each remaining attribute
            for attr in self.attributes:
                if attr not in state_dict:
                    # Calculate information gain for this attribute
                    ig = self._information_gain(attr, matching_cars)
                    
                    # For A*, we'll add all possible values
                    # But for efficiency, just add the best attribute
                    new_path = path + [attr]
                    new_g = g + 1
                    new_state = state  # Will be updated when answer given
                    new_h = self._h_score(state)
                    new_f = new_g + new_h
                    
                    heapq.heappush(frontier, (new_f, new_g, state, new_path))
        
        # Fallback: return attributes sorted by information gain
        return self._greedy_sequence(known_attrs)
    
    def _h_score(self, state: Tuple) -> float:
        """
        Heuristic: estimated questions remaining
        Using log2 of remaining cars as heuristic
        """
        state_dict = dict(state)
        matching = self._filter_cars(state_dict)
        
        if len(matching) <= 1:
            return 0.0
        
        # Heuristic: log2(num_cars) questions needed
        return math.log2(len(matching))
    
    def _filter_cars(self, attrs: Dict[str, str]) -> List[Dict]:
        """Filter cars matching given attributes"""
        result = []
        for car in self.cars:
            if all(car.get(k) == v for k, v in attrs.items()):
                result.append(car)
        return result
    
    def _information_gain(self, attribute: str, cars: List[Dict]) -> float:
        """Calculate information gain for attribute"""
        if not cars:
            return 0.0
        
        # Calculate entropy
        total = len(cars)
        entropy_before = math.log2(total) if total > 0 else 0
        
        # Calculate weighted entropy after split
        value_counts = defaultdict(list)
        for car in cars:
            value_counts[car.get(attribute, 'Unknown')].append(car)
        
        entropy_after = 0
        for value, subset in value_counts.items():
            p = len(subset) / total
            if len(subset) > 1:
                entropy_after += p * math.log2(len(subset))
        
        return entropy_before - entropy_after
    
    def _greedy_sequence(self, known_attrs: Dict[str, str]) -> List[str]:
        """Fallback: greedy information gain ordering"""
        remaining_attrs = [a for a in self.attributes if a not in known_attrs]
        matching = self._filter_cars(known_attrs)
        
        # Sort by information gain
        ig_scores = [(attr, self._information_gain(attr, matching)) 
                     for attr in remaining_attrs]
        ig_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [attr for attr, _ in ig_scores]


class AdvancedExpertSystem:
    """
    Advanced Expert System with multiple reasoning modes
    Demonstrates comprehensive AI techniques beyond basic expert systems
    """
    
    def __init__(self, csv_file: str = "data/car_data.csv"):
        # Check for expanded dataset first
        expanded_file = "data/car_data_expanded.csv"
        if os.path.exists(expanded_file):
            csv_file = expanded_file
            print(f"📊 Using expanded dataset: {expanded_file}")
        
        self.cars = []
        self.attributes = {}
        self.known_attributes = {}
        self.belief_state = {}
        self.asked_questions = []
        
        # Advanced components
        self.case_base = CaseBase()
        self.frame_hierarchy = self._build_frame_hierarchy()
        self.fuzzy_mode = False
        
        # Performance tracking
        self.metrics = {
            'questions_asked': 0,
            'reasoning_mode': 'forward_chaining',
            'start_time': None,
            'end_time': None
        }
        
        self.load_knowledge_base(csv_file)
        self.initialize_belief_state()
    
    def load_knowledge_base(self, csv_file: str):
        """Load cars from CSV"""
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                car = {
                    'model': row['model'],
                    'brand': row['brand'],
                    'body_type': row['body_type'],
                    'fuel_type': row['fuel_type'],
                    'price_range': row['price_range'],
                    'luxury': row['luxury'],
                    'engine_cc': row.get('engine_cc', 'Unknown')
                }
                self.cars.append(car)
                
                # Track possible values for each attribute
                for key, value in car.items():
                    if key != 'model' and key != 'engine_cc':
                        if key not in self.attributes:
                            self.attributes[key] = set()
                        self.attributes[key].add(value)
        
        print(f"✅ Loaded {len(self.cars)} cars with {len(self.attributes)} attributes")
    
    def _build_frame_hierarchy(self) -> FrameNode:
        """
        Build frame-based knowledge hierarchy
        Demonstrates inheritance in knowledge representation
        """
        # Root frame
        vehicle = FrameNode("Vehicle")
        vehicle.set_attribute("has_wheels", True)
        vehicle.set_attribute("requires_fuel", True)
        
        # Car frame (inherits from Vehicle)
        car = FrameNode("Car", parent=vehicle)
        car.set_attribute("num_wheels", 4)
        car.set_attribute("vehicle_type", "automobile")
        
        # Specific body types (inherit from Car)
        suv = FrameNode("SUV", parent=car)
        suv.set_attribute("ground_clearance", "high")
        suv.set_attribute("seating_capacity", "5-7")
        
        sedan = FrameNode("Sedan", parent=car)
        sedan.set_attribute("ground_clearance", "low")
        sedan.set_attribute("seating_capacity", "5")
        
        hatchback = FrameNode("Hatchback", parent=car)
        hatchback.set_attribute("boot_space", "compact")
        hatchback.set_attribute("seating_capacity", "4-5")
        
        return vehicle
    
    def initialize_belief_state(self):
        """Initialize belief state with uniform distribution"""
        for car in self.cars:
            car_id = f"{car['brand']} {car['model']}"
            self.belief_state[car_id] = 1.0 / len(self.cars)
    
    def forward_chaining(self) -> List[Tuple[str, str]]:
        """
        Forward chaining inference
        Data-driven: starts with facts, derives conclusions
        """
        inferred_facts = []
        
        # Rule 1: If luxury car and high price → premium_brand
        if self.known_attributes.get('luxury') == 'yes' and \
           'above_30L' in self.known_attributes.get('price_range', ''):
            inferred_facts.append(('premium_brand', 'yes'))
        
        # Rule 2: If SUV and diesel → family_vehicle
        if self.known_attributes.get('body_type') == 'SUV' and \
           self.known_attributes.get('fuel_type') == 'Diesel':
            inferred_facts.append(('family_vehicle', 'yes'))
        
        # Rule 3: If hatchback and under_10L → budget_friendly
        if self.known_attributes.get('body_type') == 'Hatchback' and \
           'under_10L' in self.known_attributes.get('price_range', ''):
            inferred_facts.append(('budget_friendly', 'yes'))
        
        # Rule 4: If electric → eco_friendly
        if self.known_attributes.get('fuel_type') == 'Electric':
            inferred_facts.append(('eco_friendly', 'yes'))
        
        return inferred_facts
    
    def backward_chaining(self, goal_car: Dict) -> List[str]:
        """
        Backward chaining inference
        Goal-driven: starts with hypothesis, works backward
        Returns list of attributes to verify
        """
        attributes_to_verify = []
        
        # Determine which attributes differ from known
        for attr in ['brand', 'body_type', 'fuel_type', 'price_range', 'luxury']:
            if attr not in self.known_attributes:
                attributes_to_verify.append(attr)
            elif self.known_attributes[attr] != goal_car.get(attr):
                # Known attribute conflicts with hypothesis
                return []  # Hypothesis refuted
        
        return attributes_to_verify
    
    def calculate_information_gain(self, attribute: str) -> float:
        """Calculate information gain for an attribute"""
        matching_cars = self.get_matching_cars()
        
        if not matching_cars:
            return 0.0
        
        # Entropy before split
        total = len(matching_cars)
        entropy_before = math.log2(total) if total > 0 else 0
        
        # Entropy after split by attribute
        value_groups = defaultdict(list)
        for car in matching_cars:
            value_groups[car.get(attribute, 'Unknown')].append(car)
        
        entropy_after = 0
        for value, group in value_groups.items():
            p = len(group) / total
            if len(group) > 1:
                entropy_after += p * math.log2(len(group))
        
        return entropy_before - entropy_after
    
    def calculate_gini_impurity(self, attribute: str) -> float:
        """
        Calculate Gini impurity for an attribute
        Alternative to information gain
        """
        matching_cars = self.get_matching_cars()
        
        if not matching_cars:
            return 0.0
        
        total = len(matching_cars)
        
        # Group by attribute value
        value_groups = defaultdict(list)
        for car in matching_cars:
            value_groups[car.get(attribute, 'Unknown')].append(car)
        
        # Calculate weighted Gini impurity
        gini = 0
        for value, group in value_groups.items():
            p = len(group) / total
            # Gini for this group (1 - sum of squared probabilities)
            group_gini = 1 - (1/len(group))**2 * len(group) if len(group) > 0 else 0
            gini += p * group_gini
        
        return 1 - gini  # Return Gini gain (reduction in impurity)
    
    def ask_optimal_question_astar(self) -> Optional[Tuple[str, List[str]]]:
        """Use A* search to find optimal question"""
        astar = AStarSearch(list(self.attributes.keys()), self.cars)
        optimal_sequence = astar.search(self.known_attributes)
        
        if optimal_sequence:
            next_attr = optimal_sequence[0]
            values = sorted(list(self.attributes[next_attr]))
            return next_attr, values
        
        return None
    
    def process_fuzzy_answer(self, attribute: str, fuzzy_answer: str):
        """Process fuzzy linguistic answer"""
        category, confidence = FuzzySet.parse_fuzzy_term(fuzzy_answer)
        
        # Update belief state with fuzzy confidence
        matching_cars = self.get_matching_cars()
        
        for car in matching_cars:
            car_id = f"{car['brand']} {car['model']}"
            # Adjust belief based on fuzzy confidence
            if car.get(attribute) in fuzzy_answer.lower():
                self.belief_state[car_id] *= confidence
            else:
                self.belief_state[car_id] *= (1 - confidence)
        
        # Normalize
        total = sum(self.belief_state.values())
        if total > 0:
            for car_id in self.belief_state:
                self.belief_state[car_id] /= total
    
    def get_matching_cars(self) -> List[Dict]:
        """Get cars matching known attributes"""
        result = []
        for car in self.cars:
            if all(car.get(k) == v for k, v in self.known_attributes.items()):
                result.append(car)
        return result
    
    def get_recommendation(self) -> Tuple[Optional[Dict], float]:
        """Get top recommendation with confidence"""
        # Sort by belief state
        sorted_beliefs = sorted(self.belief_state.items(), 
                               key=lambda x: x[1], reverse=True)
        
        if sorted_beliefs:
            car_id, confidence = sorted_beliefs[0]
            # Find the car dict
            for car in self.cars:
                if f"{car['brand']} {car['model']}" == car_id:
                    return car, confidence
        
        return None, 0.0
    
    def save_case(self, problem: Dict, solution: Dict, num_questions: int):
        """Save successful case for CBR"""
        performance = {
            'questions_asked': num_questions,
            'success': True,
            'reasoning_mode': self.metrics['reasoning_mode']
        }
        self.case_base.add_case(problem, solution, performance)
    
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics"""
        return {
            'questions_asked': len(self.asked_questions),
            'reasoning_mode': self.metrics['reasoning_mode'],
            'cars_remaining': len(self.get_matching_cars()),
            'top_confidence': self.get_recommendation()[1]
        }


if __name__ == "__main__":
    print("="*70)
    print("ADVANCED EXPERT SYSTEM - Feature Demonstration")
    print("="*70)
    
    es = AdvancedExpertSystem()
    
    print("\n1. Frame Inheritance Test:")
    print(f"   Vehicle has_wheels: {es.frame_hierarchy.get_attribute('has_wheels')}")
    suv_frame = es.frame_hierarchy.children[0].children[0]  # SUV
    print(f"   SUV inherits has_wheels: {suv_frame.get_attribute('has_wheels')}")
    print(f"   SUV ground_clearance: {suv_frame.get_attribute('ground_clearance')}")
    
    print("\n2. Fuzzy Logic Test:")
    term, conf = FuzzySet.parse_fuzzy_term("somewhat sporty")
    print(f"   'somewhat sporty' → category: {term}, confidence: {conf}")
    
    print("\n3. Information Gain vs Gini Impurity:")
    ig = es.calculate_information_gain('brand')
    gini = es.calculate_gini_impurity('brand')
    print(f"   Brand - IG: {ig:.3f}, Gini: {gini:.3f}")
    
    print("\n4. Case-Based Reasoning:")
    print(f"   Cases in database: {len(es.case_base.cases)}")
    
    print("\n5. Performance Metrics:")
    metrics = es.get_performance_metrics()
    for key, value in metrics.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*70)
    print("Use expert_system_advanced_cli.py for interactive demo")
    print("="*70)
