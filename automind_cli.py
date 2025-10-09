#!/usr/bin/env python3
"""
AutoMind CLI - Simple command-line interface
For when Streamlit is not available
"""

from nlp_engine import extract_features, suggest_similar_queries, clear_context, get_context_stack, get_preferences, reset_preferences, calculate_confidence
from guessing_engine import GuessingEngine


def print_banner():
    """Print welcome banner."""
    print("=" * 70)
    print(" " * 15 + "🚗 AUTOMIND - CAR RECOMMENDER 🚗")
    print("=" * 70)
    print()
    print("Welcome! Describe the car you're looking for and I'll find matches.")
    print("Type 'quit' or 'exit' to stop, 'help' for examples")
    print()


def print_help():
    """Print help information."""
    print("\n📋 EXAMPLE QUERIES:")
    print("  • 'A Toyota SUV under 20 lakhs'")
    print("  • 'Luxury BMW sedan above 50L'")
    print("  • 'Cheap Maruti hatchback'")
    print("  • 'Electric car by Tesla'")
    print("  • 'Premium diesel sedan from Hyundai'")
    print()
    print("💡 SUPPORTED FEATURES:")
    print("  • Brand: Toyota, Hyundai, Maruti, BMW, etc.")
    print("  • Type: SUV, Sedan, Hatchback")
    print("  • Fuel: Petrol, Diesel, Electric")
    print("  • Price: under 10L, 20-30L, above 30L, etc.")
    print("  • Luxury: premium, luxury, cheap, budget, etc.")
    print()
    print("🤖 AI FEATURES (RISC-Style):")
    print("  • Nickname recognition: 'beemer' → BMW, 'merc' → Mercedes")
    print("  • Typo correction: 'Tayota' → Toyota, 'Hundai' → Hyundai")
    print("  • Context memory: Say 'the sedan one' after mentioning a brand")
    print("  • Smart clarification: Asks for more details when unsure")
    print("  • Preference learning: Remembers what you like across conversation")
    print("  • Type 'clear' to reset conversation context")
    print("  • Type 'prefs' to see your learned preferences")
    print()


def display_features(features):
    """Display extracted features."""
    print("\n🎯 EXTRACTED FEATURES:")
    print("-" * 70)
    
    feature_labels = {
        'brand': '🏢 Brand',
        'type': '🚙 Type',
        'fuel': '⛽ Fuel',
        'price_range': '💰 Price Range',
        'luxury': '⭐ Luxury Status'
    }
    
    for key, label in feature_labels.items():
        value = features.get(key)
        if value is not None:
            if key == 'luxury':
                value = "Yes (Premium)" if value else "No (Budget)"
            print(f"  {label:20}: {value}")
        else:
            print(f"  {label:20}: Not specified")
    
    print("-" * 70)


def display_matches(matches, engine, features):
    """Display car matches."""
    if not matches:
        print("\n😕 NO MATCHES FOUND")
        print("\nI couldn't find any cars matching your criteria.")
        print("This might happen if:")
        print("  • The combination is too specific (try removing some filters)")
        print("  • The brand/model isn't in our database")
        print("  • There's a typo in the query")
        return False
    
    print(f"\n🎉 FOUND {len(matches)} MATCHES!\n")
    print("=" * 70)
    return True
    
    # Display top match prominently
    top_car, top_score = matches[0]
    print("\n🏆 BEST MATCH:")
    print("-" * 70)
    print(f"  {top_car.get('brand', '')} {top_car.get('model', '')}")
    print(f"  Type: {top_car.get('body_type', 'N/A')}")
    print(f"  Fuel: {top_car.get('fuel_type', 'N/A')}")
    print(f"  Price Range: {top_car.get('price_range', 'N/A').replace('_', ' ')}")
    print(f"  Luxury: {top_car.get('luxury', 'N/A')}")
    print(f"  Match Score: {top_score}/100")
    
    confidence = "High" if top_score >= 50 else "Medium" if top_score >= 30 else "Low"
    print(f"  Confidence: {confidence}")
    print("-" * 70)
    
    # Display other matches
    if len(matches) > 1:
        print("\n📋 OTHER RECOMMENDATIONS:\n")
        for i, (car, score) in enumerate(matches[1:], 2):
            print(f"{i}. {car.get('brand', '')} {car.get('model', '')} (Score: {score})")
            print(f"   Type: {car.get('body_type', 'N/A')}, "
                  f"Fuel: {car.get('fuel_type', 'N/A')}, "
                  f"Price: {car.get('price_range', 'N/A').replace('_', ' ')}")
    
    print()


def _handle_help_command():
    """Handle help command."""
    print_help()


def _handle_clear_command():
    """Handle clear command."""
    clear_context()
    reset_preferences()
    print("✨ Context and preferences cleared! Starting fresh conversation.\n")
    return 0  # Reset query count


def _display_preferences():
    """Display user preferences."""
    prefs = get_preferences()
    print("\n🧠 YOUR LEARNED PREFERENCES:")
    print("-" * 70)
    
    if prefs['prefers_electric'] is True:
        print("  • Prefers: Electric vehicles")
    elif prefs['prefers_electric'] is False:
        print("  • Prefers: Non-electric vehicles")
    
    if prefs['prefers_suv'] is True:
        print("  • Prefers: SUVs")
    elif prefs['prefers_suv'] is False:
        print("  • Prefers: Non-SUV body types")
    
    if prefs['preferred_brands']:
        print(f"  • Brands you've searched: {', '.join(prefs['preferred_brands'])}")
    
    if prefs['price_sensitivity']:
        print(f"  • Price sensitivity: {prefs['price_sensitivity']}")
    
    if not any([prefs['prefers_electric'], prefs['prefers_suv'], 
               prefs['preferred_brands'], prefs['price_sensitivity']]):
        print("  • No preferences learned yet. Keep searching!")
    print("-" * 70)
    print()


def _show_context_info():
    """Show context information if available."""
    context = get_context_stack()
    if len(context) > 0:
        print(f"💭 Context: Remembering {len(context)} previous turn(s)")


def _suggest_followup(has_matches, matches, engine, features, user_input):
    """Suggest follow-up queries based on results."""
    if not has_matches:
        followup = engine.suggest_followup_question(features)
        print(f"\n💡 TIP: {followup}")
        
        # Get smart suggestions based on query
        suggestions = suggest_similar_queries(user_input)
        print("\n🔄 You could also try:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
        print()
    elif matches and matches[0][1] < 30:
        print(f"\n⚠️  Low confidence match (score: {matches[0][1]}/100)")
        print("💡 TIP: Try adding more details for better results:")
        followup = engine.suggest_followup_question(features)
        print(f"   - {followup}\n")


def _process_query(user_input: str, engine: GuessingEngine):
    """Process a user query and display results."""
    _show_context_info()
    
    # Extract features
    print("⚙️  Analyzing your query...")
    features = extract_features(user_input)
    
    # Display extracted features
    display_features(features)
    
    # Find matches
    print("\n🔎 Searching database...")
    matches = engine.find_matches(features, top_n=5)
    
    # Display results
    has_matches = display_matches(matches, engine, features)
    
    # Suggest follow-up
    _suggest_followup(has_matches, matches, engine, features, user_input)
    
    print("=" * 70)


def main():
    """Main CLI loop."""
    print_banner()
    
    # Initialize engine
    print("Loading car database...")
    engine = GuessingEngine()
    print(f"✅ Ready! {len(engine.cars)} cars loaded.")
    print("💡 Tip: Type 'help' for examples, 'clear' to reset context\n")
    
    # Main loop
    query_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("🔍 Your query: ").strip()
            
            # Handle commands
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using AutoMind! Goodbye!")
                print(f"\n📊 Session Summary: {query_count} queries processed")
                break
            
            if user_input.lower() in ['help', 'h', '?']:
                _handle_help_command()
                continue
            
            if user_input.lower() == 'clear':
                query_count = _handle_clear_command()
                continue
            
            if user_input.lower() in ['prefs', 'preferences']:
                _display_preferences()
                continue
            
            query_count += 1
            print()
            
            _process_query(user_input, engine)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.\n")
    
    # Summary
    print(f"\n📊 Session Summary: {query_count} queries processed")


if __name__ == "__main__":
    main()
