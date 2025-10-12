# Expert System for Car Recommendation - AI Coursework Documentation

## Overview

This is a **classic AI Expert System** that demonstrates fundamental artificial intelligence concepts for academic coursework. Unlike the machine learning approach, this system uses **symbolic AI** and **knowledge-based reasoning** to recommend cars.

## Core AI Concepts Implemented

### 1. Knowledge Representation

**What it is:** Storing facts and rules about the domain (cars) in a structured format.

**Implementation:**
```python
class CarKnowledgeBase:
    - Stores 50 cars with attributes (brand, type, fuel, price, luxury)
    - Uses frames/semantic networks to represent car knowledge
    - Maintains attribute-value relationships
```

**AI Concept:** Knowledge representation using frames (attribute-value pairs for each car)

### 2. Inference Engine

**What it is:** A reasoning mechanism that derives new facts from known facts using logical rules.

**Implementation:**
```python
class InferenceEngine:
    - forward_chain(): Applies rules to derive new facts
    - apply_rule(): Evaluates if-then rules
    - Implements production system architecture
```

**AI Concepts:**
- **Forward Chaining:** Start with known facts, apply rules to derive conclusions
- **Rule-Based Reasoning:** IF-THEN rules like "IF price=under_10L AND luxury=No THEN budget_car"

**Example Rules:**
```
Rule 1: IF price_range = under_10L AND luxury = No THEN is_budget = True
Rule 2: IF luxury = Yes THEN is_luxury = True  
Rule 3: IF body_type IN [SUV, Sedan] THEN is_family = True
```

### 3. Information Gain & Optimal Question Selection

**What it is:** AI search strategy to select the most informative question at each step.

**Implementation:**
```python
def calculate_information_gain(attribute, possible_cars):
    - Calculates entropy before asking question
    - Calculates expected entropy after asking
    - Returns information gain = current_entropy - expected_entropy
    - Selects attribute with highest information gain
```

**AI Concepts:**
- **Entropy:** Measure of uncertainty in the dataset
- **Information Gain:** Reduction in entropy after asking a question
- **Greedy Search:** Always pick the question that maximizes information gain

**Mathematical Formula:**
```
Information Gain(A) = Entropy(S) - Σ(|Sv|/|S| × Entropy(Sv))

Where:
- S = current set of possible cars
- A = attribute being considered
- Sv = subset of cars with value v for attribute A
```

### 4. Belief State Management

**What it is:** Maintaining and updating probabilistic beliefs about which car is the answer.

**Implementation:**
```python
class BeliefState:
    - possible_cars: Set of cars still possible
    - confidence_scores: Probability distribution over cars
    - update_belief(): Bayesian-style belief propagation
```

**AI Concepts:**
- **Uncertainty Handling:** Dealing with incomplete information
- **Belief Propagation:** Updating confidence scores based on new evidence
- **Probabilistic Reasoning:** Assigning confidence scores to hypotheses

**Update Mechanism:**
```
For each answer:
1. Increase confidence of matching cars by 1.5x
2. Decrease confidence of non-matching cars by 0.1x
3. Normalize to maintain probability distribution
```

### 5. Expert System Architecture

**What it is:** Complete AI system integrating all components.

**Components:**
1. **Knowledge Base** - Domain facts and rules
2. **Inference Engine** - Reasoning mechanism  
3. **Working Memory** - Current state (belief state)
4. **User Interface** - Question/answer interaction

**System Flow:**
```
1. Initialize: Load knowledge base, set all cars as possible
2. Loop until determined:
   a. Calculate information gain for all attributes
   b. Select best question (highest gain)
   c. Ask user the question
   d. Update belief state based on answer
   e. Apply forward chaining to infer new facts
3. Return top candidates with confidence scores
```

## Comparison: Expert System vs Machine Learning

| Aspect | Expert System (This) | Machine Learning (Previous) |
|--------|---------------------|---------------------------|
| **Approach** | Symbolic AI, rules | Statistical learning |
| **Knowledge** | Explicit rules | Learned patterns |
| **Reasoning** | Logical inference | Pattern matching |
| **Transparency** | Fully explainable | Black box |
| **Data Needed** | Domain knowledge | Training data |
| **Updates** | Add/modify rules | Retrain model |
| **AI Paradigm** | Classical AI | Modern ML |

## Key Differences from ML Approach

### What Makes This "True AI"?

1. **Symbolic Reasoning:** Uses symbols and logic, not just numbers
2. **Explicit Knowledge:** Rules are human-readable and modifiable
3. **Logical Inference:** Derives conclusions through deduction
4. **Explainable:** Every decision can be traced through rules
5. **No Training:** Uses domain knowledge, not data patterns

### Why Expert Systems for AI Coursework?

Expert systems are **foundational AI** because they demonstrate:
- How machines can reason with knowledge
- How to represent human expertise in code
- How to make logical inferences
- How to handle uncertainty systematically

These are core AI concepts that predate (and complement) modern machine learning.

## Usage Examples

### Example 1: Interactive Session

```bash
$ python expert_system_cli.py

[AI] Question 1: What is the brand?
Options: Toyota, Honda, Ford, ...
[User] Toyota

[AI] Question 2: What is the body_type?
Options: SUV, Sedan, Hatchback
[User] SUV

[AI] Narrowed to 5 cars
[AI] Inferred: is_family = True

[AI] Question 3: What is the price_range?
...
```

### Example 2: Programmatic Use

```python
from expert_system import ExpertSystem

# Create expert system
es = ExpertSystem()

# Ask questions
attribute, values = es.ask_question()
# Returns: ('brand', ['Toyota', 'Honda', ...])

# Process answer
es.process_answer('brand', 'Toyota')

# Get recommendations
car, confidence = es.get_recommendation()
print(f"{car['brand']} {car['model']} - {confidence*100:.1f}% confidence")
```

## AI Techniques Summary

### 1. Knowledge-Based Systems ✓
- **Knowledge Base:** CarKnowledgeBase class
- **Facts:** Car attributes and values
- **Rules:** Inference rules for classification

### 2. Search Algorithms ✓
- **Search Strategy:** Information gain maximization
- **Greedy Search:** Always pick best question
- **Goal:** Find car with minimum questions

### 3. Reasoning & Inference ✓
- **Forward Chaining:** Derive facts from rules
- **Rule-Based System:** Production rules
- **Logical Inference:** IF-THEN reasoning

### 4. Uncertainty & Probability ✓
- **Belief States:** Probabilistic car rankings
- **Confidence Scores:** Bayesian-style updates
- **Uncertainty Handling:** Multiple candidates

### 5. Problem Solving ✓
- **Problem:** Identify car with minimum questions
- **State Space:** All possible car-attribute combinations
- **Heuristic:** Information gain for question selection

## Testing & Validation

```bash
# Run demo
python expert_system.py

# Interactive CLI
python expert_system_cli.py

# Test all components
python test_expert_system.py
```

## Academic Alignment

This implementation covers these AI topics:

1. **Knowledge Representation** (frames, semantic networks)
2. **Inference Engines** (forward chaining, production systems)
3. **Search Algorithms** (information gain, greedy search)
4. **Uncertainty** (belief states, confidence scores)
5. **Expert Systems** (complete AI architecture)

These are fundamental AI concepts taught in introductory AI courses and demonstrate understanding of classical AI beyond just machine learning.

## File Structure

```
expert_system.py          # Core expert system implementation
expert_system_cli.py      # Interactive command-line interface
test_expert_system.py     # Test suite
EXPERT_SYSTEM_GUIDE.md    # This documentation
```

## Further Enhancements (Optional)

1. **Backward Chaining:** Goal-directed reasoning
2. **Fuzzy Logic:** Handle "somewhat luxury" answers
3. **Certainty Factors:** Confidence in rules (like MYCIN)
4. **Explanation Facility:** Explain why questions are asked
5. **Learning Component:** Update rules based on feedback

## References

- Russell & Norvig, "Artificial Intelligence: A Modern Approach" (Knowledge Representation, Inference)
- Expert Systems: Principles and Programming (Giarratano & Riley)
- Information Theory and Entropy (Shannon)

---

**Status:** ✅ Production-ready expert system demonstrating classical AI techniques
**Purpose:** AI coursework demonstrating foundational AI concepts beyond machine learning
