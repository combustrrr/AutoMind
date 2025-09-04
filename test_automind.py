#!/usr/bin/env python3
"""
Test script for AutoMind game functionality
"""

from automind import GuessTheCarGame, CarData

def test_car_data():
    """Test the CarData class."""
    print("Testing CarData class...")
    data = CarData()
    assert len(data.cars) > 0, "No cars loaded"
    
    car = data.get_random_car()
    assert 'model' in car, "Car missing model field"
    assert 'brand' in car, "Car missing brand field"
    print(f"✅ CarData test passed. Sample car: {car['model']}")

def test_game_logic():
    """Test the game logic."""
    print("\nTesting GuessTheCarGame class...")
    game = GuessTheCarGame()
    
    # Start a new game
    game.start_new_game()
    assert game.current_car is not None, "No car selected"
    
    # Test clue generation
    clue = game.get_clue(0)
    assert len(clue) > 0, "Empty clue generated"
    print(f"✅ Clue generation test passed. Sample clue: {clue}")
    
    # Test guess checking
    correct_model = game.current_car['model']
    assert game.check_guess(correct_model), "Correct guess not recognized"
    assert not game.check_guess("NonexistentCar"), "Wrong guess accepted"
    print(f"✅ Guess checking test passed. Test car: {correct_model}")
    
    # Test score calculation
    game.attempts = 1
    score = game.calculate_score()
    assert score == 100, "Score calculation incorrect for 1 attempt"
    print(f"✅ Score calculation test passed. Score for 1 attempt: {score}")

def test_data_integrity():
    """Test data integrity and completeness."""
    print("\nTesting data integrity...")
    data = CarData()
    
    required_fields = ['model', 'brand', 'body_type', 'fuel_type', 'price_range', 'luxury', 'engine_cc', 'keywords']
    
    for i, car in enumerate(data.cars):
        for field in required_fields:
            assert field in car, f"Car {i} missing field: {field}"
        
        # Check for empty values
        for field in required_fields:
            assert car[field].strip(), f"Car {i} has empty {field}"
    
    print(f"✅ Data integrity test passed. All {len(data.cars)} cars have complete data.")

def run_all_tests():
    """Run all tests."""
    print("🧪 Running AutoMind Game Tests")
    print("="*40)
    
    try:
        test_car_data()
        test_game_logic()
        test_data_integrity()
        print("\n🎉 All tests passed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)