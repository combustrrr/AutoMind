#!/usr/bin/env python3
"""
Car Akinator - Interactive car guessing game
Like Akinator but for cars - asks questions to guess the car you're thinking of
"""

import csv
import random
from typing import List, Dict, Optional, Tuple
from collections import Counter

class CarAkinator:
    """
    Interactive car guessing game that asks strategic questions
    to narrow down and guess the car the user is thinking of.
    """
    
    def __init__(self, csv_path: str = "data/car_data.csv"):
        """Initialize the car database and question strategy."""
        self.cars = []
        self.load_cars(csv_path)
        self.remaining_cars = self.cars.copy()
        self.questions_asked = []
        self.answers_given = []
        self.question_count = 0
        
        # Question strategy - ordered by information value
        self.question_strategy = [
            ("luxury", "Is it a luxury/premium car?"),
            ("body_type", "Is it an SUV?"),
            ("fuel_type", "Does it run on petrol?"),
            ("price_range", "Is it priced under 15 lakhs?"),
            ("body_type", "Is it a sedan?"),
            ("fuel_type", "Is it a diesel car?"),
            ("brand", "Is it made by a Japanese company (Toyota/Honda)?"),
            ("price_range", "Is it priced above 25 lakhs?"),
            ("brand", "Is it made by Maruti Suzuki?"),
            ("brand", "Is it made by Hyundai?"),
        ]
        
    def load_cars(self, csv_path: str):
        """Load car database from CSV file."""
        try:
            with open(csv_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.cars.append({
                        'model': row['model'],
                        'brand': row['brand'],
                        'body_type': row['body_type'],
                        'fuel_type': row['fuel_type'],
                        'price_range': row['price_range'],
                        'luxury': row['luxury'],
                        'engine_cc': row['engine_cc']
                    })
            print(f"[Car Akinator] Loaded {len(self.cars)} cars")
        except FileNotFoundError:
            print(f"[Car Akinator] Error: Could not find {csv_path}")
            self.cars = []
    
    def start_game(self):
        """Start a new guessing game."""
        self.remaining_cars = self.cars.copy()
        self.questions_asked = []
        self.answers_given = []
        self.question_count = 0
        
        print("\n🎯 Welcome to Car Akinator!")
        print("Think of any car from the Indian market, and I'll try to guess it!")
        print("Answer with 'yes', 'no', or 'don't know'")
        print("=" * 60)
        print(f"I have {len(self.remaining_cars)} cars in my database...")
        
    def get_best_question(self) -> Optional[Tuple[str, str]]:
        """
        Get the most strategic question to ask next.
        Uses information theory to find question that best splits remaining cars.
        """
        if len(self.remaining_cars) <= 1:
            return None
            
        # If few cars left, ask direct model questions
        if len(self.remaining_cars) <= 3:
            for car in self.remaining_cars:
                model_question = f"Are you thinking of the {car['brand']} {car['model']}?"
                return ("model", model_question)
        
        # Use predefined strategy for systematic questioning
        for attr, question in self.question_strategy:
            if (attr, question) not in self.questions_asked:
                # Check if this question would be informative
                if self._is_question_useful(attr, question):
                    return (attr, question)
        
        # Fallback: ask about specific brands if strategy exhausted
        brands = set(car['brand'] for car in self.remaining_cars)
        for brand in brands:
            question = f"Is it made by {brand}?"
            if ("brand", question) not in self.questions_asked:
                return ("brand", question)
        
        return None
    
    def _is_question_useful(self, attribute: str, question: str) -> bool:
        """Check if asking this question would help narrow down cars."""
        if attribute == "model":
            return True
            
        # Count how this question would split the remaining cars
        yes_count = 0
        no_count = 0
        
        for car in self.remaining_cars:
            if self._would_answer_yes(car, attribute, question):
                yes_count += 1
            else:
                no_count += 1
        
        # Good question splits cars roughly in half
        total = len(self.remaining_cars)
        if total <= 2:
            return True
            
        # Useful if it eliminates at least 1/4 of remaining cars
        min_elimination = max(1, total // 4)
        return min(yes_count, no_count) >= min_elimination
    
    def _would_answer_yes(self, car: Dict, attribute: str, question: str) -> bool:
        """Determine if a car would match a 'yes' answer to the question."""
        if attribute == "luxury":
            return car['luxury'].lower() == 'yes'
        elif attribute == "body_type":
            if "SUV" in question:
                return car['body_type'].lower() == 'suv'
            elif "sedan" in question:
                return car['body_type'].lower() == 'sedan'
            elif "hatchback" in question:
                return car['body_type'].lower() == 'hatchback'
        elif attribute == "fuel_type":
            if "petrol" in question:
                return car['fuel_type'].lower() == 'petrol'
            elif "diesel" in question:
                return car['fuel_type'].lower() == 'diesel'
            elif "electric" in question:
                return car['fuel_type'].lower() == 'electric'
        elif attribute == "price_range":
            if "under 15 lakhs" in question:
                return car['price_range'] in ['under_10L', 'under_20L']
            elif "above 25 lakhs" in question:
                return car['price_range'] in ['above_30L', '20-30L']
            elif "under 10 lakhs" in question:
                return car['price_range'] == 'under_10L'
        elif attribute == "brand":
            if "Japanese" in question:
                return car['brand'] in ['Toyota', 'Honda']
            elif "Maruti" in question:
                return 'Maruti' in car['brand']
            elif "Hyundai" in question:
                return car['brand'] == 'Hyundai'
            else:
                # Extract brand name from question
                for brand in ['Toyota', 'Honda', 'Hyundai', 'Tata', 'Mahindra', 'BMW', 'Mercedes']:
                    if brand in question:
                        return brand in car['brand']
        elif attribute == "model":
            # Direct model question
            return car['model'] in question
            
        return False
    
    def process_answer(self, answer: str, current_question: Tuple[str, str]) -> bool:
        """
        Process user's answer and filter remaining cars.
        Returns True if game should continue, False if we have a guess.
        """
        answer = answer.lower().strip()
        attribute, question = current_question
        
        self.questions_asked.append(current_question)
        self.answers_given.append(answer)
        self.question_count += 1
        
        if answer in ['yes', 'y']:
            # Keep cars that match 'yes' answer
            self.remaining_cars = [
                car for car in self.remaining_cars 
                if self._would_answer_yes(car, attribute, question)
            ]
        elif answer in ['no', 'n']:
            # Keep cars that match 'no' answer  
            self.remaining_cars = [
                car for car in self.remaining_cars 
                if not self._would_answer_yes(car, attribute, question)
            ]
        elif answer in ["don't know", "dont know", "dk", "idk"]:
            # Keep all cars (no filtering)
            pass
        else:
            print("Please answer 'yes', 'no', or 'don't know'")
            return True
        
        print(f"🤔 Narrowed down to {len(self.remaining_cars)} possibilities...")
        
        # Check if we can make a guess
        if len(self.remaining_cars) == 1:
            return False  # Ready to guess
        elif len(self.remaining_cars) == 0:
            print("🤨 Hmm, no cars match your answers. Let me think of something else...")
            return False
        elif len(self.remaining_cars) <= 3 and self.question_count >= 3:
            return False  # Make educated guess
            
        return True  # Continue asking questions
    
    def make_final_guess(self) -> str:
        """Make final guess and return result message."""
        if len(self.remaining_cars) == 0:
            return self._handle_no_match()
        elif len(self.remaining_cars) == 1:
            return self._handle_perfect_guess()
        else:
            return self._handle_multiple_guesses()
    
    def _handle_no_match(self) -> str:
        """Handle case where no cars match the answers."""
        result = "\n🤔 Strange... no cars in my database match your answers.\n"
        result += "Possible reasons:\n"
        result += "• The car might not be in my database\n"
        result += "• There might have been a misunderstanding in the questions\n"
        result += "• You might be thinking of a car from outside the Indian market\n\n"
        result += "💡 Want to try again with a different car?"
        return result
    
    def _handle_perfect_guess(self) -> str:
        """Handle case where we narrowed down to exactly one car."""
        car = self.remaining_cars[0]
        result = f"\n🎉 **I've got it!**\n\n"
        result += f"You're thinking of the **{car['brand']} {car['model']}**!\n\n"
        result += f"📋 Car Details:\n"
        result += f"• Brand: {car['brand']}\n"
        result += f"• Type: {car['body_type']}\n"
        result += f"• Fuel: {car['fuel_type']}\n"
        result += f"• Price: {car['price_range'].replace('_', ' ')}\n"
        result += f"• Luxury: {car['luxury']}\n"
        result += f"• Engine: {car['engine_cc']}cc\n\n"
        result += f"🎯 Guessed in {self.question_count} questions!"
        return result
    
    def _handle_multiple_guesses(self) -> str:
        """Handle case where multiple cars are possible."""
        result = f"\n🤔 I'm down to {len(self.remaining_cars)} possibilities:\n\n"
        
        for i, car in enumerate(self.remaining_cars, 1):
            result += f"{i}. **{car['brand']} {car['model']}** "
            result += f"({car['body_type']}, {car['fuel_type']}, {car['price_range'].replace('_', ' ')})\n"
        
        result += f"\n💭 My best guess is the **{self.remaining_cars[0]['brand']} {self.remaining_cars[0]['model']}**\n"
        result += f"🎯 Questions asked: {self.question_count}"
        return result
    
    def get_game_summary(self) -> str:
        """Get summary of the game session."""
        result = "\n📊 **Game Summary:**\n"
        result += f"• Questions asked: {self.question_count}\n"
        result += f"• Final possibilities: {len(self.remaining_cars)}\n"
        result += f"• Starting database: {len(self.cars)} cars\n\n"
        
        if self.questions_asked:
            result += "❓ **Questions & Answers:**\n"
            for i, (question, answer) in enumerate(zip([q[1] for q in self.questions_asked], self.answers_given), 1):
                result += f"{i}. {question} → **{answer.title()}**\n"
        
        return result


def main():
    """Demo the Car Akinator in terminal."""
    akinator = CarAkinator()
    
    while True:
        akinator.start_game()
        
        # Game loop
        while True:
            question_data = akinator.get_best_question()
            if not question_data:
                break
                
            attribute, question = question_data
            print(f"\n❓ Question {akinator.question_count + 1}: {question}")
            
            answer = input("Your answer (yes/no/don't know): ").strip()
            
            if not akinator.process_answer(answer, question_data):
                break
        
        # Show final result
        print(akinator.make_final_guess())
        print(akinator.get_game_summary())
        
        # Ask if user wants to play again
        play_again = input("\n🎮 Want to play again? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("\n👋 Thanks for playing Car Akinator!")
            break


if __name__ == "__main__":
    main()