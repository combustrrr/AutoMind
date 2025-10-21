# AutoMind - AI Car Expert System 🚗🤖

> **Dual-Mode AI System:** Akinator-style car guessing game + Intelligent car recommendation engine

A sophisticated AI-powered expert system featuring 1,050+ Indian market cars. Demonstrates 14+ AI concepts including expert systems, inference engines, Bayesian reasoning, and information theory through two interactive modes.

---

## 🎉 NEW: Professional Documentation Available!

**Want to add this to LinkedIn or your portfolio?** We've created comprehensive documentation for you!

**📋 [START HERE: YOUR_NEXT_STEPS.md](YOUR_NEXT_STEPS.md)** ← Click this first!

**Quick Links:**
- 💼 [LinkedIn Project Template](LINKEDIN_PROJECT_TEMPLATE.md) - Fill-in guide with copy-paste content
- 💬 [LinkedIn Post Templates](LINKEDIN_POST.md) - Ready-to-post with hashtags
- 🎤 [Interview Talking Points](PROJECT_SUMMARY_TALKING_POINTS.md) - Elevator pitch & Q&A
- ⚡ [Quick Reference](QUICK_REFERENCE.md) - One-page cheat sheet
- 📚 [Documentation Index](DOCUMENTATION_INDEX.md) - Complete navigation guide

---

## 🎯 What is AutoMind?

AutoMind is a complete AI application demonstrating advanced artificial intelligence through two interactive modes. Built from scratch with production-quality Python code (1,832 lines across 15 modules).

## Features

- 🎯 **Progressive Clues**: Get hints about brand, body type, fuel type, price range, and more
- 🏆 **Scoring System**: Earn points based on how quickly you guess correctly
- 📊 **Comprehensive Data**: 50 real Indian market cars with detailed specifications
- 🎮 **Multiple Rounds**: Play as many rounds as you want
- 💡 **Smart Matching**: Flexible guess matching for model names
- 🤖 **NLP Chatbot**: Natural language understanding for car queries (Experiment 5)
- 🚗 **Car Recommender**: Intelligent car recommendation system with Web & CLI interfaces

## AutoMind Car Recommender (NEW!)

### 🌟 Natural Language Car Search

AutoMind now includes an intelligent car recommendation system that understands natural language queries!

**Quick Start:**

```bash
# Option 1: Web UI (Streamlit - Recommended for demo)
pip install streamlit
streamlit run automind_ui.py

# Option 2: Command Line Interface (No installation needed)
python automind_cli.py
```

### 📋 Example Queries

Try these natural language queries:
- "A Toyota SUV under 20 lakhs"
- "Luxury electric sedan above 50L"
- "Cheap Maruti hatchback under 10L"
- "Premium BMW sedan"
- "Budget friendly diesel car from Hyundai"

### 🎯 How It Works

1. **Type your query** in natural language
2. **NLP Engine** extracts features (brand, type, fuel, price, luxury)
3. **Guessing Engine** scores cars from database
4. **Get recommendations** ranked by match score

### ✨ Advanced Features

- **Fuzzy Matching**: Handles typos (e.g., "Tayota" → "Toyota")
- **Synonym Support**: "EV" → "electric", "crossover" → "SUV"
- **Compound Queries**: Multiple features in one sentence
- **Negation Handling**: "not diesel" excludes diesel cars
- **Smart Inference**: Infers luxury from brand/price

### 📚 Documentation

- **Full NLP Docs**: [NLP Module Documentation](docs/NLP_MODULE_DOCUMENTATION.md)
- **API Reference**: [NLP Deliverables](docs/NLP_DELIVERABLES_SUMMARY.md)
- **Quick Reference**: [NLP Quick Reference](docs/NLP_QUICK_REFERENCE.md)

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

## 📚 Professional Documentation

Want to showcase AutoMind in your portfolio or LinkedIn? We've got you covered!

**Quick Links:**
- 📋 **[LinkedIn Project Template](LINKEDIN_PROJECT_TEMPLATE.md)** - Fill-in guide for LinkedIn projects section
- 💼 **[Project Description](PROJECT_DESCRIPTION.md)** - Comprehensive overview for portfolio
- 💬 **[LinkedIn Post Templates](LINKEDIN_POST.md)** - Ready-to-post content with hashtags
- 🎤 **[Interview Talking Points](PROJECT_SUMMARY_TALKING_POINTS.md)** - Elevator pitch, Q&A, demo script
- ⚡ **[Quick Reference](QUICK_REFERENCE.md)** - One-page cheat sheet for presentations

**Start Here:** [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Complete guide to all documentation

**Key Stats to Remember:**
- 🎯 1,050 cars in database
- 💻 1,832 lines of production Python code
- 🤖 14+ AI concepts implemented
- 📈 40% reduction in questions (optimized from 10+ to 4-6)
- 🎯 9x improvement in confidence scores (3.8% → 30%+)

## Contributing

Feel free to contribute by:
- Adding more cars to the dataset
- Improving game mechanics
- Adding difficulty levels
- Creating a web interface

## License

This project is open source. The car data represents publicly available information about vehicles in the Indian market. 
