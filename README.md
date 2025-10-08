# AutoMind - Guess the Car Game 🚗

A fun and interactive car guessing game featuring 50 popular Indian market cars. Test your automotive knowledge by identifying cars from clues about their brand, specifications, and characteristics.

## Features

- 🎯 **Progressive Clues**: Get hints about brand, body type, fuel type, price range, and more
- 🏆 **Scoring System**: Earn points based on how quickly you guess correctly
- 📊 **Comprehensive Data**: 50 real Indian market cars with detailed specifications
- 🎮 **Multiple Rounds**: Play as many rounds as you want
- 💡 **Smart Matching**: Flexible guess matching for model names
- 🤖 **NLP Chatbot**: Natural language understanding for car queries (Experiment 5)

## NLP Query System (Experiment 5)

AutoMind includes an advanced NLP-based chatbot that understands natural language car queries:

### Supported Query Types
- **Brand + Type**: "Show me Maruti hatchbacks"
- **Fuel + Budget**: "Affordable electric cars under 20 lakhs"
- **Luxury + Price**: "Premium sedans above 30 lakhs"
- **Complex Queries**: "Cheap diesel SUV from Tata under 15L"

### Extractable Attributes
- **brand**: Toyota, Hyundai, Maruti Suzuki, BMW, etc.
- **type**: SUV, sedan, hatchback
- **fuel**: petrol, diesel, electric (supports synonyms like "EV", "gasoline")
- **price_range**: under_10l, 10-20l, 20-30l, above_30l
- **luxury**: Inferred from keywords (luxury/budget) or price range

### Try the NLP Chatbot
```bash
# Run the interactive NLP demo
python3 demo_enhanced_nlp.py

# Verify all NLP deliverables
python3 verify_nlp_deliverables.py
```

📄 **Full Documentation**: See [NLP Deliverables Summary](docs/NLP_DELIVERABLES_SUMMARY.md)

## How to Play

1. **Start the Game**: Run the game and you'll be presented with a mystery car
2. **Get Clues**: Type `hint` to receive progressive clues about the car
3. **Make Guesses**: Type your guess for the car model name
4. **Score Points**: Earn more points for guessing correctly with fewer attempts
5. **Play Again**: Continue with new cars or quit anytime

## Installation & Usage

### Prerequisites
- Python 3.6 or higher

### Running the Game
```bash
# Clone the repository or download the files
git clone <repository-url>
cd AutoMind

# Run the game
python3 automind.py
```

### Running Tests
```bash
# Run the test suite to verify everything works
python3 test_automind.py
```

## Game Commands

- **`hint`** - Get a clue about the current car
- **`quit`** - Exit the game
- **Car model name** - Your guess (e.g., "Swift", "Creta", "Fortuner")

## Scoring

- 🥇 **1 attempt**: 100 points (Perfect!)
- 🥈 **2 attempts**: 75 points (Excellent!)
- 🥉 **3 attempts**: 50 points (Good!)
- 📖 **4 attempts**: 25 points (Fair)
- 💪 **5 attempts**: 10 points (Just made it!)

## Data Source

The game uses a curated dataset of 50 popular Indian market cars including:
- Maruti Suzuki, Hyundai, Tata, Mahindra, Honda, Toyota, and more
- Hatchbacks, Sedans, and SUVs
- Petrol, Diesel, and Electric vehicles
- Price ranges from under ₹10 lakhs to above ₹30 lakhs

## File Structure

```
AutoMind/
├── automind.py              # Main game application
├── test_automind.py         # Test suite
├── requirements.txt         # Dependencies (Python standard library only)
├── README.md               # This file
├── generate_keywords.py    # NLP pattern extraction script
├── demo_enhanced_nlp.py    # NLP chatbot demo
├── verify_nlp_deliverables.py # Deliverables verification
├── data/
│   ├── car_data.csv        # Original car dataset
│   ├── car_data_enriched.csv # Enhanced dataset with keywords
│   └── data_validation_log.txt # Data processing log
├── src/
│   ├── chatbot.py          # NLP engine implementation
│   └── keywords.json       # Pattern database with synonyms
└── docs/
    ├── DATA_DICTIONARY.md  # Comprehensive data documentation
    ├── NLP_DESIGN_PLAN.md  # Complete NLP design documentation
    ├── NLP_DELIVERABLES_SUMMARY.md # NLP deliverables summary
    └── EXPERIMENT_5_REPORT.md # Experiment report
```

## Example Gameplay

```
🚗 GUESS THE CAR - Round 1
==================================================
I'm thinking of a car... You have 5 attempts to guess it!

Attempt 1/5
Your guess (or 'hint'/'quit'): hint
💡 Clue: 🏢 Brand: This car is made by Hyundai

Attempt 1/5
Your guess (or 'hint'/'quit'): Creta
🎉 Correct! The car was: Creta
You got it in 1 attempt(s)!
Round score: +100 points
```

## Contributing

Feel free to contribute by:
- Adding more cars to the dataset
- Improving game mechanics
- Adding difficulty levels
- Creating a web interface

## License

This project is open source. The car data represents publicly available information about vehicles in the Indian market. 
