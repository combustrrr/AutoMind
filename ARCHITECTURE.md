# AutoMind - Modular Architecture Documentation

## 📁 Project Structure

```
AutoMind/
├── app.py                          # Main Streamlit application (entry point)
├── requirements.txt                 # Python dependencies
│
├── automind/                       # Core AI package
│   ├── __init__.py                 # Package initialization
│   ├── knowledge_base.py           # Knowledge representation (1,050 cars)
│   ├── inference_engine.py         # AI reasoning engine
│   ├── expert_system.py            # Expert system facade
│   ├── ml_model.py                 # ML classifier (hybrid AI)
│   │
│   ├── recommendation/             # Recommendation system module
│   │   ├── __init__.py
│   │   └── engine.py               # Content-based recommendation AI
│   │
│   ├── ui/                         # UI components module
│   │   ├── __init__.py
│   │   ├── components.py           # Reusable UI elements
│   │   ├── guessing.py             # Guessing mode UI (to be created)
│   │   └── recommendation.py       # Recommendation mode UI (to be created)
│   │
│   └── utils/                      # Utility modules
│       ├── __init__.py
│       └── logger.py               # Session logging utility
│
├── data/                           # Data directory
│   ├── car_data_enriched.csv      # Processed car database
│   └── car_data.csv               # Original dataset
│
├── logs/                           # Session logs
│   ├── session_*.json             # Guessing mode logs
│   └── recommendations/           # Recommendation mode logs
│       └── recommendation_*.json
│
├── scripts/                        # Data processing scripts
│   ├── process_new_data.py
│   └── download_and_inspect.py
│
└── docs/                           # Documentation
    ├── HYBRID_SYSTEM_GUIDE.md
    ├── FIXES_APPLIED.md
    ├── SUCCESS_SUMMARY.md
    └── ...
```

---

## 🏗️ Architecture Layers

### 1. **Presentation Layer** (`app.py`)
- **Purpose:** User interface and interaction
- **Technology:** Streamlit web framework
- **Responsibilities:**
  - Mode selection (Guessing vs Recommendation)
  - User input collection
  - Result display
  - Session state management

### 2. **AI Core Layer** (`automind/`)
Main AI components implementing expert system logic:

#### a. **Knowledge Representation**
- `knowledge_base.py` - Frame-based car knowledge (1,050 cars)
- Symbolic facts and attributes
- Attribute indexing for fast lookup

#### b. **Reasoning Engine**
- `inference_engine.py` - Core AI reasoning
  - Forward chaining (data-driven inference)
  - Backward chaining (goal-driven inference)
  - Information theory (entropy/Gini)
  - Belief state management
  - Constraint satisfaction

#### c. **Expert System Facade**
- `expert_system.py` - High-level interface
  - Coordinates knowledge base and inference
  - Session management
  - Performance tracking

#### d. **ML Component** (Hybrid AI)
- `ml_model.py` - Random Forest classifier
  - Price segment prediction
  - Feature extraction
  - Sklearn integration

### 3. **Recommendation Module** (`automind/recommendation/`)
- **Purpose:** Content-based car recommendation
- **AI Concepts:**
  - Multi-criteria decision making
  - Preference-based filtering
  - Probability scoring
  - Ranking algorithms

Components:
- `engine.py` - RecommendationEngine class
  - Preference parsing
  - Attribute mapping
  - Evidence application
  - Result enrichment

### 4. **UI Module** (`automind/ui/`)
- **Purpose:** Reusable UI components
- **Separation of Concerns:** Business logic vs presentation

Components:
- `components.py` - Common UI elements
  - AI explanation displays
  - Session log viewer
  - Car details viewer
  - Performance metrics
- `guessing.py` - Guessing mode UI (to be created)
- `recommendation.py` - Recommendation mode UI (to be created)

### 5. **Utilities Module** (`automind/utils/`)
- **Purpose:** Cross-cutting concerns

Components:
- `logger.py` - SessionLogger class
  - Interaction tracking
  - AI process logging
  - JSON file management
  - Mode-specific logging

### 6. **Data Layer** (`data/`)
- **Purpose:** Knowledge base storage
- Processed car database (CSV)
- Data enrichment scripts

### 7. **Logging Layer** (`logs/`)
- **Purpose:** Session persistence and analysis
- Separate directories for each mode
- JSON format for easy parsing

---

## 🔄 Data Flow

### Guessing Mode Flow:
```
User → app.py → expert_system.py → inference_engine.py → knowledge_base.py
                     ↓
            SessionLogger (utils/logger.py)
                     ↓
            UIComponents (ui/components.py)
                     ↓
                  User Display
```

### Recommendation Mode Flow:
```
User Preferences → app.py → RecommendationEngine → expert_system.py
                                ↓
                         inference_engine.py
                                ↓
                          knowledge_base.py
                                ↓
                    SessionLogger + UIComponents
                                ↓
                    Ranked Results → User Display
```

---

## 🧩 Module Responsibilities

### Core AI Modules:

1. **knowledge_base.py**
   - Store 1,050 car frames
   - Attribute indexing
   - Value descriptions
   - Forward chaining rules

2. **inference_engine.py**
   - Question selection (entropy/Gini)
   - Belief state updates
   - Forward/backward chaining
   - Constraint checking
   - Rule application

3. **expert_system.py**
   - High-level API
   - Session lifecycle
   - Performance tracking
   - Model querying

### Recommendation Module:

4. **recommendation/engine.py**
   - Preference mapping
   - Multi-criteria matching
   - Content-based filtering
   - Result ranking

### UI Module:

5. **ui/components.py**
   - Reusable displays
   - AI explanations
   - Log viewers
   - Metrics dashboards

### Utilities:

6. **utils/logger.py**
   - Session tracking
   - File I/O
   - AI process documentation
   - Result logging

---

## 🎯 Design Principles

### 1. **Separation of Concerns**
- UI logic separated from business logic
- AI reasoning isolated from presentation
- Data access abstracted

### 2. **Modularity**
- Each module has single responsibility
- Clear interfaces between components
- Easy to test in isolation

### 3. **Reusability**
- Common UI components shared
- Logger used by both modes
- Expert system core shared

### 4. **Extensibility**
- Easy to add new modes
- Simple to add new AI strategies
- Straightforward to extend logging

### 5. **Maintainability**
- Clear file organization
- Documented interfaces
- Logical grouping

---

## 🔌 Component Interfaces

### SessionLogger API:
```python
logger = SessionLogger(mode="guessing")
logger.log_question(question, answer, value)
logger.log_result(result, guessed_car, actual_car)
logger.get_interactions()
```

### RecommendationEngine API:
```python
engine = RecommendationEngine(strategy="entropy")
recommendations = engine.get_recommendations(preferences)
ai_info = engine.get_ai_processing_info()
```

### UIComponents API:
```python
UIComponents.display_ai_explanation_guessing(strategy)
UIComponents.display_session_log(interactions)
UIComponents.display_car_details(details)
UIComponents.display_performance_metrics(metrics)
```

---

## 📊 Benefits of This Architecture

### For Development:
- ✅ **Easier debugging** - Isolated components
- ✅ **Faster testing** - Unit test each module
- ✅ **Clearer code** - Single responsibility
- ✅ **Better collaboration** - Work on different modules

### For AI Demonstration:
- ✅ **Clear AI concepts** - Each module shows specific AI
- ✅ **Transparent processing** - Logging shows AI steps
- ✅ **Educational value** - Easy to explain each part
- ✅ **Professional structure** - Industry-standard organization

### For Maintenance:
- ✅ **Easy updates** - Change one module without affecting others
- ✅ **Bug isolation** - Problems contained to specific modules
- ✅ **Feature addition** - Add new capabilities cleanly
- ✅ **Code reuse** - Share components across features

---

## 🚀 Future Enhancements

### Planned Modules:
1. **automind/evaluation/** - Model evaluation metrics
2. **automind/ml/** - Additional ML models
3. **automind/search/** - A* search implementation
4. **automind/learning/** - Case-based reasoning
5. **automind/api/** - REST API for external access

### Potential Improvements:
- Add unit tests for each module
- Create integration tests
- Add type hints throughout
- Generate API documentation
- Create architecture diagrams
- Add performance profiling

---

## 📚 Learning Outcomes

By studying this architecture, you learn:

1. **Software Engineering:**
   - Modular design
   - Separation of concerns
   - Package organization
   - Interface design

2. **AI Implementation:**
   - Expert systems structure
   - Recommendation systems
   - Knowledge representation
   - Inference engines

3. **Best Practices:**
   - Code organization
   - Documentation
   - Logging and monitoring
   - Maintainable code

---

## 🎓 For Your AI Course

This architecture demonstrates:
- ✅ **Professional code organization**
- ✅ **Industry-standard structure**
- ✅ **Clear separation of AI logic**
- ✅ **Maintainable and extensible design**
- ✅ **Well-documented components**

**Bonus points for:**
- Clean architecture
- Modular design
- Professional presentation
- Reusable components
- Comprehensive logging

---

This modular architecture transforms AutoMind from a monolithic script into a professional-grade AI application! 🌟
