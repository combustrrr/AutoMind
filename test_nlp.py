#!/usr/bin/env python3
"""
Test script for NLP Engine
Tests feature extraction with 10 sample inputs
"""

from nlp_engine import extract_features

def test_nlp_engine():
    """Run comprehensive tests on the NLP engine."""
    
    # 10 diverse test cases
    test_cases = [
        {
            "input": "A Toyota SUV under 20 lakhs",
            "expected": {
                "brand": "Toyota",
                "type": "suv",
                "price_range": "under_20L"
            }
        },
        {
            "input": "Luxury BMW sedan above 50 lakhs",
            "expected": {
                "brand": "BMW",
                "type": "sedan",
                "luxury": True,
                "price_range": "above_30L"
            }
        },
        {
            "input": "cheap Maruti hatchback under 10L",
            "expected": {
                "brand": "Maruti Suzuki",
                "type": "hatchback",
                "luxury": False,
                "price_range": "under_10L"
            }
        },
        {
            "input": "Looking for an electric hatchback by Tesla",
            "expected": {
                "brand": "Tesla",
                "type": "hatchback",
                "fuel": "electric"
            }
        },
        {
            "input": "I want a luxury sedan above 40 lakhs",
            "expected": {
                "type": "sedan",
                "luxury": True,
                "price_range": "above_30L"
            }
        },
        {
            "input": "Show me petrol SUVs under 15 lakhs",
            "expected": {
                "type": "suv",
                "fuel": "petrol",
                "price_range": "10-20L"
            }
        },
        {
            "input": "Budget friendly diesel sedan from Hyundai",
            "expected": {
                "brand": "Hyundai",
                "type": "sedan",
                "fuel": "diesel",
                "luxury": False
            }
        },
        {
            "input": "A compact electric car by Hyundai under 18L",
            "expected": {
                "brand": "Hyundai",
                "type": "hatchback",
                "fuel": "electric",
                "price_range": "10-20L"
            }
        },
        {
            "input": "not electric, petrol crossover",
            "expected": {
                "type": "suv",
                "fuel": "petrol"
            }
        },
        {
            "input": "Tayota Fortuner around 30 lakhs",  # Typo test
            "expected": {
                "brand": "Toyota",
                "type": "suv",
                "price_range": "20-30L"
            }
        }
    ]
    
    print("=" * 80)
    print(" " * 25 + "NLP ENGINE TEST SUITE")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"  Input: '{test_case['input']}'")
        
        # Extract features
        result = extract_features(test_case['input'])
        
        # Check expectations
        print(f"  Output: {result}")
        
        # Validate against expected values
        test_passed = True
        for key, expected_value in test_case['expected'].items():
            if result.get(key) != expected_value:
                print(f"  ❌ MISMATCH: Expected {key}='{expected_value}', got '{result.get(key)}'")
                test_passed = False
        
        if test_passed:
            print(f"  ✅ PASSED")
            passed += 1
        else:
            print(f"  ❌ FAILED")
            failed += 1
        
        print("-" * 80)
    
    print()
    print("=" * 80)
    print(f"SUMMARY: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    return passed, failed


def demonstrate_features():
    """Demonstrate all supported features."""
    
    print("\n" + "=" * 80)
    print(" " * 25 + "FEATURE DEMONSTRATION")
    print("=" * 80)
    print()
    
    print("📋 SUPPORTED FEATURES:")
    print()
    
    demos = [
        ("Brand Detection", "Toyota Fortuner"),
        ("Body Type Detection", "I want an SUV"),
        ("Fuel Type Detection", "Electric vehicle please"),
        ("Price Range Detection", "Under 15 lakhs"),
        ("Luxury Detection", "Premium sedan"),
        ("Compound Query", "A luxury electric sedan by Tesla above 50 lakhs"),
        ("Fuzzy Matching", "Tayota car"),  # Typo
        ("Synonym Support", "Crossover vehicle with gasoline"),
        ("Negation Handling", "Not diesel, petrol car"),
        ("Budget Keywords", "Cheap and affordable hatchback")
    ]
    
    for feature, example in demos:
        print(f"🔹 {feature}:")
        print(f"   Input: '{example}'")
        result = extract_features(example)
        print(f"   Result: {result}")
        print()


if __name__ == "__main__":
    # Run tests
    passed, failed = test_nlp_engine()
    
    # Show feature demonstration
    demonstrate_features()
    
    # Exit with appropriate code
    exit(0 if failed == 0 else 1)
