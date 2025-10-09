#!/usr/bin/env python3
"""
NLP Engine for AutoMind Car Recommendation System
Extracts structured features from natural language user input

RISC-Style AI Architecture:
- ENHANCE_KEYWORDS: Common variations and misspellings
- FUZZY_MATCH: Levenshtein distance matching
- CONTEXT_STACK: Multi-turn conversation memory
"""

import re
import json
import difflib
from typing import Dict, Optional, List, Tuple

# Load pattern database
with open("src/keywords.json") as f:
    PATTERNS = json.load(f)

# RISC AI Enhancement 1: ENHANCED_KEYWORDS
# Common variations, nicknames, and misspellings
BRAND_VARIATIONS = {
    'maruti': ['maruti', 'maruti suzuki', 'suzuki', 'maruthi'],
    'toyota': ['toyota', 'tayota', 'toyata'],
    'hyundai': ['hyundai', 'hundai', 'hyunday', 'hyndai'],
    'honda': ['honda', 'handa', 'hunda'],
    'bmw': ['bmw', 'beemer', 'bimmer'],
    'mercedes': ['mercedes', 'merc', 'benz', 'mercedes-benz'],
    'tata': ['tata', 'tataa'],
    'mahindra': ['mahindra', 'mahendra'],
    'ford': ['ford', 'fard'],
    'kia': ['kia', 'keya'],
}

MODEL_VARIATIONS = {
    'civic': ['civic', 'sivic'],
    'accord': ['accord', 'acord'],
    'crv': ['crv', 'cr-v', 'honda crv'],
    'camry': ['camry', 'camery'],
    'corolla': ['corolla', 'carolla', 'corola'],
    'fortuner': ['fortuner', 'fortner', 'fortunar'],
    'swift': ['swift', 'swfit'],
    'creta': ['creta', 'creeta'],
}

# RISC AI Enhancement 3: CONTEXT_STACK
# Simple conversation context memory
CONTEXT_STACK = []
MAX_CONTEXT_TURNS = 3

# RISC AI Enhancement 4: SMART CLARIFICATION
# Low confidence threshold for asking clarifying questions
CLARIFY_WHEN_CONFIDENT = 0.3  # Ask for clarification when confidence < 30%

# RISC AI Enhancement 5: PREFERENCE LEARNING
# Simple user preference tracking
USER_PREFERENCES = {
    'prefers_electric': None,
    'prefers_suv': None,
    'preferred_brands': [],
    'price_sensitivity': None  # 'budget', 'luxury', or None
}


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    RISC AI Enhancement 2: FUZZY_MATCH
    Calculate Levenshtein distance between two strings.
    Simpler than difflib for basic fuzzy matching.
    
    Args:
        s1, s2: Strings to compare
        
    Returns:
        Edit distance (number of operations to transform s1 to s2)
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def fuzzy_match(target: str, query: str, threshold: float = 0.75) -> bool:
    """
    RISC AI Enhancement 2: FUZZY_MATCH
    Check if target matches query using fuzzy matching.
    
    Args:
        target: The string to match against
        query: The search string
        threshold: Similarity threshold (0-1), default 0.75
        
    Returns:
        True if match is above threshold
    """
    # Exact match
    if target in query or query in target:
        return True
    
    # Fuzzy match using Levenshtein distance
    max_len = max(len(target), len(query))
    if max_len == 0:
        return False
    
    distance = levenshtein_distance(target, query)
    similarity = 1 - (distance / max_len)
    
    return similarity >= threshold


def update_context(query: str, features: Dict[str, Optional[str]]) -> None:
    """
    RISC AI Enhancement 3: CONTEXT_STACK
    Update conversation context with latest query and features.
    
    Args:
        query: User's query text
        features: Extracted features from query
    """
    global CONTEXT_STACK
    
    CONTEXT_STACK.append({
        'query': query,
        'features': features.copy()
    })
    
    # Keep only last N turns
    if len(CONTEXT_STACK) > MAX_CONTEXT_TURNS:
        CONTEXT_STACK.pop(0)


def get_context_feature(feature_name: str) -> Optional[str]:
    """
    RISC AI Enhancement 3: CONTEXT_STACK
    Get feature value from recent context if not found in current query.
    
    Args:
        feature_name: Name of feature to retrieve
        
    Returns:
        Feature value from context or None
    """
    # Search backwards through context (most recent first)
    for context in reversed(CONTEXT_STACK):
        if context['features'].get(feature_name):
            return context['features'][feature_name]
    return None


def extract_features(text: str, use_context: bool = True) -> Dict[str, Optional[str]]:
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
    
    # Handle common variations and unclear queries
    if len(text.strip()) < 3:
        print(f"[NLP Engine] Input too short: '{original_text}'")
        return _empty_features(original_text)
    
    # Check if query is too vague
    vague_queries = ['car', 'vehicle', 'automobile', 'something', 'anything', 'good', 'nice', 'best']
    words = text.split()
    if len(words) <= 2 and any(vague in text for vague in vague_queries):
        print(f"[NLP Engine] Vague input: '{original_text}'")
        print(f"[NLP Engine] Please be more specific (e.g., 'Toyota SUV', 'cheap hatchback')")
    
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
    features['brand'] = _extract_brand(text, original_text, use_context)
    
    # 2. BODY TYPE DETECTION with synonyms
    features['type'] = _extract_body_type(text, negations.get('type'))
    
    # 3. FUEL TYPE DETECTION with synonyms
    features['fuel'] = _extract_fuel_type(text, negations.get('fuel'))
    
    # 4. PRICE RANGE DETECTION
    features['price_range'] = _extract_price_range(text)
    
    # 5. LUXURY/BUDGET DETECTION
    features['luxury'] = _extract_luxury_status(text, features)
    
    # RISC AI Enhancement 3: Update context stack
    if use_context:
        update_context(original_text, features)
    
    # RISC AI Enhancement 5: Update preferences
    update_preferences(features)
    
    # Calculate confidence score
    confidence = calculate_confidence(features)
    
    # Log what was detected (for debugging)
    print(f"[NLP Engine] Input: '{original_text}'")
    print(f"[NLP Engine] Detected: {features}")
    print(f"[NLP Engine] Confidence: {confidence:.1%}")
    
    # RISC AI Enhancement 4: Suggest clarification if needed
    clarification = suggest_clarification(features, confidence)
    if clarification:
        print(f"[NLP Engine] Suggestion: {clarification}")
    
    return features


def _empty_features(original_text: str) -> Dict[str, Optional[str]]:
    """Return empty features dictionary for unclear queries."""
    print(f"[NLP Engine] Input: '{original_text}'")
    print(f"[NLP Engine] Detected: No clear features - query too vague")
    return {
        "brand": None,
        "type": None,
        "fuel": None,
        "price_range": None,
        "luxury": None
    }


def _extract_brand(text: str, original_text: str, use_context: bool = True) -> Optional[str]:
    """
    RISC AI Enhancement 1+2: ENHANCE_KEYWORDS + FUZZY_MATCH
    Extract car brand with enhanced keywords and fuzzy matching.
    
    Args:
        text: Preprocessed query text (lowercase)
        original_text: Original user query
        use_context: Whether to use context stack for fallback
        
    Returns:
        Brand name or None
    """
    # Step 1: Check enhanced brand variations (nicknames, common misspellings)
    for brand_key, variations in BRAND_VARIATIONS.items():
        for variation in variations:
            if re.search(rf"\b{variation}\b", text):
                return brand_key.title()
    
    # Step 2: Direct match from dataset
    for brand in PATTERNS["brands"]:
        brand_words = brand.split()
        if any(re.search(rf"\b{word}\b", text) for word in brand_words):
            return brand.title()
    
    # Step 3: RISC FUZZY_MATCH - Use Levenshtein distance for typos
    words = text.split()
    all_brands = list(BRAND_VARIATIONS.keys()) + PATTERNS["brands"]
    
    for word in words:
        if len(word) > 3:  # Only check meaningful words
            for brand in all_brands:
                # Use our custom fuzzy matcher
                if fuzzy_match(brand, word, threshold=0.75):
                    return brand.title()
    
    # Step 4: RISC CONTEXT_STACK - Fallback to context if available
    if use_context:
        context_brand = get_context_feature('brand')
        if context_brand:
            print(f"[NLP Engine] Using brand from context: {context_brand}")
            return context_brand
    
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


def get_context_stack() -> List[Dict]:
    """
    Get current conversation context.
    
    Returns:
        List of context turns (recent first)
    """
    return list(reversed(CONTEXT_STACK))


def clear_context() -> None:
    """Clear conversation context (start fresh conversation)."""
    global CONTEXT_STACK
    CONTEXT_STACK = []


def calculate_confidence(features: Dict[str, Optional[str]]) -> float:
    """
    RISC AI Enhancement 4: SMART CLARIFICATION
    Calculate confidence score based on number and quality of extracted features.
    
    Args:
        features: Extracted features dictionary
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    score = 0.0
    max_score = 100.0
    
    # Brand detection: 30 points
    if features.get('brand'):
        score += 30
    
    # Body type detection: 20 points
    if features.get('type'):
        score += 20
    
    # Fuel type detection: 20 points
    if features.get('fuel'):
        score += 20
    
    # Price range detection: 20 points
    if features.get('price_range'):
        score += 20
    
    # Luxury status detection: 10 points
    if features.get('luxury') is not None:
        score += 10
    
    return score / max_score


def handle_confusion() -> str:
    """
    RISC AI Enhancement 6: CONVERSATION REPAIR
    Provide helpful message when query is unclear or confusing.
    
    Returns:
        Helpful guidance message
    """
    return "I'm not sure I understand. Could you mention the brand name or car type? For example: 'Toyota SUV' or 'luxury sedan'"


def suggest_clarification(features: Dict[str, Optional[str]], confidence: float) -> Optional[str]:
    """
    RISC AI Enhancement 4: SMART CLARIFICATION
    Suggest clarification questions when confidence is low.
    
    Args:
        features: Extracted features
        confidence: Confidence score (0-1)
        
    Returns:
        Clarification question or None if confidence is sufficient
    """
    if confidence >= CLARIFY_WHEN_CONFIDENT:
        return None
    
    # Build clarification based on what's missing
    missing = []
    if not features.get('brand'):
        missing.append("brand (e.g., Toyota, Hyundai, Maruti)")
    if not features.get('type'):
        missing.append("type (SUV, sedan, or hatchback)")
    if not features.get('fuel'):
        missing.append("fuel type (petrol, diesel, electric)")
    if not features.get('price_range'):
        missing.append("budget (e.g., under 20 lakhs)")
    
    if missing:
        return f"I could use more details. Consider specifying: {', '.join(missing[:2])}"
    
    return None


def update_preferences(features: Dict[str, Optional[str]]) -> None:
    """
    RISC AI Enhancement 5: PREFERENCE LEARNING
    Update user preferences based on their queries.
    
    Args:
        features: Extracted features from query
    """
    global USER_PREFERENCES
    
    # Track electric preference
    if features.get('fuel') == 'electric':
        USER_PREFERENCES['prefers_electric'] = True
    elif features.get('fuel') in ['petrol', 'diesel']:
        if USER_PREFERENCES['prefers_electric'] is None:
            USER_PREFERENCES['prefers_electric'] = False
    
    # Track SUV preference
    if features.get('type') == 'suv':
        USER_PREFERENCES['prefers_suv'] = True
    elif features.get('type') in ['sedan', 'hatchback']:
        if USER_PREFERENCES['prefers_suv'] is None:
            USER_PREFERENCES['prefers_suv'] = False
    
    # Track brand preferences
    if features.get('brand'):
        brand = features['brand']
        if brand not in USER_PREFERENCES['preferred_brands']:
            USER_PREFERENCES['preferred_brands'].append(brand)
            # Keep only last 3 brands
            if len(USER_PREFERENCES['preferred_brands']) > 3:
                USER_PREFERENCES['preferred_brands'].pop(0)
    
    # Track price sensitivity
    if features.get('luxury') is True:
        USER_PREFERENCES['price_sensitivity'] = 'luxury'
    elif features.get('luxury') is False:
        USER_PREFERENCES['price_sensitivity'] = 'budget'


def get_preferences() -> Dict:
    """
    RISC AI Enhancement 5: PREFERENCE LEARNING
    Get current user preferences.
    
    Returns:
        User preferences dictionary
    """
    return USER_PREFERENCES.copy()


def reset_preferences() -> None:
    """
    RISC AI Enhancement 5: PREFERENCE LEARNING
    Reset user preferences to defaults.
    """
    global USER_PREFERENCES
    USER_PREFERENCES = {
        'prefers_electric': None,
        'prefers_suv': None,
        'preferred_brands': [],
        'price_sensitivity': None
    }


def suggest_similar_queries(text: str) -> List[str]:
    """Suggest similar queries based on unclear input."""
    suggestions = []
    
    text_lower = text.lower()
    
    # If mentions price but no other details
    if any(word in text_lower for word in ['cheap', 'budget', 'under', 'above', 'lakhs', 'lacs']):
        suggestions.append("Try: 'Cheap hatchback under 10 lakhs'")
        suggestions.append("Or: 'SUV under 20 lakhs'")
    
    # If mentions luxury but no details
    if any(word in text_lower for word in ['luxury', 'premium', 'expensive']):
        suggestions.append("Try: 'Luxury sedan above 30 lakhs'")
        suggestions.append("Or: 'Premium BMW sedan'")
    
    # If mentions fuel but no type
    if any(word in text_lower for word in ['electric', 'ev', 'diesel', 'petrol']):
        suggestions.append("Try: 'Electric hatchback'")
        suggestions.append("Or: 'Diesel SUV under 25 lakhs'")
    
    # Generic suggestions if none match
    if not suggestions:
        suggestions = [
            "Try: 'Toyota SUV under 20 lakhs'",
            "Or: 'Cheap Maruti hatchback'",
            "Or: 'Electric cars under 30 lakhs'"
        ]
    
    return suggestions[:3]  # Return top 3


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
