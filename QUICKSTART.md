# AutoMind - Quick Start Guide

## 🚀 Fastest Way to Demo

### Option 1: CLI (No Installation)
```bash
python automind_cli.py
```
**Then try:** "A Toyota SUV under 20 lakhs"

### Option 2: Web UI (Visual Demo)
```bash
pip install streamlit
streamlit run automind_ui.py
```
**Then visit:** http://localhost:8501

---

## 🎯 Demo Queries (Copy & Paste)

```
A Toyota SUV under 20 lakhs
Luxury BMW sedan above 50 lakhs
Cheap Maruti hatchback under 10L
Electric crossover vehicle
A luxury electric sedan by Tesla above 50 lakhs
```

---

## 📋 What You'll See

### Input
"A Toyota SUV under 20 lakhs"

### Extracted Features
- Brand: Toyota
- Type: SUV
- Price: under_20L

### Best Match
**Toyota Innova Crysta** (Score: 50/100)
- Type: SUV
- Fuel: Diesel
- Price: 10-20L

---

## 🎥 For Teacher Demo

**Show this sequence:**

1. **Start CLI:** `python automind_cli.py`
2. **Enter query:** "Cheap Maruti hatchback under 10L"
3. **See results:** Maruti Swift (80/100 match)
4. **Show another:** "Luxury BMW sedan above 50L"

**Total time:** 2 minutes

---

## ✅ System Features

- ✅ Natural language understanding
- ✅ Fuzzy matching (typo correction)
- ✅ Synonym support (EV→electric)
- ✅ Smart scoring (0-100)
- ✅ Multiple UI options

---

## 📚 Documentation

- `DEMO_INSTRUCTIONS.md` - Full demo guide
- `SYSTEM_TEST_REPORT.md` - Test results
- `docs/NLP_MODULE_DOCUMENTATION.md` - Technical docs

---

**Ready in 30 seconds!** Just run `python automind_cli.py`
