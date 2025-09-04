import re
import json

# Load YOUR pattern database (from Day 1)
with open("src/keywords.json") as f:
    PATTERNS = json.load(f)

def respond_to_user(input_text: str) -> str:
    """Rule-based chatbot for Indian car queries (Experiment 5)"""
    input_text = input_text.lower()
    detected = {"brand": None, "type": None, "price": None}
    
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
    
    # 2. BODY TYPE DETECTION (From YOUR body_types)
    for body_type in PATTERNS["body_types"]:
        if re.search(rf"\b{body_type}\b", input_text):
            detected["type"] = body_type
    
    # 3. PRICE DETECTION (Using YOUR price bins)
    price_match = re.search(r'(under|below) (\d+)[\s,]*(lakhs?|lacs?)', input_text)
    above_match = re.search(r'(above|over) (\d+)[\s,]*(lakhs?|lacs?)', input_text)
    
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
    
    # 4. GENERATE RESPONSE (Using YOUR dataset context)
    if detected["brand"] and detected["type"] and detected["price"]:
        price_formatted = detected['price'].replace('_', ' ')
        return f"Found matches! Top {detected['type']} from {detected['brand']} in {price_formatted} range:"
    elif detected["brand"]:
        return f"{detected['brand']} models available. Ask about type or price!"
    else:
        return "I understand car queries! Try: 'Maruti SUV under 10L'"

# Experiment 5 test (RUN THIS FIRST)
if __name__ == "__main__":
    print(respond_to_user("cheap maruti hatchback under 10 lakhs"))
    # Output: "Found matches! Top hatchback from Maruti under under 10l:"
    
    # Add to chatbot.py for Experiment 5 proof
    TEST_CASES = [
        ("luxury BMW sedan above 50 lakhs", "Found matches! Top sedan from Bmw under above 30l:"),
        ("Tata Nexon EV", "Tata models available. Ask about type or price!"),  # Edge case
    ]

    for inp, expected in TEST_CASES:
        result = respond_to_user(inp)
        print(f"Input: {inp}")
        print(f"Output: {result}")
        print(f"Expected: {expected}")
        print("---")
    print("✅ All Experiment 5 test cases completed!")