#!/usr/bin/env python3
"""
NLP Engine for AutoMind Car Recommendation System
Extracts structured features from natural language user input
"""

import re
import json
import difflib
from typing import Dict, Optional, List

# Load pattern database
with open("src/keywords.json") as f:
    PATTERNS = json.load(f)


def extract_features(text: str) -> Dict[str, Optional[str]]:
    """
    Extract car features from user input text.
    
    Args:
        text: User input string describing a car
        
    Returns:
        Dictionary with extracted features:
        {
            'brand': str or None,
            'type': str or None, 
            'fuel': str or None,
            'price_range': str or None,
            'luxury': bool or None
        }
    
    Example:
        >>> extract_features("A Toyota SUV under 20 lakhs")
        {'brand': 'Toyota', 'type': 'SUV', 'fuel': None, 'price_range': 'under_20L', 'luxury': None}
    """
    # Preprocessing
    original_text = text
    text = text.lower()
    text = re.sub(r'\b(car|cars|vehicle|vehicles|want|looking|show|give|me|a|an|the)\b', '', text)
    text = text.strip()
    
    # Initialize result dictionary
    features = {
        "brand": None,
        "type": None,
        "fuel": None,
        "price_range": None,
        "luxury": None
    }
    
    # Check for negations
    negations = {
        "brand": None,
        "type": None,
        "fuel": None
    }
    
    # Detect negations
    negation_patterns = [
        (r'not\s+(\w+)', 'not'),
        (r'no\s+(\w+)', 'no'),
        (r'without\s+(\w+)', 'without')
    ]
    
    for pattern, neg_type in negation_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            negated_word = match.group(1)
            # Check what's being negated
            for fuel_type in ['electric', 'diesel', 'petrol', 'ev', 'gasoline']:
                if fuel_type in negated_word:
                    negations['fuel'] = negated_word
            for body_type in ['suv', 'sedan', 'hatchback']:
                if body_type in negated_word:
                    negations['type'] = negated_word
    
    # 1. BRAND DETECTION with fuzzy matching
    features['brand'] = _extract_brand(text, original_text)
    
    # 2. BODY TYPE DETECTION with synonyms
    features['type'] = _extract_body_type(text, negations.get('type'))
    
    # 3. FUEL TYPE DETECTION with synonyms
    features['fuel'] = _extract_fuel_type(text, negations.get('fuel'))
    
    # 4. PRICE RANGE DETECTION
    features['price_range'] = _extract_price_range(text)
    
    # 5. LUXURY/BUDGET DETECTION
    features['luxury'] = _extract_luxury_status(text, features)
    
    # Log what was detected (for debugging)
    print(f"[NLP Engine] Input: '{original_text}'")
    print(f"[NLP Engine] Detected: {features}")
    
    return features


def _extract_brand(text: str, original_text: str) -> Optional[str]:
    """Extract car brand with fuzzy matching for typos."""
    # Direct match
    for brand in PATTERNS["brands"]:
        brand_words = brand.split()
        if any(re.search(rf"\b{word}\b", text) for word in brand_words):
            return brand.title()
    
    # Common brands not in dataset
    common_brands = ["bmw", "audi", "mercedes", "lexus", "jaguar", "volvo", "tesla"]
    for brand in common_brands:
        if re.search(rf"\b{brand}\b", text):
            return brand.upper() if brand == "bmw" else brand.title()
    
    # Fuzzy matching for typos (e.g., "Tayota" -> "Toyota")
    words = original_text.lower().split()
    all_brands = PATTERNS["brands"] + common_brands
    
    for word in words:
        if len(word) > 3:  # Only check words longer than 3 chars
            matches = difflib.get_close_matches(word, all_brands, n=1, cutoff=0.75)
            if matches:
                brand = matches[0]
                return brand.upper() if brand == "bmw" else brand.title()
    
    return None


def _extract_body_type(text: str, negated: Optional[str] = None) -> Optional[str]:
    """Extract body type with synonym support."""
    body_type_synonyms = {
        "suv": ["suv", "suvs", "crossover", "crossovers", "4x4", "off-road", "sport utility"],
        "sedan": ["sedan", "sedans", "saloon", "saloons"],
        "hatchback": ["hatchback", "hatchbacks", "hatch", "compact"]
    }
    
    for body_type, synonyms in body_type_synonyms.items():
        # Skip if this type is negated
        if negated and body_type in negated:
            continue
            
        for synonym in synonyms:
            if re.search(rf"\b{synonym}\b", text):
                return body_type
    
    return None


def _extract_fuel_type(text: str, negated: Optional[str] = None) -> Optional[str]:
    """Extract fuel type with synonym support."""
    fuel_synonyms = {
        "electric": ["electric", "ev", "battery", "e-car", "zero-emission", "e-vehicle"],
        "diesel": ["diesel"],
        "petrol": ["petrol", "gasoline", "gas"]
    }
    
    for fuel_type, synonyms in fuel_synonyms.items():
        # Skip if this fuel type is negated
        if negated:
            for syn in synonyms:
                if syn in negated:
                    continue
        
        for synonym in synonyms:
            if re.search(rf"\b{synonym}\b", text):
                return fuel_type
    
    return None


def _extract_price_range(text: str) -> Optional[str]:
    """Extract price range using regex patterns."""
    # Patterns for Indian currency format
    under_pattern = r'(under|below|upto|within|less\s+than|maximum)\s*(\d+)\s*(lakhs?|lacs?|l)'
    above_pattern = r'(above|over|more\s+than|starting|minimum)\s*(\d+)\s*(lakhs?|lacs?)'
    around_pattern = r'(around|approximately|about)\s*(\d+)\s*(lakhs?|lacs?|l)'
    
    # Check "under" patterns
    match = re.search(under_pattern, text)
    if match:
        amount = int(match.group(2))
        if amount <= 10:
            return "under_10L"
        elif amount <= 20:
            return "under_20L"
        elif amount <= 30:
            return "under_30L"
        else:
            return "20-30L"
    
    # Check "above" patterns
    match = re.search(above_pattern, text)
    if match:
        amount = int(match.group(2))
        if amount >= 50:
            return "above_30L"
        elif amount >= 30:
            return "above_30L"
        elif amount >= 20:
            return "20-30L"
        else:
            return "10-20L"
    
    # Check "around" patterns
    match = re.search(around_pattern, text)
    if match:
        amount = int(match.group(2))
        if amount <= 10:
            return "under_10L"
        elif amount <= 20:
            return "10-20L"
        elif amount <= 30:
            return "20-30L"
        else:
            return "above_30L"
    
    return None


def _extract_luxury_status(text: str, features: Dict) -> Optional[bool]:
    """Determine luxury status from keywords and context."""
    luxury_keywords = ["luxury", "premium", "high-end", "expensive", "flagship", "elite", "prestige"]
    budget_keywords = ["cheap", "affordable", "budget", "economical", "value", "entry-level", "basic", "low-cost"]
    luxury_brands = ["bmw", "mercedes", "audi", "lexus", "jaguar", "volvo", "land rover"]
    
    # Check explicit keywords
    if any(re.search(rf"\b{kw}\b", text) for kw in luxury_keywords):
        return True
    
    if any(re.search(rf"\b{kw}\b", text) for kw in budget_keywords):
        return False
    
    # Infer from brand
    if features.get('brand'):
        brand_lower = features['brand'].lower()
        if any(luxury_brand in brand_lower for luxury_brand in luxury_brands):
            return True
    
    # Infer from price
    price_range = features.get('price_range')
    if price_range:
        if 'above_30L' in price_range:
            return True
        elif 'under_10L' in price_range:
            return False
    
    return None


def preprocess_text(text: str) -> str:
    """
    Preprocess user input text.
    - Convert to lowercase
    - Remove punctuation (keeping spaces)
    - Normalize whitespace
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())
    return text


def get_supported_brands() -> List[str]:
    """Return list of supported car brands."""
    return PATTERNS.get("brands", []) + ["bmw", "audi", "mercedes", "lexus", "jaguar", "volvo", "tesla"]


def get_supported_types() -> List[str]:
    """Return list of supported body types."""
    return ["suv", "sedan", "hatchback"]


def get_supported_fuels() -> List[str]:
    """Return list of supported fuel types."""
    return ["electric", "diesel", "petrol"]


if __name__ == "__main__":
    # Test the module
    test_inputs = [
        "A Toyota SUV under 20 lakhs",
        "Luxury BMW sedan above 50L",
        "cheap Maruti hatchback under 10 lakhs",
        "electric car by Tesla",
        "Hyundai Creta",
        "not electric, petrol SUV",
        "Tayota Fortuner",  # Typo test
        "around 15 lakhs sedan"
    ]
    
    print("=" * 70)
    print("NLP ENGINE TEST")
    print("=" * 70)
    
    for test in test_inputs:
        print(f"\nInput: '{test}'")
        result = extract_features(test)
        print(f"Output: {result}")
        print("-" * 70)
