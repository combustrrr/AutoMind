# AutoMind - AI-Powered Car Recommendation System 🚗🤖

An intelligent car recommendation system demonstrating **classic AI techniques** (Expert Systems, Knowledge Representation, Inference Engines) alongside modern **Machine Learning**. Perfect for AI coursework and educational purposes.

## 🎓 AI Techniques Demonstrated

### Classic AI (Expert System)
- ✅ **Knowledge Base** - Frame-based representation with 50+ cars
- ✅ **Inference Engine** - Forward chaining, rule-based reasoning
- ✅ **Information Gain** - Optimal question selection using entropy
- ✅ **Belief State Management** - Probabilistic reasoning, uncertainty handling
- ✅ **Symbolic AI** - Explainable, traceable decision-making

### Machine Learning
- ✅ **TF-IDF Vectorization** - Text feature extraction
- ✅ **Random Forest Classifier** - Multi-class car prediction
- ✅ **Confidence Scoring** - Probabilistic predictions
- ✅ **Training Pipeline** - Data generation and model training

### NLP & Context Awareness
- ✅ **Natural Language Processing** - Query understanding
- ✅ **Fuzzy Matching** - Typo tolerance (Levenshtein distance)
- ✅ **Context Stack** - Multi-turn conversations
- ✅ **Preference Learning** - User preference tracking

## 🚀 Quick Start

### Expert System (Recommended for AI Coursework)

```bash
# Interactive expert system using AI reasoning
python expert_system_cli.py
```

**What makes it "True AI":**
- Uses information theory (entropy, information gain)
- Forward chaining inference engine
- Knowledge-based reasoning
- Fully explainable decisions

### Dataset Expansion (NEW!)

Expand from 50 to 100s+ cars using real Kaggle data:

```bash
# Install dependencies
pip install kagglehub pandas

# Download and integrate CardDekho dataset
python download_kaggle_dataset.py
```

See `KAGGLE_DATASET_GUIDE.md` for details.

### Natural Language Interface
- **Synonym Support**: "EV" → "electric", "crossover" → "SUV"
- **Compound Queries**: Multiple features in one sentence
- **Negation Handling**: "not diesel" excludes diesel cars
- **Smart Inference**: Infers luxury from brand/price
- **🆕 Smart Clarification**: Asks for details when confidence is low (< 30%)
- **🆕 Preference Learning**: Remembers what you like across conversation
- **🆕 Conversation Repair**: Helpful guidance when queries are unclear
- **🆕 Machine Learning**: Actual ML-powered predictions with confidence scores

### 📚 Documentation

- **Full NLP Docs**: [NLP Module Documentation](docs/NLP_MODULE_DOCUMENTATION.md)
- **API Reference**: [NLP Deliverables](docs/NLP_DELIVERABLES_SUMMARY.md)
- **Quick Reference**: [NLP Quick Reference](docs/NLP_QUICK_REFERENCE.md)
- **🆕 RISC AI Enhancements**: [RISC AI Enhancements](docs/RISC_AI_ENHANCEMENTS.md)
- **🆕 ML Integration**: [Machine Learning Integration](docs/ML_INTEGRATION.md)

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
