#!/usr/bin/env python3
"""
Demo script for AutoMind - Guess the Car Game
Shows how the game works with simulated gameplay
"""

from automind import GuessTheCarGame, CarData
import time

def simulate_gameplay():
    """Simulate a game session for demonstration."""
    print("🎬 AutoMind Game Demo")
    print("="*40)
    
    # Initialize game
    game = GuessTheCarGame()
    game.start_new_game()
    
    # Show the car we're going to "guess" (for demo purposes)
    target_car = game.current_car
    print(f"\n[Demo Info: Target car is {target_car['model']} by {target_car['brand']}]")
    
    # Simulate getting clues
    print("\n🤖 Player asks for hints...")
    for i in range(3):
        clue = game.get_clue(i)
        print(f"💡 Clue {i+1}: {clue}")
        time.sleep(1)
    
    # Simulate making a guess
    print(f"\n🤖 Player guesses: {target_car['model']}")
    game.attempts = 3  # Simulate 3 attempts
    
    if game.check_guess(target_car['model']):
        score = game.calculate_score()
        print(f"🎉 Correct! Score: {score} points")
    
    # Show some statistics
    print(f"\n📊 Game Statistics:")
    print(f"   • Total cars in database: {len(game.car_data.cars)}")
    print(f"   • Car brands available: {len(set(car['brand'] for car in game.car_data.cars))}")
    print(f"   • Body types: {set(car['body_type'] for car in game.car_data.cars)}")
    print(f"   • Fuel types: {set(car['fuel_type'] for car in game.car_data.cars)}")

def show_sample_cars():
    """Display some sample cars from the database."""
    print("\n🚗 Sample Cars in Database:")
    print("-"*50)
    
    data = CarData()
    
    # Show a few different types of cars
    shown_brands = set()
    count = 0
    
    for car in data.cars:
        if car['brand'] not in shown_brands and count < 5:
            luxury_status = "Luxury" if car['luxury'] == 'True' else "Mass Market"
            engine_info = f"{car['engine_cc']}cc" if car['engine_cc'] != '0' else "Electric"
            
            print(f"🔸 {car['model']} ({car['brand']})")
            print(f"   {car['body_type']} | {car['fuel_type']} | {engine_info} | {luxury_status}")
            print(f"   Price: {car['price_range'].replace('_', ' ').replace('L', ' lakhs')}")
            print(f"   Keywords: {car['keywords']}")
            print()
            
            shown_brands.add(car['brand'])
            count += 1

def main():
    """Run the demo."""
    print("AutoMind Demo - Showcasing the Car Guessing Game")
    print("="*60)
    
    show_sample_cars()
    simulate_gameplay()
    
    print("\n" + "="*60)
    print("🎮 Ready to play the real game? Run: python3 automind.py")
    print("🧪 Want to run tests? Run: python3 test_automind.py")

if __name__ == "__main__":
    main()