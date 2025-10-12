#!/usr/bin/env python3
"""
Interactive Expert System CLI for Car Recommendation
AI-powered car guessing game using expert system techniques
"""

from expert_system import ExpertSystem
import sys


def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 70)
    print("  🚗 CAR EXPERT SYSTEM - AI Reasoning Demo 🚗")
    print("=" * 70)
    print("\n  This is an AI Expert System that demonstrates:")
    print("    • Knowledge Base (facts about 50 cars)")
    print("    • Inference Engine (forward chaining)")
    print("    • Information Gain (optimal question selection)")
    print("    • Belief State (probabilistic reasoning)")
    print("    • Rule-Based Reasoning (logical rules)")
    print("\n  I'll ask you questions to guess which car you're thinking of!")
    print("=" * 70)


def display_status(es: ExpertSystem):
    """Display current reasoning status"""
    status = es.get_status()
    print(f"\n📊 Status:")
    print(f"   Possible cars remaining: {status['possible_cars']}")
    print(f"   Questions asked: {status['asked_questions']}")
    if status['known_attributes']:
        print(f"   Known attributes: {status['known_attributes']}")


def ask_user_question(attribute: str, values: list) -> str:
    """Ask user a question and get answer"""
    print(f"\n❓ What is the {attribute.replace('_', ' ')}?")
    print(f"\n   Options:")
    
    for i, value in enumerate(values, 1):
        print(f"   {i}. {value}")
    
    while True:
        try:
            choice = input(f"\n   Enter choice (1-{len(values)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(values):
                return values[idx]
            else:
                print(f"   ❌ Please enter a number between 1 and {len(values)}")
        except (ValueError, KeyboardInterrupt):
            print("   ❌ Invalid input. Please enter a number.")
        except EOFError:
            sys.exit(0)


def display_recommendations(es: ExpertSystem):
    """Display final recommendations"""
    candidates = es.get_top_candidates(n=5)
    
    if not candidates:
        print("\n❌ No cars match your criteria!")
        return
    
    print("\n" + "=" * 70)
    print("  🎯 TOP RECOMMENDATIONS (with AI confidence scores)")
    print("=" * 70)
    
    for i, (car, confidence) in enumerate(candidates, 1):
        print(f"\n{i}. {car['brand']} {car['model']}")
        print(f"   Confidence: {confidence*100:.1f}%")
        print(f"   Type: {car['body_type']}")
        print(f"   Fuel: {car['fuel_type']}")
        print(f"   Price Range: {car['price_range'].replace('_', ' ').replace('-', ' to ')}")
        print(f"   Luxury: {car['luxury']}")
        print(f"   Engine: {car['engine_cc']} cc")
    
    print("\n" + "=" * 70)


def display_reasoning_trace(es: ExpertSystem):
    """Display AI reasoning trace"""
    print("\n" + "=" * 70)
    print("  🧠 AI REASONING TRACE")
    print("=" * 70)
    
    print("\n  Questions Asked:")
    for i, (attr, value) in enumerate(es.question_history, 1):
        print(f"    {i}. {attr.replace('_', ' ')}: {value}")
    
    # Get inferred facts
    inferred = es.inference_engine.forward_chain(es.belief_state)
    print("\n  Inferred Facts (using forward chaining):")
    for fact, value in inferred.items():
        if value:
            print(f"    ✓ {fact.replace('_', ' ')}")
    
    status = es.get_status()
    print(f"\n  Final State:")
    print(f"    • Possible cars: {status['possible_cars']}")
    print(f"    • Determined: {'Yes' if status['is_determined'] else 'No'}")
    
    print("=" * 70)


def main():
    """Main interactive loop"""
    print_banner()
    
    # Initialize expert system
    print("\n[System] Loading knowledge base...")
    es = ExpertSystem()
    
    print("\n✅ Ready! I know about 50 Indian market cars.")
    print("   Think of a car, and I'll try to guess it!")
    
    input("\n   Press Enter to start...")
    
    # Main reasoning loop
    question_count = 0
    max_questions = 10  # Limit questions to avoid exhaustion
    
    while question_count < max_questions:
        # Check if determined
        status = es.get_status()
        if status['is_determined'] or status['possible_cars'] <= 3:
            break
        
        # Ask next question using AI reasoning
        result = es.ask_question()
        
        if result is None:
            break
        
        attribute, values = result
        
        # Display current status
        display_status(es)
        
        # Ask user
        answer = ask_user_question(attribute, values)
        
        # Process answer and update belief state
        print(f"\n   [AI] Processing your answer: {answer}")
        inferred = es.process_answer(attribute, answer)
        
        # Show inference results
        if any(inferred.values()):
            print(f"   [AI] Inferred: {', '.join(k for k, v in inferred.items() if v)}")
        
        question_count += 1
    
    # Display final recommendations
    display_recommendations(es)
    
    # Display reasoning trace
    display_reasoning_trace(es)
    
    # Ask if user wants to play again
    print("\n" + "=" * 70)
    try:
        again = input("   Play again? (y/n): ").strip().lower()
        if again == 'y':
            es.reset()
            print("\n   [System] Starting new session...\n")
            main()
        else:
            print("\n   👋 Thank you for trying the Expert System!")
            print("=" * 70)
    except (KeyboardInterrupt, EOFError):
        print("\n\n   👋 Thank you for trying the Expert System!")
        print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n   👋 Goodbye!")
        sys.exit(0)
