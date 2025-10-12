# AutoMind NLP Module Documentation

## Overview

The AutoMind NLP (Natural Language Processing) module enables the car recommendation system to understand natural language user queries and extract structured features for car matching.

## Architecture

```
User Input → NLP Engine → Feature Dictionary → Guessing Engine → Car Recommendations
                ↓              ↓                    ↓
         Confidence Score  Preferences      Smart Clarification
```

### Components

1. **nlp_engine.py** - Extracts features from text with AI enhancements
2. **guessing_engine.py** - Matches features to cars
3. **automind_ui.py** - Streamlit web interface
4. **automind_cli.py** - Command-line interface

### RISC AI Enhancements

The NLP Engine implements three intelligent enhancements:

1. **Smart Clarification** - Asks for details when confidence < 30%
2. **Preference Learning** - Tracks user preferences across conversation
3. **Conversation Repair** - Provides helpful guidance for unclear queries

See [RISC AI Enhancements](RISC_AI_ENHANCEMENTS.md) for detailed documentation.

## NLP Engine (`nlp_engine.py`)

### Main Function: `extract_features(text)`

Extracts structured car features from natural language input.

**Input:** String (user query)

**Output:** Dictionary with keys:
- `brand` (str or None): Car manufacturer
- `type` (str or None): Body type (SUV, Sedan, Hatchback)
- `fuel` (str or None): Fuel type (petrol, diesel, electric)
- `price_range` (str or None): Price bracket
- `luxury` (bool or None): Luxury status

**Example:**
```python
from nlp_engine import extract_features

features = extract_features("A Toyota SUV under 20 lakhs")
# Returns:
# {
#     'brand': 'Toyota',
#     'type': 'suv',
#     'fuel': None,
#     'price_range': 'under_20L',
#     'luxury': None
# }
```

### Supported Features

#### 1. Brand Detection
- **Direct matching**: Recognizes brands from dataset
- **Fuzzy matching**: Handles typos (e.g., "Tayota" → "Toyota")
- **Partial matching**: "Maruti" matches "Maruti Suzuki"

**Supported Brands:**
- Maruti Suzuki, Hyundai, Tata, Toyota, Honda, Mahindra
- BMW, Mercedes, Audi, Tesla, and more

#### 2. Body Type Detection
- **Types**: SUV, Sedan, Hatchback
- **Synonyms**:
  - SUV: crossover, 4x4, off-road
  - Sedan: saloon
  - Hatchback: hatch, compact

#### 3. Fuel Type Detection
- **Types**: Petrol, Diesel, Electric
- **Synonyms**:
  - Electric: EV, battery, e-car, zero-emission
  - Petrol: gasoline, gas

#### 4. Price Range Detection
- **Regex patterns**: Extracts "under 20L", "above 50 lakhs", "around 15L"
- **Price bins**:
  - under_10L
  - 10-20L (also under_20L)
  - 20-30L (also under_30L)
  - above_30L

#### 5. Luxury Status Detection
- **Luxury keywords**: luxury, premium, high-end, expensive, flagship
- **Budget keywords**: cheap, affordable, budget, economical
- **Brand inference**: BMW, Mercedes → luxury
- **Price inference**: above 30L → luxury, under 10L → budget

### Advanced Features

#### Smart Clarification (NEW!)
Provides guidance when confidence is low (< 30%):
```python
extract_features("a car")
# Console output:
#   Confidence: 0.0%
#   Suggestion: I could use more details. Consider specifying:
#               brand (e.g., Toyota, Hyundai, Maruti),
#               type (SUV, sedan, or hatchback)
```

#### Preference Learning (NEW!)
Tracks user preferences across queries:
```python
from nlp_engine import extract_features, get_preferences

extract_features("electric car")
extract_features("Toyota SUV")

prefs = get_preferences()
# Returns:
# {
#     'prefers_electric': True,
#     'prefers_suv': True,
#     'preferred_brands': ['Toyota'],
#     'price_sensitivity': None
# }
```

#### Conversation Repair (NEW!)
Helps users formulate better queries:
```python
from nlp_engine import handle_confusion

message = handle_confusion()
# Returns: "I'm not sure I understand. Could you mention the brand 
#           name or car type? For example: 'Toyota SUV' or 'luxury sedan'"
```

#### Negation Handling
Detects "not", "no", "without" patterns:
```python
extract_features("not diesel, petrol car")
# Won't extract diesel, will extract petrol
```

#### Compound Queries
Handles multiple features in one query:
```python
extract_features("A luxury electric sedan by Tesla above 50 lakhs")
# Extracts: brand=Tesla, type=sedan, fuel=electric, 
#           price_range=above_30L, luxury=True
```

#### Fuzzy Matching
Uses `difflib` to match misspellings:
```python
extract_features("Tayota Fortuner")
# Corrects to: brand=Toyota
```

## Guessing Engine (`guessing_engine.py`)

### Main Class: `GuessingEngine`

Scores and ranks cars based on extracted features.

#### Methods

**`score_car(car, features)`**
- Scores a single car against features
- Returns integer score (0-100)
- Scoring weights:
  - Brand match: 30 points
  - Body type match: 20 points
  - Fuel type match: 20 points
  - Price range match: 15 points
  - Luxury status match: 15 points

**`find_matches(features, top_n=5)`**
- Returns top N matching cars
- Returns list of (car, score) tuples
- Sorted by score descending

**`get_best_guess(features)`**
- Returns single best matching car
- Returns None if no matches

**`suggest_followup_question(features)`**
- Analyzes missing features
- Returns suggestion string

**Example:**
```python
from guessing_engine import GuessingEngine

engine = GuessingEngine()
features = {'brand': 'Toyota', 'type': 'suv'}

matches = engine.find_matches(features, top_n=3)
for car, score in matches:
    print(f"{car['model']}: {score} points")
```

## User Interfaces

### Web UI (`automind_ui.py`)

**Requirements:** `pip install streamlit`

**Run:** `streamlit run automind_ui.py`

**Features:**
- Interactive web interface
- Real-time feature extraction display
- Match score visualization
- Search history
- Responsive design

**Usage:**
```bash
streamlit run automind_ui.py
# Opens browser at http://localhost:8501
```

### CLI (`automind_cli.py`)

**Requirements:** None (uses only standard library)

**Run:** `python automind_cli.py`

**Features:**
- Command-line interface
- No external dependencies
- Batch query support
- Works on any terminal

**Commands:**
- Type your query
- `help` - Show examples
- `quit` or `exit` - Exit program

## Testing

### Test Suite (`test_nlp.py`)

Comprehensive test suite with 10 diverse test cases.

**Run:** `python test_nlp.py`

**Tests:**
1. Brand + Type + Price extraction
2. Luxury + Brand + Type + Price
3. Budget + Brand + Type + Price
4. Brand + Type + Fuel
5. Type + Luxury + Price
6. Type + Fuel + Price
7. Brand + Type + Fuel + Luxury
8. Compound query with all features
9. Negation handling
10. Fuzzy matching (typo correction)

**Output:**
- Pass/fail for each test
- Summary statistics
- Feature demonstrations

## Examples

### Example 1: Simple Query
```python
Input: "Toyota Fortuner"
Output: {
    'brand': 'Toyota',
    'type': None,
    'fuel': None,
    'price_range': None,
    'luxury': None
}
```

### Example 2: Complex Query
```python
Input: "A luxury electric sedan by Tesla above 50 lakhs"
Output: {
    'brand': 'Tesla',
    'type': 'sedan',
    'fuel': 'electric',
    'price_range': 'above_30L',
    'luxury': True
}
```

### Example 3: Budget Query
```python
Input: "Cheap Maruti hatchback under 10L"
Output: {
    'brand': 'Maruti Suzuki',
    'type': 'hatchback',
    'fuel': None,
    'price_range': 'under_10L',
    'luxury': False
}
```

### Example 4: Synonym Usage
```python
Input: "EV crossover with gasoline backup"
Output: {
    'brand': None,
    'type': 'suv',  # crossover → suv
    'fuel': 'electric',  # EV → electric
    'price_range': None,
    'luxury': None
}
```

## Supported Keywords

### Brand Keywords
All brands from dataset + BMW, Audi, Mercedes, Tesla, Lexus, Jaguar, Volvo

### Type Synonyms
- **SUV**: suv, suvs, crossover, crossovers, 4x4, off-road, sport utility
- **Sedan**: sedan, sedans, saloon, saloons
- **Hatchback**: hatchback, hatchbacks, hatch, compact

### Fuel Synonyms
- **Electric**: electric, ev, battery, e-car, zero-emission, e-vehicle
- **Diesel**: diesel
- **Petrol**: petrol, gasoline, gas

### Price Keywords
- **Under**: under, below, upto, within, less than, maximum
- **Above**: above, over, more than, starting, minimum
- **Around**: around, approximately, about

### Luxury Keywords
- **Luxury**: luxury, premium, high-end, expensive, flagship, elite, prestige
- **Budget**: cheap, affordable, budget, economical, value, entry-level, basic, low-cost

## Performance

- **Processing Time**: <10ms per query (NLP extraction)
- **Accuracy**: 80%+ on test suite
- **False Positives**: Minimal due to strict matching
- **Fuzzy Match Threshold**: 75% similarity

## Debugging

Enable debug output by checking console logs:
```python
extract_features("your query")
# Prints: [NLP Engine] Input: 'your query'
# Prints: [NLP Engine] Detected: {...}
```

## Error Handling

### Common Issues

1. **No matches found**
   - Solution: Provide more specific features
   - System suggests follow-up questions

2. **Typo not corrected**
   - Fuzzy matching requires 75%+ similarity
   - Try different spelling or use correct brand name

3. **Wrong price range**
   - Check price format: "under 20L" or "20 lakhs"
   - Supported: lakhs, lacs, L

## Integration Guide

### Step 1: Extract Features
```python
from nlp_engine import extract_features

features = extract_features(user_input)
```

### Step 2: Find Matches
```python
from guessing_engine import GuessingEngine

engine = GuessingEngine()
matches = engine.find_matches(features, top_n=5)
```

### Step 3: Display Results
```python
for car, score in matches:
    print(f"{car['brand']} {car['model']}: {score} points")
```

## Dataset Format

Expected CSV columns:
- `model`: Car model name
- `brand`: Manufacturer name
- `body_type`: SUV, Sedan, or Hatchback
- `fuel_type`: Petrol, Diesel, or Electric
- `price_range`: under_10L, 10-20L, 20-30L, above_30L
- `luxury`: Yes or No

## Future Enhancements

1. **Multi-language support** (Hindi, regional languages)
2. **Voice input integration**
3. **More fuel types** (Hybrid, CNG)
4. **Year/model year filtering**
5. **Safety ratings**
6. **Mileage preferences**
7. **Seating capacity**
8. **Color preferences**

## Credits

Developed for AutoMind Car Recommendation System
- NLP Engine: Rule-based pattern matching with fuzzy matching
- Dataset: Indian car market (50 cars)
- Technologies: Python 3.6+, Streamlit (optional)
