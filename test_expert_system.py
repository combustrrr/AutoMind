#!/usr/bin/env python3
"""
Test Suite for Expert System
Validates all AI components
"""

from expert_system import (
    CarKnowledgeBase, BeliefState, InferenceEngine, ExpertSystem
)


def test_knowledge_base():
    """Test Knowledge Base component"""
    print("=" * 70)
    print("TEST 1: Knowledge Base")
    print("=" * 70)
    
    kb = CarKnowledgeBase()
    
    # Test: KB loaded cars
    assert len(kb.cars) > 0, "KB should load cars"
    print(f"✓ Loaded {len(kb.cars)} cars")
    
    # Test: Attributes identified
    assert 'brand' in kb.attributes, "Should have brand attribute"
    assert 'body_type' in kb.attributes, "Should have body_type attribute"
    print(f"✓ Identified {len(kb.attributes)} attributes")
    
    # Test: Get cars by attribute
    suvs = kb.get_cars_by_attribute('body_type', 'SUV')
    assert len(suvs) > 0, "Should find SUVs"
    print(f"✓ Found {len(suvs)} SUVs")
    
    print("\n✅ Knowledge Base tests PASSED\n")


def test_belief_state():
    """Test Belief State component"""
    print("=" * 70)
    print("TEST 2: Belief State Management")
    print("=" * 70)
    
    kb = CarKnowledgeBase()
    bs = BeliefState(kb.cars)
    
    # Test: Initial state
    initial_count = bs.get_possible_count()
    assert initial_count == len(kb.cars), "Should start with all cars possible"
    print(f"✓ Initial state: {initial_count} possible cars")
    
    # Test: Update belief
    bs.update_belief('body_type', 'SUV')
    after_update = bs.get_possible_count()
    assert after_update < initial_count, "Should narrow down after update"
    print(f"✓ After filtering for SUV: {after_update} possible cars")
    
    # Test: Confidence scores
    candidates = bs.get_top_candidates(n=3)
    assert len(candidates) > 0, "Should have candidates"
    assert candidates[0][1] > 0, "Top candidate should have positive confidence"
    print(f"✓ Top candidate confidence: {candidates[0][1]*100:.1f}%")
    
    # Test: Multiple updates
    bs.update_belief('fuel_type', 'Petrol')
    final_count = bs.get_possible_count()
    assert final_count <= after_update, "Should narrow down further"
    print(f"✓ After filtering for Petrol: {final_count} possible cars")
    
    print("\n✅ Belief State tests PASSED\n")


def test_inference_engine():
    """Test Inference Engine component"""
    print("=" * 70)
    print("TEST 3: Inference Engine")
    print("=" * 70)
    
    kb = CarKnowledgeBase()
    ie = InferenceEngine(kb)
    bs = BeliefState(kb.cars)
    
    # Test: Information gain calculation
    gain = ie.calculate_information_gain('brand', bs.possible_cars)
    assert gain >= 0, "Information gain should be non-negative"
    print(f"✓ Information gain for 'brand': {gain:.3f}")
    
    # Test: Question selection
    question = ie.select_next_question(bs)
    assert question is not None, "Should select a question"
    print(f"✓ Selected question: {question}")
    
    # Test: No duplicate questions
    question2 = ie.select_next_question(bs)
    assert question2 != question, "Should not repeat questions"
    print(f"✓ Next question: {question2}")
    
    # Test: Forward chaining
    bs.update_belief('price_range', 'under_10L')
    bs.update_belief('luxury', 'No')
    inferred = ie.forward_chain(bs)
    assert 'is_budget' in inferred, "Should infer budget status"
    assert inferred['is_budget'] == True, "Should infer as budget car"
    print(f"✓ Forward chaining inferred: {inferred}")
    
    print("\n✅ Inference Engine tests PASSED\n")


def test_expert_system():
    """Test complete Expert System"""
    print("=" * 70)
    print("TEST 4: Complete Expert System")
    print("=" * 70)
    
    es = ExpertSystem()
    
    # Test: Initialization
    assert len(es.kb.cars) > 0, "ES should have cars"
    assert es.belief_state.get_possible_count() > 0, "Should have possible cars"
    print(f"✓ Initialized with {len(es.kb.cars)} cars")
    
    # Test: Ask question
    result = es.ask_question()
    assert result is not None, "Should generate a question"
    attribute, values = result
    assert len(values) > 0, "Should have answer options"
    print(f"✓ Generated question about '{attribute}' with {len(values)} options")
    
    # Test: Process answer
    answer = values[0]
    inferred = es.process_answer(attribute, answer)
    assert isinstance(inferred, dict), "Should return inferred facts"
    print(f"✓ Processed answer, inferred: {inferred}")
    
    # Test: Status
    status = es.get_status()
    assert status['possible_cars'] > 0, "Should have possible cars"
    assert status['asked_questions'] == 1, "Should have asked 1 question"
    print(f"✓ Status: {status}")
    
    # Test: Recommendations
    candidates = es.get_top_candidates(n=3)
    assert len(candidates) > 0, "Should have recommendations"
    print(f"✓ Got {len(candidates)} recommendations")
    
    # Test: Reset
    es.reset()
    status_after_reset = es.get_status()
    assert status_after_reset['asked_questions'] == 0, "Should reset questions"
    assert status_after_reset['possible_cars'] == len(es.kb.cars), "Should reset cars"
    print(f"✓ Reset successful")
    
    print("\n✅ Expert System tests PASSED\n")


def test_multi_turn_reasoning():
    """Test multi-turn reasoning scenario"""
    print("=" * 70)
    print("TEST 5: Multi-Turn Reasoning Scenario")
    print("=" * 70)
    
    es = ExpertSystem()
    
    print(f"Initial: {es.belief_state.get_possible_count()} cars")
    
    # Turn 1: Ask about brand
    q1 = es.ask_question()
    if q1:
        attr, values = q1
        # Simulate answering "Toyota"
        if 'Toyota' in values:
            es.process_answer(attr, 'Toyota')
            count1 = es.belief_state.get_possible_count()
            print(f"✓ After Turn 1 ({attr}=Toyota): {count1} cars")
    
    # Turn 2: Ask next question
    q2 = es.ask_question()
    if q2:
        attr, values = q2
        # Answer with first option
        es.process_answer(attr, values[0])
        count2 = es.belief_state.get_possible_count()
        print(f"✓ After Turn 2 ({attr}={values[0]}): {count2} cars")
    
    # Turn 3: Ask next question
    q3 = es.ask_question()
    if q3:
        attr, values = q3
        es.process_answer(attr, values[0])
        count3 = es.belief_state.get_possible_count()
        print(f"✓ After Turn 3 ({attr}={values[0]}): {count3} cars")
    
    # Check convergence
    final_status = es.get_status()
    print(f"\n✓ Final state: {final_status['possible_cars']} cars remaining")
    print(f"✓ Total questions: {final_status['asked_questions']}")
    
    # Get recommendation
    recommendation = es.get_recommendation()
    if recommendation:
        car, confidence = recommendation
        print(f"✓ Top recommendation: {car['brand']} {car['model']} ({confidence*100:.1f}%)")
    
    print("\n✅ Multi-turn reasoning test PASSED\n")


def test_information_gain_ordering():
    """Test that questions are ordered by information gain"""
    print("=" * 70)
    print("TEST 6: Information Gain Ordering")
    print("=" * 70)
    
    es = ExpertSystem()
    ie = es.inference_engine
    bs = es.belief_state
    
    # Calculate gains for all attributes
    gains = {}
    for attr in es.kb.attributes.keys():
        gain = ie.calculate_information_gain(attr, bs.possible_cars)
        gains[attr] = gain
    
    print("Information gains:")
    for attr, gain in sorted(gains.items(), key=lambda x: x[1], reverse=True):
        print(f"  {attr:15} = {gain:.4f}")
    
    # First question should be highest gain
    first_q = es.ask_question()
    if first_q:
        first_attr, _ = first_q
        max_gain_attr = max(gains.items(), key=lambda x: x[1])[0]
        assert first_attr == max_gain_attr, f"Should ask about highest gain attribute"
        print(f"\n✓ Correctly selected '{first_attr}' (highest information gain)")
    
    print("\n✅ Information gain ordering test PASSED\n")


def run_all_tests():
    """Run all test suites"""
    print("\n" + "=" * 70)
    print("  EXPERT SYSTEM TEST SUITE")
    print("=" * 70)
    print("\nTesting all AI components:\n")
    
    try:
        test_knowledge_base()
        test_belief_state()
        test_inference_engine()
        test_expert_system()
        test_multi_turn_reasoning()
        test_information_gain_ordering()
        
        print("=" * 70)
        print("  ✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nExpert System demonstrates:")
        print("  ✓ Knowledge Representation")
        print("  ✓ Belief State Management")
        print("  ✓ Forward Chaining Inference")
        print("  ✓ Information Gain Calculation")
        print("  ✓ Optimal Question Selection")
        print("  ✓ Multi-turn Reasoning")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
