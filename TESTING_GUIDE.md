# Testing Guide for AutoMind Improvements

## Quick Test Scenarios

### Test 1: Electric Vehicle Logic Consistency
**Goal:** Verify electric cars don't get asked about engine displacement

**Steps:**
1. Start a new game
2. When asked "Preferred fuel or powertrain?" → Select **Electric**
3. Continue answering questions
4. **Verify:** You should NEVER be asked about "engine in litres" or "engine performance"
5. Check the Session Log in sidebar to confirm no engine questions appear

**Expected Result:** ✅ No engine displacement questions for electric vehicles

---

### Test 2: Session Logging
**Goal:** Confirm all interactions are logged

**Steps:**
1. Play a complete game session
2. Look at the sidebar → Click **"Session Log"** expander
3. Verify you see all your questions and answers listed
4. Check the file system: `logs/session_YYYYMMDD_HHMMSS.json`
5. Open the JSON file and verify structure

**Expected Result:** ✅ All Q&A pairs logged in sidebar and file

---

### Test 3: Akinator-Style Guessing
**Goal:** Verify the system guesses sooner (not just recommending)

**Steps:**
1. Think of a specific car (e.g., "Tata Nexon EV")
2. Answer questions honestly
3. Notice when the system makes its first guess
4. **Compare:** Should guess with ~4-6 questions, not 8-10

**Expected Result:** ✅ Earlier guessing behavior (more confident sooner)

---

### Test 4: Constraint Rule Validation
**Goal:** Check if logical rules fire correctly

**Test Scenarios:**

| When you select... | System should infer/skip... |
|-------------------|----------------------------|
| Fuel Type: Electric | Skip engine CC questions |
| Luxury: Yes | Infer Premium price segment |
| Family Size: Large | Suggest SUV body type |
| Persona: Eco | Prefer electric fuel type |

**Steps:**
1. Select one of the triggers above
2. Watch subsequent questions
3. Check if constraints are respected

---

## How to Verify Logs

### In Browser (Sidebar):
```
Sidebar → Session Log (click to expand)
You'll see:
  Q1: Preferred fuel or powertrain?
  → Electric
  ---
  Q2: Which body style fits best?
  → SUV
  ---
```

### In File System:
```bash
# View latest log
ls -lt logs/
cat logs/session_*.json | tail -1
```

### JSON Structure:
```json
{
  "session_id": "20251014_153045",
  "interactions": [
    {
      "timestamp": "2025-10-14T15:30:50.123456",
      "question": "Preferred fuel or powertrain?",
      "answer": "Electric",
      "value": "electric"
    }
  ]
}
```

---

## Common Issues to Report

If you encounter any of these, let me know:

1. **Still asking engine questions for electric cars**
   - Check session log
   - Provide the log file

2. **Not guessing soon enough**
   - Still feels like recommendations
   - Too many questions before guess

3. **Logs not appearing**
   - Check sidebar expander
   - Check `logs/` directory exists
   - Verify file permissions

4. **Illogical combinations**
   - Any other impossible scenarios
   - E.g., "Budget luxury cars", "Electric diesel", etc.

---

## Current Thresholds

For reference, the system now uses:

```python
confidence_threshold = 0.65  # Was 0.78
gap_threshold = 0.15         # Was 0.18
backward_chain_activation = 0.35  # Was 0.78
```

This means:
- Guesses when top candidate has 65% probability (vs 78%)
- Needs 15% gap between top 2 (vs 18%)
- Starts asking specific questions at 35% probability (vs 78%)

---

## Reporting Issues

When reporting problems, please provide:

1. **Session log** (from sidebar or logs/ directory)
2. **Screenshot** of the illogical question
3. **Steps to reproduce**
4. **Car you were thinking of**

This will help identify and fix edge cases!
