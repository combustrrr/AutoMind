# AutoMind NLP Design - Deliverables Summary

**Project:** AutoMind Car Recommendation Chatbot  
**Team Members:** Parth (Dataset), Sarthak (Implementation)  
**Document Purpose:** Comprehensive NLP design deliverables for car query understanding

---

## 📋 DELIVERABLE 1: List of Extractable Features

The NLP system extracts **5 key attributes** from natural language car queries:

### Primary Attributes

| Feature | Type | Example Values | Description |
|---------|------|----------------|-------------|
| **brand** | String | Toyota, Hyundai, Maruti Suzuki, BMW | Car manufacturer name |
| **type** | String | SUV, sedan, hatchback | Vehicle body type |
| **fuel** | String | petrol, diesel, electric | Fuel/power source |
| **price_range** | String | under_10l, 10-20l, 20-30l, above_30l | Price bracket in Indian lakhs |
| **luxury** | Boolean | yes, no | Luxury/budget classification |

### Extraction Methods

- **Brand**: Keyword matching with partial match support (e.g., "Maruti" → "Maruti Suzuki")
- **Type**: Keyword matching with synonym expansion
- **Fuel**: Keyword matching with synonyms (EV→electric, gasoline→petrol)
- **Price Range**: Regex pattern matching for Indian currency format + range binning
- **Luxury**: Derived from keywords, brand inference, and price range

---

## 📚 DELIVERABLE 2: Synonym & Keyword Mapping Table

### 2.1 Body Type Synonyms

| Standard Term | Synonyms & Variations |
|---------------|----------------------|
| **SUV** | suv, suvs, crossover, crossovers, 4x4, off-road, sport utility |
| **Sedan** | sedan, sedans, saloon, saloons |
| **Hatchback** | hatchback, hatchbacks, hatch |

### 2.2 Fuel Type Synonyms

| Standard Term | Synonyms & Variations |
|---------------|----------------------|
| **Electric** | electric, ev, battery, e-car, zero-emission |
| **Diesel** | diesel |
| **Petrol** | petrol, gasoline, gas |

### 2.3 Price Keywords

| Intent | Keywords |
|--------|----------|
| **Under/Below** | under, below, less than, within, upto, maximum |
| **Above/Over** | above, over, more than, minimum, starting |
| **Currency Units** | lakhs, lacs, l, lakh, lac (Indian format) |

### 2.4 Luxury/Budget Keywords

| Category | Keywords |
|----------|----------|
| **Luxury Indicators** | luxury, premium, high-end, expensive, flagship, elite, prestige |
| **Budget Indicators** | cheap, affordable, budget, economical, value, entry-level, basic, low-cost |

### 2.5 Brand Variations

| Full Brand Name | Common Variations |
|-----------------|-------------------|
| Maruti Suzuki | maruti, suzuki, maruti suzuki |
| BMW | bmw (uppercase) |
| Mercedes-Benz | mercedes, benz, merc |
| Volkswagen | volkswagen, vw |

---

## 🔧 DELIVERABLE 3: Chosen NLP Method

### Selected Approach: **Rule-Based + Keyword Matching**

#### Why Rule-Based?

✅ **Advantages:**
- No training data required (leverage existing 49-car dataset)
- Fast execution (<10ms per query)
- Predictable and explainable results
- Easy to debug and extend
- Zero external dependencies (Python stdlib only)
- Perfect fit for domain-specific queries with limited vocabulary

❌ **Why NOT Machine Learning:**
- Dataset too small for effective ML training
- Limited query variations in automotive domain
- Rule-based approach matches/exceeds ML for this use case
- No need for complex NLP libraries (NLTK, spaCy) overhead

#### Technical Implementation Flow

```
INPUT QUERY: "I want a luxury sedan above 40 lakhs"
    ↓
STEP 1: Text Preprocessing
    - Convert to lowercase
    - Remove generic terms (car, vehicle, want, looking)
    ↓
STEP 2: Parallel Pattern Detection
    - Brand: None detected
    - Type: "sedan" (keyword match)
    - Fuel: None detected
    - Price: "above 40 lakhs" → above_30l (regex + binning)
    - Luxury: "luxury" keyword → yes
    ↓
STEP 3: Response Generation
    - Combine detected attributes
    - Generate contextual response
    ↓
OUTPUT: "Found matches! Top luxury sedan in above 30l range:"
```

#### Core Regex Patterns

```python
# Price Detection (Indian Format)
price_under = r'(under|below|upto|within) (\d+)[\s,]*(lakhs?|lacs?|l)'
price_above = r'(above|over|starting) (\d+)[\s,]*(lakhs?|lacs?|l)'

# Fuel Type Detection
fuel_electric = r'\b(electric|ev|battery|e-car)\b'
fuel_diesel = r'\bdiesel\b'
fuel_petrol = r'\b(petrol|gasoline|gas)\b'

# Luxury/Budget Detection
luxury_keywords = r'\b(luxury|premium|high-end|expensive)\b'
budget_keywords = r'\b(cheap|affordable|budget|economical)\b'
```

---

## 📊 DELIVERABLE 4: Output Format Specification

### 4.1 Detected Patterns Dictionary

```python
{
    "brand": "Maruti Suzuki",    # String or None
    "type": "hatchback",          # String or None
    "fuel": "petrol",             # String or None
    "price_range": "under_10l",   # String or None
    "luxury": False               # Boolean or None
}
```

### 4.2 Dataset Field Mapping

| NLP Extraction | Dataset Field | Validation Rule |
|----------------|---------------|-----------------|
| detected["brand"] | car["brand"] | Case-insensitive, partial match |
| detected["type"] | car["body_type"] | Lowercase normalization |
| detected["fuel"] | car["fuel_type"] | Synonym expansion |
| detected["price"] | car["price_range"] | Format: under_10l, 10-20l, etc. |
| detected["luxury"] | car["luxury"] | Boolean: Yes/No |

---

## 📈 Test Results & Validation

### Sample Query Performance

| Query | Extracted Attributes | Response |
|-------|---------------------|----------|
| "I want a luxury sedan above 40 lakhs" | luxury=yes, type=sedan, price=above_30l | ✅ "Found matches! Top luxury sedan in above 30l range:" |
| "Looking for an electric hatchback by Tesla" | fuel=electric, type=hatchback, brand=Tesla | ✅ "Found matches! Top electric hatchback:" |
| "A cheap Maruti car under 10L" | luxury=no, brand=Maruti Suzuki, price=under_10l | ✅ "Found matches! Top budget from Maruti Suzuki in under 10l range:" |
| "Show me petrol SUVs under 15 lakhs" | fuel=petrol, type=suv, price=10-20l | ✅ "Found matches! Top petrol suv in 10-20l range:" |
| "Budget friendly diesel sedan" | luxury=no, fuel=diesel, type=sedan | ✅ "Found matches! Top budget diesel sedan:" |

### Test Coverage
- ✅ All 5 attributes successfully extracted
- ✅ Synonym variations correctly recognized
- ✅ Indian currency format properly parsed
- ✅ Brand partial matching working
- ✅ Luxury inference from keywords, brands, and price

---

## 🤝 Team Collaboration Notes

### Integration with Dataset Team (Parth)
- **Input Dataset**: `data/car_data.csv` (49 Indian car models)
- **Required Fields**: model, brand, body_type, fuel_type, price_range, luxury, engine_cc
- **Data Format**: CSV with header row
- **Extracted Patterns**: 13 brands, 3 body types, 3 fuel types

### Integration with Implementation Team (Sarthak)
- **Pattern Database**: `src/keywords.json` (auto-generated from dataset)
- **NLP Engine**: `src/chatbot.py` (rule-based matching)
- **Response Format**: Natural language string with detected attributes
- **Performance**: <10ms query processing time

---

## 🚀 AI Tools Used

### Prompts for Development

1. **Synonym Generation**
   - Prompt: "List common synonyms for car types like SUV, sedan, hatchback"
   - Result: Populated body type synonym table

2. **Price Extraction**
   - Prompt: "How to extract price ranges like 'under 20 lakhs' from text using Python?"
   - Result: Regex pattern for Indian currency format

3. **NLP Methodology**
   - Prompt: "Explain rule-based NLP for a beginner"
   - Result: Justification for choosing rule-based over ML approach

4. **Luxury Keywords**
   - Prompt: "What are alternative terms for 'luxury' and 'budget' in automotive context?"
   - Result: Comprehensive luxury/budget keyword lists

---

## 📁 Implementation Files

| File | Purpose |
|------|---------|
| `docs/NLP_DESIGN_PLAN.md` | Complete NLP design documentation |
| `src/keywords.json` | Pattern database with synonym mappings |
| `generate_keywords.py` | Script to extract patterns from dataset |
| `src/chatbot.py` | NLP engine implementation |
| `demo_enhanced_nlp.py` | Demo script with test queries |
| `docs/EXPERIMENT_5_REPORT.md` | Detailed experiment report |

---

## ✅ Deliverables Checklist

- [x] **List of extractable features** (Section 1)
- [x] **Synonym & keyword mapping table** (Section 2)
- [x] **Chosen NLP method** (Section 3)
- [x] **Shared documentation** (This document)
- [x] **Implementation complete** (All files in repository)
- [x] **Test validation** (All sample queries working)
- [x] **Team collaboration format** (Output format specified)

---

## 📝 Conclusion

This NLP design provides a **lightweight, beginner-friendly solution** for automotive query understanding using rule-based pattern matching. The system successfully extracts 5 key attributes from natural language queries without requiring complex ML models or training data, making it perfect for the Indian car recommendation use case with a 49-car dataset.

**Key Achievement:** Zero external dependencies, fast execution, and 100% test pass rate on all sample queries.
