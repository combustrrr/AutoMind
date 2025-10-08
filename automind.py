#!/usr/bin/env python3
"""
AutoMind - Guess the Car Game

A fun car guessing game using Indian market car data.
Players receive clues about a car and try to guess the model.
"""

import csv
import random
import sys
from typing import Dict, List, Optional


class CarData:
    """Handles loading and accessing car data."""
    
    def __init__(self, data_file: str = "data/car_data_enriched.csv"):
        self.cars: List[Dict[str, str]] = []
        self.data_file = data_file
        self.load_data()
    
    def load_data(self) -> None:
        """Load car data from CSV file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.cars = list(reader)
            print(f"Loaded {len(self.cars)} cars from database.")
        except FileNotFoundError:
            print(f"Error: Could not find data file '{self.data_file}'")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading data: {e}")
            sys.exit(1)
    
    def get_random_car(self) -> Dict[str, str]:
        """Get a random car from the database."""
        return random.choice(self.cars)


class GuessTheCarGame:
    """Main game class for the car guessing game."""
    
    def __init__(self):
        self.car_data = CarData()
        self.current_car: Optional[Dict[str, str]] = None
        self.attempts = 0
        self.max_attempts = 5
        self.score = 0
        self.games_played = 0
    
    def start_new_game(self) -> None:
        """Start a new round of the guessing game."""
        self.current_car = self.car_data.get_random_car()
        self.attempts = 0
        self.games_played += 1
        
        print("\n" + "="*50)
        print(f"🚗 GUESS THE CAR - Round {self.games_played}")
        print("="*50)
        print(f"I'm thinking of a car... You have {self.max_attempts} attempts to guess it!")
        print("Type 'hint' for a clue, 'quit' to exit, or guess the car model.")
        print("-"*50)
    
    def get_clue(self, clue_level: int) -> str:
        """Generate clues based on the current car's attributes."""
        if not self.current_car:
            return "No car selected!"
        
        clues = [
            f"🏢 Brand: This car is made by {self.current_car['brand']}",
            f"🚙 Body Type: It's a {self.current_car['body_type'].lower()}",
            f"⛽ Fuel Type: It runs on {self.current_car['fuel_type'].lower()}",
            f"💰 Price Range: It costs {self.current_car['price_range'].replace('_', ' ').replace('L', ' lakhs')}",
            f"🔧 Engine: It has a {self.current_car['engine_cc']}cc engine" if self.current_car['engine_cc'] != '0' else "🔋 It's an electric vehicle",
            f"✨ Keywords: {self.current_car['keywords']}"
        ]
        
        # Return clues progressively
        if clue_level < len(clues):
            return clues[clue_level]
        else:
            return "No more clues available!"
    
    def check_guess(self, guess: str) -> bool:
        """Check if the guess matches the current car model."""
        if not self.current_car:
            return False
        
        # Normalize both strings for comparison
        car_model = self.current_car['model'].lower().strip()
        user_guess = guess.lower().strip()
        
        # Check for exact match or if guess is contained in model name
        return user_guess == car_model or user_guess in car_model
    
    def calculate_score(self) -> int:
        """Calculate score based on attempts used."""
        if self.attempts == 1:
            return 100  # Perfect guess
        elif self.attempts == 2:
            return 75   # Excellent
        elif self.attempts == 3:
            return 50   # Good
        elif self.attempts == 4:
            return 25   # Fair
        else:
            return 10   # Just made it
    
    def play_round(self) -> bool:
        """Play a single round of the game. Returns True if player wants to continue."""
        self.start_new_game()
        clue_level = 0
        
        while self.attempts < self.max_attempts:
            print(f"\nAttempt {self.attempts + 1}/{self.max_attempts}")
            user_input = input("Your guess (or 'hint'/'quit'): ").strip()
            
            if user_input.lower() == 'quit':
                print("Thanks for playing! 👋")
                return False
            
            if user_input.lower() == 'hint':
                clue = self.get_clue(clue_level)
                print(f"💡 Clue: {clue}")
                clue_level += 1
                continue
            
            self.attempts += 1
            
            if self.check_guess(user_input):
                round_score = self.calculate_score()
                self.score += round_score
                print(f"\n🎉 Correct! The car was: {self.current_car['model']}")
                print(f"You got it in {self.attempts} attempt(s)!")
                print(f"Round score: +{round_score} points")
                print(f"Total score: {self.score} points")
                break
            else:
                remaining = self.max_attempts - self.attempts
                if remaining > 0:
                    print(f"❌ Not quite right. {remaining} attempt(s) remaining.")
                else:
                    print(f"\n💔 Out of attempts! The car was: {self.current_car['model']}")
                    print(f"Better luck next round!")
        
        # Ask if player wants to continue
        while True:
            continue_game = input("\nPlay another round? (y/n): ").strip().lower()
            if continue_game in ['y', 'yes']:
                return True
            elif continue_game in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    def run(self) -> None:
        """Main game loop."""
        print("🚗 Welcome to AutoMind - Guess the Car! 🚗")
        print("\nCan you identify Indian market cars from clues?")
        
        try:
            while True:
                if not self.play_round():
                    break
            
            # Game over - show final stats
            print("\n" + "="*50)
            print("🏁 GAME OVER - Final Statistics")
            print("="*50)
            print(f"Games played: {self.games_played}")
            print(f"Final score: {self.score} points")
            if self.games_played > 0:
                avg_score = self.score / self.games_played
                print(f"Average score per game: {avg_score:.1f} points")
            print("\nThanks for playing AutoMind! 🚗💨")
            
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing! 👋")
        except Exception as e:
            print(f"\nAn error occurred: {e}")


def main():
    """Entry point for the game."""
    game = GuessTheCarGame()
    game.run()


if __name__ == "__main__":
    main()