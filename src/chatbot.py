import re
import json

# Load YOUR pattern database (from Day 1)
with open("src/keywords.json") as f:
    PATTERNS = json.load(f)

def respond_to_user(input_text: str) -> str:
    """Rule-based chatbot for Indian car queries (Experiment 5)"""
    input_text = input_text.lower()
    # Remove generic terms that don't help with filtering
    input_text = re.sub(r'\b(car|cars|vehicle|vehicles|want|looking|show|give)\b', '', input_text)
    detected = {"brand": None, "type": None, "price": None, "fuel": None, "luxury": None}
    
    # 1. BRAND DETECTION (Keyword matching from YOUR dataset)
    for brand in PATTERNS["brands"]:
        # Handle both full brand names and partial matches (e.g., "maruti" for "maruti suzuki")
        brand_words = brand.split()
        if any(re.search(rf"\b{word}\b", input_text) for word in brand_words):
            detected["brand"] = brand.title()
            break
    
    # Handle common brand names not in dataset
    if not detected["brand"]:
        common_brands = ["bmw", "audi", "mercedes", "lexus", "jaguar", "volvo"]
        for brand in common_brands:
            if re.search(rf"\b{brand}\b", input_text):
                detected["brand"] = brand.upper() if brand == "bmw" else brand.title()
                break
    
    # 2. BODY TYPE DETECTION (From YOUR body_types with synonyms)
    body_type_synonyms = {
        "suv": ["suv", "suvs", "crossover", "crossovers", "4x4", "off-road", "sport utility"],
        "sedan": ["sedan", "sedans", "saloon", "saloons"],
        "hatchback": ["hatchback", "hatchbacks", "hatch"]
    }
    
    for body_type, synonyms in body_type_synonyms.items():
        for synonym in synonyms:
            if re.search(rf"\b{synonym}\b", input_text):
                detected["type"] = body_type
                break
        if detected["type"]:
            break
    
    # 3. FUEL TYPE DETECTION (From YOUR fuel_types with synonyms)
    fuel_synonyms = {
        "electric": ["electric", "ev", "battery", "e-car", "zero-emission"],
        "diesel": ["diesel"],
        "petrol": ["petrol", "gasoline", "gas"]
    }
    
    for fuel_type, synonyms in fuel_synonyms.items():
        for synonym in synonyms:
            if re.search(rf"\b{synonym}\b", input_text):
                detected["fuel"] = fuel_type
                break
        if detected["fuel"]:
            break
    
    # 4. PRICE DETECTION (Using YOUR price bins)
    price_match = re.search(r'(under|below|upto|within) (\d+)[\s,]*(lakhs?|lacs?|l)', input_text)
    above_match = re.search(r'(above|over|starting) (\d+)[\s,]*(lakhs?|lacs?)', input_text)
    
    if price_match:
        amount = int(price_match.group(2))
        if amount <= 10:
            detected["price"] = "under_10l"
        elif amount <= 20:
            detected["price"] = "10-20l"
        else:
            detected["price"] = "20-30l"
    elif above_match:
        amount = int(above_match.group(2))
        if amount >= 30:
            detected["price"] = "above_30l"
        elif amount >= 20:
            detected["price"] = "20-30l"
        else:
            detected["price"] = "10-20l"
    
    # 5. LUXURY/BUDGET DETECTION (Keywords + Price Inference)
    luxury_keywords = ["luxury", "premium", "high-end", "expensive", "flagship", "elite", "prestige"]
    budget_keywords = ["cheap", "affordable", "budget", "economical", "value", "entry-level", "basic", "low-cost"]
    
    # Luxury brands inference
    luxury_brands = ["bmw", "mercedes", "audi", "lexus", "jaguar", "volvo", "land rover"]
    
    if any(re.search(rf"\b{keyword}\b", input_text) for keyword in luxury_keywords):
        detected["luxury"] = True
    elif any(re.search(rf"\b{keyword}\b", input_text) for keyword in budget_keywords):
        detected["luxury"] = False
    elif detected["brand"] and any(brand.lower() in detected["brand"].lower() for brand in luxury_brands):
        detected["luxury"] = True
    elif detected["price"] and detected["price"] == "above_30l":
        detected["luxury"] = True
    elif detected["price"] and detected["price"] == "under_10l":
        detected["luxury"] = False
    
    # 6. GENERATE RESPONSE (Using YOUR dataset context)
    response_parts = []
    
    # Build descriptive response
    if detected["luxury"] is True:
        response_parts.append("luxury")
    elif detected["luxury"] is False:
        response_parts.append("budget")
    
    if detected["fuel"]:
        response_parts.append(detected["fuel"])
    
    if detected["type"]:
        response_parts.append(detected["type"])
    
    if detected["brand"]:
        brand_part = f"from {detected['brand']}"
    else:
        brand_part = None
    
    if detected["price"]:
        price_part = f"in {detected['price'].replace('_', ' ')} range"
    else:
        price_part = None
    
    # Generate final response
    # Check if we have enough information (at least 1 attribute beyond just brand)
    non_brand_attrs = sum([1 for k, v in detected.items() if k != 'brand' and v is not None])
    
    if non_brand_attrs >= 2 or (detected["brand"] and non_brand_attrs >= 1):
        # We have good match criteria
        description = " ".join(response_parts) if response_parts else "cars"
        full_response = f"Found matches! Top {description}"
        if brand_part:
            full_response += f" {brand_part}"
        if price_part:
            full_response += f" {price_part}"
        full_response += ":"
        return full_response
    elif detected["brand"]:
        # Only brand detected (with maybe luxury inference)
        luxury_hint = ""
        if detected["luxury"] is True:
            luxury_hint = " (luxury category)"
        elif detected["luxury"] is False:
            luxury_hint = " (budget category)"
        return f"{detected['brand']} models available{luxury_hint}. Ask about type, fuel, or price!"
    elif detected["type"]:
        return f"{detected['type'].title()} options available. Specify brand, fuel, or price for better results!"
    elif detected["fuel"]:
        return f"{detected['fuel'].title()} vehicles available. Specify brand, type, or price for better results!"
    else:
        return "I understand car queries! Try: 'luxury electric sedan above 40 lakhs' or 'cheap Maruti hatchback under 10L'"

# Experiment 5 test (RUN THIS FIRST)
if __name__ == "__main__":
    print("="*60)
    print("ENHANCED NLP CHATBOT - COMPREHENSIVE TESTING")
    print("="*60)
    
    # Test cases from NLP Design Plan (comment requirements)
    TEST_CASES = [
        # Original test cases
        ("cheap maruti hatchback under 10 lakhs", "budget"),
        ("luxury BMW sedan above 50 lakhs", "luxury"),
        ("Tata Nexon EV", "Tata"),
        
        # New test cases from comment (Section 1 of design plan)
        ("I want a luxury sedan above 40 lakhs", "luxury sedan"),
        ("Looking for an electric hatchback by Tesla", "electric hatchback"),
        ("A cheap Maruti car under 10L", "budget"),
        ("Show me petrol SUVs under 15 lakhs", "petrol suv"),
        ("Budget friendly diesel sedan", "budget diesel sedan"),
        
        # Additional comprehensive tests
        ("Affordable electric car", "budget electric"),
        ("Premium Hyundai SUV above 20 lakhs", "luxury suv"),
        ("Give me EV options under 30 lakhs", "electric"),
    ]
    
    print("\nTEST RESULTS:\n")
    for i, (query, expected_keyword) in enumerate(TEST_CASES, 1):
        result = respond_to_user(query)
        print(f"Test {i}:")
        print(f"  Query:    {query}")
        print(f"  Response: {result}")
        print(f"  Expected: Should contain '{expected_keyword}'")
        print(f"  Status:   {'✅ PASS' if expected_keyword.lower() in result.lower() else '❌ FAIL'}")
        print()
    
    print("="*60)
    print("✅ All Experiment 5 test cases completed!")
    print("="*60)