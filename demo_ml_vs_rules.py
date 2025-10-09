#!/usr/bin/env python3
"""
Demo: ML-Powered AutoMind
Showcases machine learning predictions vs rule-based predictions
"""

from ml_guessing_engine import MLGuessingEngine
from guessing_engine import GuessingEngine
from nlp_engine import extract_features


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def compare_predictions(query: str):
    """Compare ML predictions with rule-based predictions."""
    print(f"\n📝 Query: '{query}'")
    print("-" * 70)
    
    # ML Predictions
    ml_engine = MLGuessingEngine()
    if ml_engine.ml_available:
        ml_predictions = ml_engine.predict_cars(query, top_n=3)
        
        print("\n🤖 ML Predictions (Actual Machine Learning):")
        for i, (car, confidence) in enumerate(ml_predictions, 1):
            print(f"  {i}. {car['brand']} {car['model']} - {confidence*100:.1f}% confidence")
    else:
        print("\n❌ ML model not available")
    
    # Rule-based Predictions  
    rule_engine = GuessingEngine()
    features = extract_features(query)
    rule_matches = rule_engine.find_matches(features, top_n=3)
    
    print("\n📏 Rule-Based Predictions (Pattern Matching):")
    for i, (car, score) in enumerate(rule_matches, 1):
        print(f"  {i}. {car['brand']} {car['model']} - {score}/100 score")


def main():
    """Run ML demo."""
    print("=" * 70)
    print("  🚗 AUTOMIND - ML vs RULE-BASED COMPARISON 🚗")
    print("=" * 70)
    print("\nShowcasing the difference between:")
    print("  • 🤖 Machine Learning (learns patterns from data)")
    print("  • 📏 Rule-Based (matches keywords)")
    
    # Test queries
    test_queries = [
        "Toyota SUV under 20 lakhs",
        "electric car with good range",
        "luxury sedan comfortable ride",
        "affordable family hatchback",
        "sporty car fast acceleration",
    ]
    
    for query in test_queries:
        compare_predictions(query)
    
    print_section("KEY DIFFERENCES")
    print("""
🤖 ML Predictions:
  • Learns from data (not hard-coded rules)
  • Provides confidence scores (knows uncertainty)
  • Generalizes to unseen queries
  • Improves with more training data

📏 Rule-Based Predictions:
  • Uses pre-programmed keyword matching
  • Fixed scoring system
  • Explainable (clear matching rules)
  • No training required

💡 Best Approach: Hybrid
  • Use ML for complex queries
  • Fallback to rules for simple/specific queries
  • Combine confidence scores
    """)
    
    print("=" * 70)
    print("\n✅ ML integration complete!")
    print("\nTo improve ML accuracy:")
    print("  1. Generate more training data")
    print("  2. Add more diverse query templates")
    print("  3. Fine-tune model hyperparameters")


if __name__ == "__main__":
    main()
