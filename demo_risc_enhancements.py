#!/usr/bin/env python3
"""
Demo script for RISC AI Enhancements
Showcases the three micro-enhancements in action
"""

from nlp_engine import (
    extract_features,
    calculate_confidence,
    get_preferences,
    reset_preferences,
    clear_context,
    handle_confusion,
    suggest_clarification
)


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_smart_clarification():
    """Demo smart clarification feature."""
    print_section("DEMO 1: SMART CLARIFICATION")
    
    print("🎯 Purpose: Ask for details when confidence is low (< 30%)\n")
    
    # Low confidence query
    print("Query: 'a car'")
    print("-" * 70)
    features = extract_features("a car")
    confidence = calculate_confidence(features)
    clarification = suggest_clarification(features, confidence)
    
    print(f"\n💡 Confidence: {confidence:.1%}")
    if clarification:
        print(f"💡 System Response: {clarification}")
    
    print("\n" + "-" * 70)
    
    # High confidence query
    print("\nQuery: 'Toyota SUV under 20 lakhs'")
    print("-" * 70)
    features = extract_features("Toyota SUV under 20 lakhs")
    confidence = calculate_confidence(features)
    clarification = suggest_clarification(features, confidence)
    
    print(f"\n💡 Confidence: {confidence:.1%}")
    if clarification:
        print(f"💡 System Response: {clarification}")
    else:
        print("💡 System Response: No clarification needed - proceeding with search!")


def demo_preference_learning():
    """Demo preference learning feature."""
    print_section("DEMO 2: PREFERENCE LEARNING")
    
    print("🎯 Purpose: Remember what user likes across conversation\n")
    
    # Reset for demo
    clear_context()
    reset_preferences()
    
    # Query 1
    print("Query 1: 'electric car'")
    print("-" * 70)
    features1 = extract_features("electric car")
    prefs1 = get_preferences()
    print(f"\n💡 Learned: Prefers electric = {prefs1['prefers_electric']}")
    
    # Query 2
    print("\n\nQuery 2: 'Toyota SUV under 20 lakhs'")
    print("-" * 70)
    features2 = extract_features("Toyota SUV under 20 lakhs")
    prefs2 = get_preferences()
    print(f"\n💡 Learned: Prefers electric = {prefs2['prefers_electric']}")
    print(f"💡 Learned: Prefers SUV = {prefs2['prefers_suv']}")
    print(f"💡 Learned: Brands = {prefs2['preferred_brands']}")
    
    # Query 3
    print("\n\nQuery 3: 'luxury BMW sedan'")
    print("-" * 70)
    features3 = extract_features("luxury BMW sedan")
    prefs3 = get_preferences()
    print(f"\n💡 Learned: Prefers electric = {prefs3['prefers_electric']}")
    print(f"💡 Learned: Prefers SUV = {prefs3['prefers_suv']}")
    print(f"💡 Learned: Brands = {prefs3['preferred_brands']}")
    print(f"💡 Learned: Price sensitivity = {prefs3['price_sensitivity']}")
    
    print("\n\n🎉 Summary: System now knows user preferences:")
    print("   • Interested in electric vehicles")
    print("   • Likes SUVs")
    print("   • Considering Toyota and BMW")
    print("   • Looking at luxury segment")


def demo_conversation_repair():
    """Demo conversation repair feature."""
    print_section("DEMO 3: CONVERSATION REPAIR")
    
    print("🎯 Purpose: Help users when queries are unclear\n")
    
    # Reset for demo
    clear_context()
    reset_preferences()
    
    # Vague query
    print("Query: 'something nice'")
    print("-" * 70)
    features = extract_features("something nice")
    
    print(f"\n💡 Confusion Detected!")
    print(f"💡 System Response: {handle_confusion()}")
    
    # Another vague query
    print("\n\nQuery: 'car'")
    print("-" * 70)
    features = extract_features("car")
    confidence = calculate_confidence(features)
    clarification = suggest_clarification(features, confidence)
    
    print(f"\n💡 Low Confidence: {confidence:.1%}")
    print(f"💡 System Response: {clarification}")
    
    print("\n\n🎉 Summary: System provides helpful guidance instead of errors!")


def _extract_turn_features(query: str, turn_num: int):
    """Extract and display features for a conversation turn."""
    print(f"Turn {turn_num}: '{query}'")
    print("-" * 70)
    
    features = extract_features(query)
    confidence = calculate_confidence(features)
    
    print(f"  Extracted: brand={features['brand']}, "
          f"type={features['type']}, "
          f"fuel={features['fuel']}, "
          f"price={features['price_range']}")
    print(f"  Confidence: {confidence:.1%}")
    
    return features


def _display_learned_preferences(prefs):
    """Display learned preferences from a conversation turn."""
    learned = []
    if prefs['prefers_electric']:
        learned.append("electric")
    if prefs['prefers_suv'] is not None:
        learned.append("SUV" if prefs['prefers_suv'] else "non-SUV")
    if prefs['preferred_brands']:
        learned.append(f"brands: {', '.join(prefs['preferred_brands'])}")
    
    if learned:
        print(f"  Preferences: {'; '.join(learned)}")


def demo_full_conversation():
    """Demo full conversation with all features."""
    print_section("DEMO 4: COMPLETE CONVERSATION")
    
    print("🎯 Purpose: Show all features working together\n")
    
    # Reset for demo
    clear_context()
    reset_preferences()
    
    conversation = [
        "electric",
        "Tesla",
        "the sedan one",
        "around 50 lakhs"
    ]
    
    for i, query in enumerate(conversation, 1):
        _extract_turn_features(query, i)
        
        prefs = get_preferences()
        _display_learned_preferences(prefs)
        
        print()
    
    print("🎉 Summary: Natural conversation with context awareness!")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("  🚗 AUTOMIND - RISC AI ENHANCEMENTS DEMO 🚗")
    print("=" * 70)
    print("\nShowcasing three intelligent micro-enhancements:")
    print("  1. Smart Clarification (asks for details when unsure)")
    print("  2. Preference Learning (remembers what you like)")
    print("  3. Conversation Repair (helps when confused)")
    
    # Run demos
    demo_smart_clarification()
    demo_preference_learning()
    demo_conversation_repair()
    demo_full_conversation()
    
    # Final summary
    print_section("SUMMARY")
    print("✅ Smart Clarification: Guides users to better queries")
    print("✅ Preference Learning: Personalizes across conversation")
    print("✅ Conversation Repair: Helpful instead of frustrating")
    print("\n💡 Key Insight: Intelligence from architecture, not complexity!")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
