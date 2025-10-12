#!/usr/bin/env python3
"""
Interactive CLI for Advanced Expert System
Allows selection of different reasoning modes
"""

from expert_system_advanced import AdvancedExpertSystem, FuzzySet
import sys


def print_banner():
    print("\n" + "="*70)
    print(" "*15 + "🧠 ADVANCED EXPERT SYSTEM 🧠")
    print("="*70)
    print("\nDemonstrating Classical and Advanced AI Techniques:")
    print("  ✓ Forward Chaining (Data-Driven)")
    print("  ✓ Backward Chaining (Goal-Driven)")
    print("  ✓ Fuzzy Logic (Uncertainty Handling)")
    print("  ✓ A* Search (Optimal Path Finding)")
    print("  ✓ Case-Based Reasoning (Learning from Experience)")
    print("  ✓ Frame Inheritance (Knowledge Representation)")
    print("="*70 + "\n")


def select_mode():
    print("\n📋 SELECT REASONING MODE:")
    print("  1. Forward Chaining + Information Gain (Classic)")
    print("  2. Backward Chaining (Goal-Driven)")
    print("  3. A* Search (Optimal Questioning)")
    print("  4. Fuzzy Logic Mode (Handle Uncertainty)")
    print("  5. Case-Based Reasoning (Learn from Past)")
    print("  6. Gini Impurity (Alternative to IG)")
    
    while True:
        try:
            choice = input("\nEnter mode (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            print("❌ Invalid choice. Please enter 1-6.")
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Exiting...")
            sys.exit(0)


def run_forward_chaining_mode(es: AdvancedExpertSystem):
    """Classic forward chaining with information gain"""
    print("\n🔄 MODE: Forward Chaining + Information Gain")
    print("="*70)
    
    es.metrics['reasoning_mode'] = 'forward_chaining'
    
    while True:
        matching = es.get_matching_cars()
        
        if len(matching) == 0:
            print("\n❌ No matching cars found!")
            break
        elif len(matching) == 1:
            car = matching[0]
            print(f"\n✅ FOUND: {car['brand']} {car['model']}")
            print(f"   Confidence: 100%")
            print(f"   Questions asked: {len(es.asked_questions)}")
            
            # Save case
            es.save_case(es.known_attributes, car, len(es.asked_questions))
            break
        
        # Calculate IG for all attributes
        print(f"\n📊 {len(matching)} cars remaining")
        print("   Calculating information gain...")
        
        best_attr = None
        best_ig = -1
        
        for attr in es.attributes.keys():
            if attr not in es.known_attributes:
                ig = es.calculate_information_gain(attr)
                if ig > best_ig:
                    best_ig = ig
                    best_attr = attr
        
        if not best_attr:
            print("\n⚠️  Cannot narrow down further")
            break
        
        print(f"   Best attribute: {best_attr} (IG: {best_ig:.3f} bits)")
        
        # Ask question
        values = sorted(list(es.attributes[best_attr]))
        print(f"\n❓ What is the {best_attr}?")
        print(f"   Options: {', '.join(values)}")
        
        answer = input("   Your answer: ").strip()
        
        if answer in values:
            es.known_attributes[best_attr] = answer
            es.asked_questions.append(best_attr)
            
            # Apply forward chaining
            inferred = es.forward_chaining()
            if inferred:
                print(f"   🔍 Forward chaining inferred: {', '.join([f'{k}={v}' for k,v in inferred])}")
        else:
            print(f"   ⚠️  Invalid answer. Choose from: {', '.join(values)}")


def run_backward_chaining_mode(es: AdvancedExpertSystem):
    """Backward chaining: start with hypothesis"""
    print("\n🎯 MODE: Backward Chaining (Goal-Driven)")
    print("="*70)
    
    es.metrics['reasoning_mode'] = 'backward_chaining'
    
    # Select a hypothesis car
    import random
    hypothesis = random.choice(es.cars)
    
    print(f"\n💡 Hypothesis: {hypothesis['brand']} {hypothesis['model']}")
    print("   Working backward to verify...")
    
    # Get attributes to verify
    to_verify = es.backward_chaining(hypothesis)
    
    print(f"   Need to verify: {', '.join(to_verify)}")
    
    for attr in to_verify:
        values = sorted(list(es.attributes[attr]))
        print(f"\n❓ What is the {attr}?")
        print(f"   Options: {', '.join(values)}")
        
        answer = input("   Your answer: ").strip()
        
        if answer in values:
            es.known_attributes[attr] = answer
            es.asked_questions.append(attr)
            
            # Check if matches hypothesis
            if answer != hypothesis.get(attr):
                print(f"   ❌ Hypothesis refuted! ({attr} should be {hypothesis.get(attr)})")
                print("\n   Switching to forward chaining...")
                run_forward_chaining_mode(es)
                return
            else:
                print(f"   ✅ Confirmed! Matches hypothesis")
        else:
            print(f"   ⚠️  Invalid answer")
    
    print(f"\n✅ HYPOTHESIS CONFIRMED: {hypothesis['brand']} {hypothesis['model']}")
    print(f"   Questions asked: {len(es.asked_questions)}")


def run_astar_mode(es: AdvancedExpertSystem):
    """A* search for optimal question sequence"""
    print("\n🌟 MODE: A* Search (Optimal Path)")
    print("="*70)
    
    es.metrics['reasoning_mode'] = 'astar_search'
    
    print("\n🔍 Computing optimal question sequence using A* search...")
    
    while True:
        matching = es.get_matching_cars()
        
        if len(matching) <= 1:
            if matching:
                car = matching[0]
                print(f"\n✅ FOUND: {car['brand']} {car['model']}")
                print(f"   Questions asked: {len(es.asked_questions)} (optimal)")
            break
        
        # Use A* to get next question
        result = es.ask_optimal_question_astar()
        
        if not result:
            break
        
        attr, values = result
        
        print(f"\n❓ What is the {attr}?")
        print(f"   Options: {', '.join(values)}")
        print(f"   [{len(matching)} cars remaining]")
        
        answer = input("   Your answer: ").strip()
        
        if answer in values:
            es.known_attributes[attr] = answer
            es.asked_questions.append(attr)
        else:
            print(f"   ⚠️  Invalid answer")


def run_fuzzy_mode(es: AdvancedExpertSystem):
    """Fuzzy logic mode with linguistic terms"""
    print("\n🌫️  MODE: Fuzzy Logic (Handle Uncertainty)")
    print("="*70)
    print("\nYou can use fuzzy terms like:")
    print("  - 'somewhat', 'slightly', 'very', 'extremely'")
    print("  - 'no', 'barely', 'quite', 'definitely', 'yes'")
    
    es.metrics['reasoning_mode'] = 'fuzzy_logic'
    es.fuzzy_mode = True
    
    # Use forward chaining but accept fuzzy answers
    while True:
        matching = es.get_matching_cars()
        
        if len(matching) <= 1:
            car, conf = es.get_recommendation()
            if car:
                print(f"\n✅ RECOMMENDATION: {car['brand']} {car['model']}")
                print(f"   Confidence: {conf*100:.1f}%")
            break
        
        # Get best question
        best_attr = None
        best_ig = -1
        
        for attr in es.attributes.keys():
            if attr not in es.known_attributes:
                ig = es.calculate_information_gain(attr)
                if ig > best_ig:
                    best_ig = ig
                    best_attr = attr
        
        if not best_attr:
            break
        
        values = sorted(list(es.attributes[best_attr]))
        print(f"\n❓ What about {best_attr}?")
        print(f"   Options: {', '.join(values)}")
        print("   (Use fuzzy terms for partial matches)")
        
        answer = input("   Your answer: ").strip()
        
        # Parse fuzzy answer
        category, confidence = FuzzySet.parse_fuzzy_term(answer)
        
        print(f"   🔍 Parsed as: {category} (confidence: {confidence:.2f})")
        
        # Check if it's a crisp answer
        if answer in values:
            es.known_attributes[best_attr] = answer
            es.asked_questions.append(best_attr)
        else:
            # Process as fuzzy
            es.process_fuzzy_answer(best_attr, answer)
            es.asked_questions.append(best_attr)


def run_cbr_mode(es: AdvancedExpertSystem):
    """Case-based reasoning mode"""
    print("\n📚 MODE: Case-Based Reasoning")
    print("="*70)
    
    es.metrics['reasoning_mode'] = 'cbr'
    
    print(f"\n📖 Cases in memory: {len(es.case_base.cases)}")
    
    if es.case_base.cases:
        print("\n🔍 Checking for similar past cases...")
        
        # Try to retrieve similar cases
        similar = es.case_base.retrieve_similar(es.known_attributes, top_k=3)
        
        if similar:
            print(f"\n✨ Found {len(similar)} similar case(s):")
            for i, case in enumerate(similar, 1):
                sol = case['solution']
                perf = case['performance']
                print(f"\n   {i}. {sol['brand']} {sol['model']}")
                print(f"      Solved in {perf['questions_asked']} questions")
                print(f"      Problem: {case['problem']}")
            
            print("\n💡 Using similar case as guide...")
        else:
            print("\n   No similar cases found. Using forward chaining...")
    else:
        print("\n   No cases yet. This will be the first case!")
    
    # Fall back to forward chaining
    run_forward_chaining_mode(es)


def run_gini_mode(es: AdvancedExpertSystem):
    """Gini impurity instead of information gain"""
    print("\n📊 MODE: Gini Impurity (Alternative to Information Gain)")
    print("="*70)
    
    es.metrics['reasoning_mode'] = 'gini_impurity'
    
    while True:
        matching = es.get_matching_cars()
        
        if len(matching) <= 1:
            if matching:
                car = matching[0]
                print(f"\n✅ FOUND: {car['brand']} {car['model']}")
                print(f"   Questions asked: {len(es.asked_questions)}")
            break
        
        # Calculate Gini for all attributes
        print(f"\n📊 {len(matching)} cars remaining")
        print("   Calculating Gini impurity...")
        
        best_attr = None
        best_gini = -1
        
        for attr in es.attributes.keys():
            if attr not in es.known_attributes:
                gini = es.calculate_gini_impurity(attr)
                if gini > best_gini:
                    best_gini = gini
                    best_attr = attr
        
        if not best_attr:
            break
        
        print(f"   Best attribute: {best_attr} (Gini gain: {best_gini:.3f})")
        
        values = sorted(list(es.attributes[best_attr]))
        print(f"\n❓ What is the {best_attr}?")
        print(f"   Options: {', '.join(values)}")
        
        answer = input("   Your answer: ").strip()
        
        if answer in values:
            es.known_attributes[best_attr] = answer
            es.asked_questions.append(best_attr)
        else:
            print(f"   ⚠️  Invalid answer")


def main():
    print_banner()
    
    # Initialize expert system
    es = AdvancedExpertSystem()
    
    # Select mode
    mode = select_mode()
    
    # Run selected mode
    if mode == 1:
        run_forward_chaining_mode(es)
    elif mode == 2:
        run_backward_chaining_mode(es)
    elif mode == 3:
        run_astar_mode(es)
    elif mode == 4:
        run_fuzzy_mode(es)
    elif mode == 5:
        run_cbr_mode(es)
    elif mode == 6:
        run_gini_mode(es)
    
    # Show final metrics
    print("\n" + "="*70)
    print("📊 PERFORMANCE METRICS:")
    print("="*70)
    metrics = es.get_performance_metrics()
    for key, value in metrics.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*70)
    print("Thank you for using the Advanced Expert System!")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
