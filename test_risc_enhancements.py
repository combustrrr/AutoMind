#!/usr/bin/env python3
"""
Test suite for RISC AI Enhancements
Tests the three micro-enhancements:
1. Smart Clarification
2. Preference Learning
3. Conversation Repair
"""

from nlp_engine import (
    extract_features,
    calculate_confidence,
    get_preferences,
    reset_preferences,
    handle_confusion,
    clear_context,
    suggest_clarification
)


def test_smart_clarification():
    """Test smart clarification enhancement."""
    print("\n" + "=" * 70)
    print("TEST 1: SMART CLARIFICATION")
    print("=" * 70)
    
    clear_context()
    reset_preferences()
    
    # Test low confidence query
    print("\n✓ Testing low confidence query (should trigger clarification):")
    features = extract_features("a car")
    confidence = calculate_confidence(features)
    clarification = suggest_clarification(features, confidence)
    
    assert confidence < 0.3, f"Expected confidence < 0.3, got {confidence}"
    assert clarification is not None, "Expected clarification message"
    print(f"  Confidence: {confidence:.1%} ✓")
    print(f"  Clarification: {clarification} ✓")
    
    # Test high confidence query
    print("\n✓ Testing high confidence query (should NOT trigger clarification):")
    features = extract_features("Toyota SUV under 20 lakhs")
    confidence = calculate_confidence(features)
    clarification = suggest_clarification(features, confidence)
    
    assert confidence >= 0.3, f"Expected confidence >= 0.3, got {confidence}"
    assert clarification is None, "Expected no clarification message"
    print(f"  Confidence: {confidence:.1%} ✓")
    print(f"  No clarification needed ✓")
    
    print("\n✅ Smart Clarification tests passed!")


def test_preference_learning():
    """Test preference learning enhancement."""
    print("\n" + "=" * 70)
    print("TEST 2: PREFERENCE LEARNING")
    print("=" * 70)
    
    clear_context()
    reset_preferences()
    
    # Initially no preferences
    print("\n✓ Testing initial state:")
    prefs = get_preferences()
    assert prefs['prefers_electric'] is None
    assert prefs['prefers_suv'] is None
    assert len(prefs['preferred_brands']) == 0
    print("  All preferences are None/empty ✓")
    
    # Learn electric preference
    print("\n✓ Testing electric preference learning:")
    extract_features("electric car")
    prefs = get_preferences()
    assert prefs['prefers_electric'] is True
    print(f"  Learned: prefers_electric = {prefs['prefers_electric']} ✓")
    
    # Learn SUV preference
    print("\n✓ Testing SUV preference learning:")
    extract_features("Toyota SUV")
    prefs = get_preferences()
    assert prefs['prefers_suv'] is True
    assert 'Toyota' in prefs['preferred_brands']
    print(f"  Learned: prefers_suv = {prefs['prefers_suv']} ✓")
    print(f"  Learned: brands = {prefs['preferred_brands']} ✓")
    
    # Learn luxury preference
    print("\n✓ Testing luxury preference learning:")
    extract_features("luxury BMW sedan above 50 lakhs")
    prefs = get_preferences()
    assert prefs['price_sensitivity'] == 'luxury'
    assert 'Bmw' in prefs['preferred_brands'] or 'BMW' in prefs['preferred_brands']
    # Note: prefers_suv stays True (doesn't flip-flop based on single query)
    print(f"  Learned: price_sensitivity = {prefs['price_sensitivity']} ✓")
    print(f"  Brands: {prefs['preferred_brands']} ✓")
    
    # Test budget preference
    print("\n✓ Testing budget preference learning:")
    reset_preferences()
    extract_features("cheap Maruti hatchback under 10L")
    prefs = get_preferences()
    assert prefs['price_sensitivity'] == 'budget'
    assert prefs['prefers_suv'] is False  # hatchback, not SUV
    print(f"  Learned: price_sensitivity = {prefs['price_sensitivity']} ✓")
    print(f"  Learned: prefers_suv = {prefs['prefers_suv']} ✓")
    
    print("\n✅ Preference Learning tests passed!")


def test_conversation_repair():
    """Test conversation repair enhancement."""
    print("\n" + "=" * 70)
    print("TEST 3: CONVERSATION REPAIR")
    print("=" * 70)
    
    clear_context()
    reset_preferences()
    
    # Test confusion handler
    print("\n✓ Testing confusion handler:")
    message = handle_confusion()
    assert "brand name" in message.lower() or "car type" in message.lower()
    assert len(message) > 20  # Should be a helpful message
    print(f"  Message: {message} ✓")
    
    # Test vague query detection
    print("\n✓ Testing vague query detection:")
    features = extract_features("something good")
    assert features['brand'] is None
    assert features['type'] is None
    print("  Vague query detected and handled ✓")
    
    # Test suggestion generation
    print("\n✓ Testing suggestion generation for missing features:")
    features = {'brand': None, 'type': None, 'fuel': 'electric', 
                'price_range': None, 'luxury': None}
    confidence = calculate_confidence(features)
    suggestion = suggest_clarification(features, confidence)
    assert suggestion is not None
    assert 'brand' in suggestion.lower() or 'type' in suggestion.lower()
    print(f"  Suggestion: {suggestion} ✓")
    
    print("\n✅ Conversation Repair tests passed!")


def test_confidence_calculation():
    """Test confidence score calculation."""
    print("\n" + "=" * 70)
    print("TEST 4: CONFIDENCE CALCULATION")
    print("=" * 70)
    
    # Test full features (100% confidence)
    print("\n✓ Testing full features (100% confidence):")
    features = {
        'brand': 'Toyota',
        'type': 'suv',
        'fuel': 'petrol',
        'price_range': 'under_20L',
        'luxury': False
    }
    confidence = calculate_confidence(features)
    assert confidence == 1.0, f"Expected 1.0, got {confidence}"
    print(f"  Confidence: {confidence:.1%} ✓")
    
    # Test partial features
    print("\n✓ Testing partial features (70% confidence):")
    features = {
        'brand': 'Toyota',
        'type': 'suv',
        'fuel': None,
        'price_range': 'under_20L',
        'luxury': None
    }
    confidence = calculate_confidence(features)
    assert confidence == 0.7, f"Expected 0.7, got {confidence}"
    print(f"  Confidence: {confidence:.1%} ✓")
    
    # Test no features (0% confidence)
    print("\n✓ Testing no features (0% confidence):")
    features = {
        'brand': None,
        'type': None,
        'fuel': None,
        'price_range': None,
        'luxury': None
    }
    confidence = calculate_confidence(features)
    assert confidence == 0.0, f"Expected 0.0, got {confidence}"
    print(f"  Confidence: {confidence:.1%} ✓")
    
    print("\n✅ Confidence Calculation tests passed!")


def run_all_tests():
    """Run all RISC AI enhancement tests."""
    print("\n" + "=" * 70)
    print("🚀 RISC AI ENHANCEMENTS - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    try:
        test_smart_clarification()
        test_preference_learning()
        test_conversation_repair()
        test_confidence_calculation()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nRISC AI Enhancements are working correctly:")
        print("  ✓ Smart Clarification (CLARIFY_WHEN_CONFIDENT = 0.3)")
        print("  ✓ Preference Learning (USER_PREFERENCES tracking)")
        print("  ✓ Conversation Repair (handle_confusion)")
        print("=" * 70)
        
        return True
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
