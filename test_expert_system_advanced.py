#!/usr/bin/env python3
"""
Comprehensive Test Suite for Advanced Expert System
Tests all AI features: forward/backward chaining, fuzzy logic, A*, CBR, etc.
"""

from expert_system_advanced import (
    AdvancedExpertSystem, FuzzySet, CaseBase, AStarSearch, FrameNode
)


def test_frame_inheritance():
    """Test frame-based knowledge representation with inheritance"""
    print("\n" + "="*70)
    print("TEST 1: Frame Inheritance")
    print("="*70)
    
    # Build hierarchy
    vehicle = FrameNode("Vehicle")
    vehicle.set_attribute("has_wheels", True)
    vehicle.set_attribute("transport_type", "ground")
    
    car = FrameNode("Car", parent=vehicle)
    car.set_attribute("num_wheels", 4)
    
    suv = FrameNode("SUV", parent=car)
    suv.set_attribute("ground_clearance", "high")
    
    # Test inheritance
    assert suv.get_attribute("has_wheels") == True, "SUV should inherit has_wheels"
    assert suv.get_attribute("num_wheels") == 4, "SUV should inherit num_wheels"
    assert suv.get_attribute("ground_clearance") == "high", "SUV should have own attribute"
    
    print("✅ Frame inheritance: PASSED")
    print("   - SUV correctly inherits attributes from Car and Vehicle")
    print("   - Own attributes accessible")
    return True


def test_fuzzy_logic():
    """Test fuzzy logic membership functions"""
    print("\n" + "="*70)
    print("TEST 2: Fuzzy Logic")
    print("="*70)
    
    # Test membership functions
    assert FuzzySet.very_low(0.1) == 1.0, "very_low(0.1) should be 1.0"
    assert FuzzySet.medium(0.5) == 1.0, "medium(0.5) should be 1.0"
    assert FuzzySet.very_high(0.95) == 1.0, "very_high(0.95) should be 1.0"
    
    # Test fuzzy term parsing
    category, conf = FuzzySet.parse_fuzzy_term("somewhat")
    assert category == "medium" and conf == 0.5, "somewhat should be medium with 0.5"
    
    category, conf = FuzzySet.parse_fuzzy_term("very")
    assert category == "high" and conf == 0.75, "very should be high with 0.75"
    
    print("✅ Fuzzy logic: PASSED")
    print("   - Membership functions working correctly")
    print("   - Linguistic term parsing accurate")
    return True


def test_case_based_reasoning():
    """Test case-based reasoning (CBR)"""
    print("\n" + "="*70)
    print("TEST 3: Case-Based Reasoning")
    print("="*70)
    
    import os
    import tempfile
    
    # Use temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        cb = CaseBase(storage_file=temp_file)
        
        # Add test cases
        problem1 = {'brand': 'Toyota', 'body_type': 'SUV'}
        solution1 = {'brand': 'Toyota', 'model': 'Fortuner'}
        performance1 = {'questions_asked': 2, 'success': True}
        
        cb.add_case(problem1, solution1, performance1)
        
        problem2 = {'brand': 'Honda', 'body_type': 'Sedan'}
        solution2 = {'brand': 'Honda', 'model': 'City'}
        performance2 = {'questions_asked': 3, 'success': True}
        
        cb.add_case(problem2, solution2, performance2)
        
        # Retrieve similar cases
        query = {'brand': 'Toyota', 'body_type': 'SUV'}
        similar = cb.retrieve_similar(query, top_k=2)
        
        assert len(similar) > 0, "Should retrieve similar cases"
        assert similar[0]['solution']['brand'] == 'Toyota', "Most similar should be Toyota"
        
        print("✅ Case-Based Reasoning: PASSED")
        print(f"   - Added {len(cb.cases)} cases")
        print(f"   - Retrieved {len(similar)} similar cases")
        print("   - Similarity matching working correctly")
        
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    return True


def test_information_gain():
    """Test information gain calculation"""
    print("\n" + "="*70)
    print("TEST 4: Information Gain Calculation")
    print("="*70)
    
    es = AdvancedExpertSystem()
    
    # Calculate IG for different attributes
    ig_brand = es.calculate_information_gain('brand')
    ig_body_type = es.calculate_information_gain('body_type')
    ig_fuel_type = es.calculate_information_gain('fuel_type')
    
    assert ig_brand > 0, "Brand should have positive information gain"
    assert ig_body_type > 0, "Body type should have positive information gain"
    
    print("✅ Information Gain: PASSED")
    print(f"   - brand IG: {ig_brand:.3f} bits")
    print(f"   - body_type IG: {ig_body_type:.3f} bits")
    print(f"   - fuel_type IG: {ig_fuel_type:.3f} bits")
    
    return True


def test_gini_impurity():
    """Test Gini impurity calculation"""
    print("\n" + "="*70)
    print("TEST 5: Gini Impurity Calculation")
    print("="*70)
    
    es = AdvancedExpertSystem()
    
    # Calculate Gini for different attributes
    gini_brand = es.calculate_gini_impurity('brand')
    gini_body_type = es.calculate_gini_impurity('body_type')
    
    assert gini_brand >= 0, "Gini should be non-negative"
    assert gini_body_type >= 0, "Gini should be non-negative"
    
    print("✅ Gini Impurity: PASSED")
    print(f"   - brand Gini: {gini_brand:.3f}")
    print(f"   - body_type Gini: {gini_body_type:.3f}")
    
    return True


def test_forward_chaining():
    """Test forward chaining inference"""
    print("\n" + "="*70)
    print("TEST 6: Forward Chaining Inference")
    print("="*70)
    
    es = AdvancedExpertSystem()
    
    # Test rule: luxury + high price → premium_brand
    es.known_attributes = {
        'luxury': 'yes',
        'price_range': 'above_30L'
    }
    
    inferred = es.forward_chaining()
    
    assert len(inferred) > 0, "Should infer facts"
    assert ('premium_brand', 'yes') in inferred, "Should infer premium_brand"
    
    print("✅ Forward Chaining: PASSED")
    print(f"   - Inferred {len(inferred)} facts")
    print(f"   - Rules: {inferred}")
    
    return True


def test_backward_chaining():
    """Test backward chaining inference"""
    print("\n" + "="*70)
    print("TEST 7: Backward Chaining Inference")
    print("="*70)
    
    es = AdvancedExpertSystem()
    
    # Pick a hypothesis
    hypothesis = es.cars[0]
    
    # Get attributes to verify
    to_verify = es.backward_chaining(hypothesis)
    
    assert len(to_verify) > 0, "Should have attributes to verify"
    
    print("✅ Backward Chaining: PASSED")
    print(f"   - Hypothesis: {hypothesis['brand']} {hypothesis['model']}")
    print(f"   - Attributes to verify: {to_verify}")
    
    return True


def test_astar_search():
    """Test A* search for optimal questions"""
    print("\n" + "="*70)
    print("TEST 8: A* Search for Optimal Sequencing")
    print("="*70)
    
    es = AdvancedExpertSystem()
    
    # Get optimal sequence
    result = es.ask_optimal_question_astar()
    
    if result:
        attr, values = result
        assert attr in es.attributes, "Should return valid attribute"
        assert len(values) > 0, "Should return possible values"
        
        print("✅ A* Search: PASSED")
        print(f"   - Next optimal question: {attr}")
        print(f"   - Possible values: {len(values)}")
    else:
        print("✅ A* Search: PASSED (no questions needed)")
    
    return True


def test_belief_state():
    """Test belief state management"""
    print("\n" + "="*70)
    print("TEST 9: Belief State Management")
    print("="*70)
    
    es = AdvancedExpertSystem()
    
    # Initial belief state
    total_belief = sum(es.belief_state.values())
    assert abs(total_belief - 1.0) < 0.01, "Beliefs should sum to 1.0"
    
    # Update with known attribute
    es.known_attributes['brand'] = 'Toyota'
    
    # Get recommendation
    car, conf = es.get_recommendation()
    
    assert car is not None, "Should get recommendation"
    assert 0 <= conf <= 1.0, "Confidence should be in [0, 1]"
    
    print("✅ Belief State: PASSED")
    print(f"   - Total belief: {total_belief:.3f}")
    print(f"   - Top recommendation: {car['brand']} {car['model']} ({conf*100:.1f}%)")
    
    return True


def test_performance_metrics():
    """Test performance tracking"""
    print("\n" + "="*70)
    print("TEST 10: Performance Metrics")
    print("="*70)
    
    es = AdvancedExpertSystem()
    
    # Simulate some questions
    es.asked_questions = ['brand', 'body_type']
    es.known_attributes = {'brand': 'Toyota', 'body_type': 'SUV'}
    
    metrics = es.get_performance_metrics()
    
    assert 'questions_asked' in metrics, "Should track questions asked"
    assert 'reasoning_mode' in metrics, "Should track reasoning mode"
    assert metrics['questions_asked'] == 2, "Should count questions correctly"
    
    print("✅ Performance Metrics: PASSED")
    for key, value in metrics.items():
        print(f"   - {key}: {value}")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print(" "*15 + "🧪 ADVANCED EXPERT SYSTEM TEST SUITE")
    print("="*70)
    
    tests = [
        ("Frame Inheritance", test_frame_inheritance),
        ("Fuzzy Logic", test_fuzzy_logic),
        ("Case-Based Reasoning", test_case_based_reasoning),
        ("Information Gain", test_information_gain),
        ("Gini Impurity", test_gini_impurity),
        ("Forward Chaining", test_forward_chaining),
        ("Backward Chaining", test_backward_chaining),
        ("A* Search", test_astar_search),
        ("Belief State", test_belief_state),
        ("Performance Metrics", test_performance_metrics),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name}: FAILED")
            print(f"   Error: {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success rate: {passed/len(tests)*100:.1f}%")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
