# NLP Design Plan for AutoMind Car Query System

**Project:** AutoMind Car Recommendation Chatbot  
**Developer:** Sarthak Kulkarni (Roll No: 23101B0019)  
**Subject:** Artificial Intelligence (Experiment 5)  
**Approach:** Rule-Based Pattern Matching + Keyword Extraction  

---

## 1. PROBLEM ANALYSIS

### Sample User Inputs:
1. **"I want a luxury sedan above 40 lakhs."**
   - Extract: luxury=yes, type=sedan, price_range=above_30l
   
2. **"Looking for an electric hatchback by Tesla."**
   - Extract: fuel=electric, type=hatchback, brand=tesla
   
3. **"A cheap Maruti car under 10L."**
   - Extract: luxury=no (cheap implies budget), brand=maruti, price_range=under_10l

4. **"Show me petrol SUVs under 15 lakhs"**
   - Extract: fuel=petrol, type=suv, price_range=10-20l

5. **"Budget friendly diesel sedan"**
   - Extract: luxury=no, fuel=diesel, type=sedan

---

## 2. EXTRACTABLE FEATURES

### 2.1 Primary Attributes (from car_data.csv)
| Attribute | Type | Example Values | Extraction Method |
|-----------|------|----------------|-------------------|
| **brand** | String | Toyota, Hyundai, Maruti Suzuki, BMW | Keyword matching with partial match support |
| **type** | String | SUV, sedan, hatchback | Keyword matching with synonyms |
| **fuel** | String | petrol, diesel, electric | Keyword matching with synonyms (EV→electric) |
| **price_range** | String | under_10l, 10-20l, 20-30l, above_30l | Regex for Indian currency (lakhs) + range binning |
| **luxury** | Boolean | yes, no | Derived from keywords + price range inference |

### 2.2 Derived Attributes
- **luxury**: Determined by:
  - Explicit keywords: "luxury", "premium", "high-end", "expensive"
  - Budget keywords (opposite): "cheap", "affordable", "budget", "economical"
  - Price inference: above_30l → likely luxury, under_10l → budget
  - Brand inference: BMW, Mercedes, Audi → luxury brands

---

## 3. SYNONYM & KEYWORD MAPPING TABLE

### 3.1 Body Type Synonyms
| Standard Term | Synonyms/Variations |
|---------------|---------------------|
| **SUV** | suv, sport utility, crossover, 4x4, off-road |
| **sedan** | sedan, saloon, 4-door |
| **hatchback** | hatchback, hatch, compact car, city car |

### 3.2 Fuel Type Synonyms
| Standard Term | Synonyms/Variations |
|---------------|---------------------|
| **petrol** | petrol, gasoline, gas |
| **diesel** | diesel |
| **electric** | electric, ev, battery, e-car, zero-emission |

### 3.3 Price-Related Keywords
| Intent | Keywords |
|--------|----------|
| **Under/Below** | under, below, less than, within, upto, maximum |
| **Above/Over** | above, over, more than, minimum, starting |
| **Currency Units** | lakhs, lacs, l, lakh, lac (Indian format) |

### 3.4 Luxury/Budget Keywords
| Category | Keywords |
|----------|----------|
| **Luxury Indicators** | luxury, premium, high-end, expensive, top-tier, flagship, elite, prestige |
| **Budget Indicators** | cheap, affordable, budget, economical, value, entry-level, basic, low-cost |

### 3.5 Brand Name Variations
| Full Brand Name | Common Variations |
|-----------------|-------------------|
| Maruti Suzuki | maruti, suzuki, maruti suzuki |
| BMW | bmw, beemer |
| Mercedes-Benz | mercedes, benz, merc |
| Volkswagen | volkswagen, vw |
| Tata Motors | tata |

---

## 4. CHOSEN NLP METHOD

### 4.1 Approach: **Rule-Based + Keyword Matching** (Beginner-Friendly, Fast)

**Why Rule-Based?**
- ✅ No training data required (leverage existing dataset)
- ✅ Fast execution (<1ms per query)
- ✅ Predictable, explainable results
- ✅ Easy to debug and extend
- ✅ Works well for domain-specific queries with limited vocabulary

**Why NOT Machine Learning?**
- Dataset too small (49 car models) for effective ML training
- Limited query variations in automotive domain
- Rule-based matches/exceeds ML for this use case
- No need for complex NLP libraries (NLTK, spaCy) overhead

### 4.2 Technical Implementation

```
INPUT QUERY: "I want a luxury electric sedan above 40 lakhs"
    ↓
STEP 1: Text Preprocessing
    - Convert to lowercase: "i want a luxury electric sedan above 40 lakhs"
    - Tokenize (implicit in regex matching)
    ↓
STEP 2: Pattern Detection (Parallel)
    - Brand: None detected
    - Type: "sedan" (keyword match)
    - Fuel: "electric" (keyword match)
    - Price: "above 40 lakhs" → above_30l (regex + binning)
    - Luxury: "luxury" keyword → yes
    ↓
STEP 3: Response Generation
    - Combine detected patterns
    - Query dataset for matches
    - Generate contextual response
    ↓
OUTPUT: "Found luxury electric sedans in above 30l range: [matching models]"
```

### 4.3 Regex Patterns Used

```python
# Price Detection (Indian Format)
price_under = r'(under|below|upto|within) (\d+)[\s,]*(lakhs?|lacs?|l)'
price_above = r'(above|over|starting) (\d+)[\s,]*(lakhs?|lacs?|l)'

# Brand Detection (Word Boundary)
brand_pattern = r'\b{brand_name}\b'

# Fuel Type Detection
fuel_electric = r'\b(electric|ev|battery|e-car)\b'
fuel_diesel = r'\bdiesel\b'
fuel_petrol = r'\b(petrol|gasoline|gas)\b'

# Luxury Detection
luxury_keywords = r'\b(luxury|premium|high-end|expensive|flagship)\b'
budget_keywords = r'\b(cheap|affordable|budget|economical|value)\b'
```

---

## 5. ALGORITHM FLOWCHART

```
START
  ↓
INPUT: User query text
  ↓
LOAD: Pattern database (keywords.json)
  ↓
NORMALIZE: Convert query to lowercase
  ↓
EXTRACT PATTERNS (Parallel Processing):
  ├─→ Brand Extraction (loop through brand list)
  ├─→ Body Type Extraction (loop through type list)
  ├─→ Fuel Type Extraction (keyword + synonym matching)
  ├─→ Price Range Extraction (regex + binning logic)
  └─→ Luxury/Budget Detection (keywords + price inference)
  ↓
VALIDATION: Check which patterns were detected
  ↓
RESPONSE GENERATION:
  ├─→ All 5 patterns? → "Complete match found: [details]"
  ├─→ 3-4 patterns? → "Partial match: [details] + Ask for missing info"
  ├─→ 1-2 patterns? → "Limited info: [details] + Suggest more criteria"
  └─→ 0 patterns? → "Try: 'Brand Type Fuel under XX lakhs'"
  ↓
OUTPUT: Response string
  ↓
END
```

---

## 6. DATA INTEGRATION WITH EXISTING DATASET

### 6.1 Dataset Fields (car_data.csv)
```csv
model,brand,body_type,fuel_type,price_range,luxury,engine_cc
Swift,Maruti Suzuki,Hatchback,Petrol,under_10L,No,1197
X5,BMW,SUV,Diesel,above_30L,Yes,2998
```

### 6.2 Field Mapping
| Dataset Field | NLP Extraction | Validation |
|---------------|----------------|------------|
| brand | Detected brand → Match dataset brand | Case-insensitive, partial match |
| body_type | Detected type → Match dataset body_type | Lowercase normalization |
| fuel_type | Detected fuel → Match dataset fuel_type | Synonym expansion |
| price_range | Detected price_range → Match dataset price_range | Format: under_10L, 10-20L, etc. |
| luxury | Detected luxury flag → Match dataset luxury | Yes/No boolean |

### 6.3 Query → Dataset Filtering Logic
```python
def filter_cars(detected_patterns, car_database):
    """Filter car dataset based on detected patterns"""
    filtered = car_database
    
    if detected_patterns['brand']:
        filtered = [car for car in filtered 
                   if car['brand'].lower() == detected_patterns['brand'].lower()]
    
    if detected_patterns['type']:
        filtered = [car for car in filtered 
                   if car['body_type'].lower() == detected_patterns['type'].lower()]
    
    if detected_patterns['fuel']:
        filtered = [car for car in filtered 
                   if car['fuel_type'].lower() == detected_patterns['fuel'].lower()]
    
    if detected_patterns['price_range']:
        filtered = [car for car in filtered 
                   if car['price_range'] == detected_patterns['price_range']]
    
    if detected_patterns['luxury'] is not None:
        luxury_val = "Yes" if detected_patterns['luxury'] else "No"
        filtered = [car for car in filtered 
                   if car['luxury'] == luxury_val]
    
    return filtered
```

---

## 7. DELIVERABLES CHECKLIST

- [x] **List of extractable features**: brand, type, fuel, price_range, luxury (Section 2)
- [x] **Synonym & keyword mapping table**: Complete mapping for all categories (Section 3)
- [x] **Chosen NLP method**: Rule-based + Keyword Matching with justification (Section 4)
- [ ] **Enhanced chatbot implementation**: Add fuel and luxury extraction to chatbot.py
- [ ] **Updated keywords.json**: Include fuel synonyms and luxury keywords
- [ ] **Test cases**: Cover all 5 attributes with various synonym combinations
- [ ] **Performance validation**: Test against sample queries from Section 1

---

## 8. AI TOOLS USAGE PROMPTS

### 8.1 Synonym Generation
**Prompt**: *"List common synonyms for car types like SUV, sedan, hatchback."*
- Result: Used to populate Section 3.1 body type synonyms

**Prompt**: *"What are alternative terms for 'luxury' and 'budget' in automotive context?"*
- Result: Used to populate Section 3.4 luxury/budget keywords

### 8.2 Price Extraction
**Prompt**: *"How to extract price ranges like 'under 20 lakhs' from text using Python?"*
- Result: Regex pattern `r'(under|below) (\d+)[\s,]*(lakhs?|lacs?)'` in Section 4.3

### 8.3 NLP Methodology
**Prompt**: *"Explain rule-based NLP for a beginner."*
- Result: Justification in Section 4.1 comparing rule-based vs ML approach

---

## 9. COLLABORATION INTERFACES

### 9.1 With Dataset Team (Sarthak's Previous Work)
- **Input**: `car_data.csv` with 49 Indian car models
- **Usage**: Extract unique values for brands, body_types, fuel_types
- **Validation**: Ensure extracted patterns match dataset format (e.g., "under_10L" not "under_10l")

### 9.2 Output Format for Query Processing
```python
{
    "brand": "Maruti Suzuki",      # String or None
    "type": "hatchback",            # String or None
    "fuel": "petrol",               # String or None
    "price_range": "under_10l",     # String or None
    "luxury": False                 # Boolean or None
}
```

### 9.3 Response Format
```python
{
    "status": "complete_match",     # complete_match | partial_match | no_match
    "detected": {...},              # Detected patterns dictionary
    "message": "Found 5 matches...", # Human-readable response
    "suggestions": []                # Missing criteria (if partial)
}
```

---

## 10. TESTING STRATEGY

### 10.1 Test Categories
1. **Single Attribute Queries**
   - "Show me Maruti cars"
   - "I want a sedan"
   - "Electric vehicles only"

2. **Multi-Attribute Queries**
   - "Maruti hatchback under 10 lakhs"
   - "Luxury diesel SUV"
   - "Affordable electric car"

3. **Synonym Variations**
   - "EV" → electric
   - "cheap" → budget (luxury=no)
   - "crossover" → SUV

4. **Edge Cases**
   - Misspellings: "maruthi" (should still match Maruti)
   - Multiple prices: "under 20 lakhs but above 10" → 10-20l range
   - Conflicting terms: "luxury budget car" → prioritize explicit keywords

### 10.2 Validation Metrics
- **Precision**: % of extracted patterns that are correct
- **Recall**: % of query patterns successfully extracted
- **Response Time**: Should be <10ms per query
- **Coverage**: % of dataset searchable via NLP patterns

---

## 11. IMPLEMENTATION ROADMAP

### Phase 1: Enhanced Pattern Extraction (30 mins)
- [x] Document NLP design plan
- [ ] Add fuel_types to keywords.json extraction
- [ ] Add synonym mappings for fuel types
- [ ] Add luxury/budget keyword lists

### Phase 2: Chatbot Enhancement (45 mins)
- [ ] Implement fuel type detection in chatbot.py
- [ ] Implement luxury/budget detection logic
- [ ] Update response generation for 5 attributes
- [ ] Add synonym matching support

### Phase 3: Testing & Validation (30 mins)
- [ ] Create comprehensive test suite
- [ ] Test all sample queries from Section 1
- [ ] Validate against car_data.csv dataset
- [ ] Document test results

### Phase 4: Documentation (15 mins)
- [ ] Update Experiment 5 report with new features
- [ ] Add outputs showing fuel and luxury extraction
- [ ] Include performance metrics for enhanced system

---

## 12. CONCLUSION

This NLP design leverages a **lightweight rule-based approach** optimized for the Indian automotive domain. By combining regex pattern matching with synonym expansion and domain knowledge, the system can extract 5 key attributes (brand, type, fuel, price_range, luxury) from natural language queries without requiring complex ML models or training data.

**Key Advantages:**
- Zero external dependencies (Python stdlib only)
- Fast execution (<10ms per query)
- Explainable results (every extraction has a clear rule)
- Easy to extend (add synonyms, brands, or patterns)
- Perfect fit for 49-car dataset with limited query variations

**Next Steps:** Implement enhanced chatbot with fuel and luxury extraction as per this design plan.
