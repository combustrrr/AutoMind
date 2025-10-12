# Kaggle Dataset Integration Guide

## Overview

This guide explains how to integrate the **CardDekho Vehicle Dataset** from Kaggle to expand AutoMind's car database from 50 to potentially hundreds or thousands of cars.

## Dataset Information

**Source**: [CardDekho Vehicle Dataset on Kaggle](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho)

**Contents**: 
- Real-world Indian car market data
- Attributes: Brand, Model, Year, Price, Fuel Type, Transmission, etc.
- Hundreds of car listings with detailed specifications

## Quick Start

### 1. Prerequisites

Install required packages:

```bash
pip install kagglehub pandas
```

### 2. Download and Process Dataset

Run the integration script:

```bash
python download_kaggle_dataset.py
```

This will:
1. ✅ Download the CardDekho dataset from Kaggle
2. ✅ Process and clean the data
3. ✅ Convert to AutoMind's format (CSV with our schema)
4. ✅ Merge with existing 50-car dataset
5. ✅ Generate expanded dataset: `data/car_data_expanded.csv`

### 3. Update Expert System

The expert system will automatically detect the expanded dataset. To use it:

```python
from expert_system import ExpertSystem

# Will load car_data_expanded.csv if available
es = ExpertSystem()
print(f"Loaded {len(es.kb.cars)} cars")
```

### 4. Retrain ML Model

If using ML-based predictions, regenerate training data:

```bash
# Generate training data from expanded dataset
python generate_training_data.py --dataset data/car_data_expanded.csv

# Train model on new data
python train_ml_model.py
```

## Output Files

After running the integration script:

```
data/
├── car_data.csv              # Original 50 cars
├── car_data_kaggle.csv       # Processed Kaggle data only
└── car_data_expanded.csv     # Merged dataset (50 + Kaggle)
```

## Data Schema Mapping

The script automatically converts Kaggle dataset to AutoMind's format:

| Kaggle Field | AutoMind Field | Conversion Logic |
|--------------|----------------|------------------|
| `name` | `brand`, `model` | Split first word as brand |
| `selling_price` | `price_range` | Categorize: <10L, 10-20L, 20-30L, >30L |
| `fuel` | `fuel_type` | Normalize: Petrol/Diesel/Electric |
| `body_type` | `body_type` | Normalize: SUV/Sedan/Hatchback |
| `engine` | `engine_cc` | Extract numeric CC value |
| - | `luxury` | Infer from price + brand |

## Data Quality

### Automatic Processing

The script handles:
- ✅ Missing values (uses sensible defaults)
- ✅ Inconsistent naming (normalizes brands/models)
- ✅ Price variations (converts to lakhs)
- ✅ Duplicate detection (brand+model combination)

### Manual Review

After processing, review the dataset:

```bash
# Check merged data
head -20 data/car_data_expanded.csv

# Count total cars
wc -l data/car_data_expanded.csv
```

## Integration with Components

### Expert System

The expert system automatically uses the expanded dataset:

```python
from expert_system import ExpertSystem

es = ExpertSystem(csv_file="data/car_data_expanded.csv")
# Now works with 100s of cars instead of 50
```

### ML Model

Retrain with more data for better accuracy:

```bash
# Generate 10,000+ training samples from expanded dataset
python generate_training_data.py --samples-per-car 50

# Train improved model
python train_ml_model.py
# Expected improvement: 30% → 50%+ accuracy
```

### NLP Engine

Works automatically with expanded brands/models:

```python
from nlp_engine import extract_features

# Will now recognize 100+ brands instead of 13
features = extract_features("I want a Nissan SUV")
```

## Benefits of Larger Dataset

### For Expert System
- ✅ More car options to choose from
- ✅ Better coverage of Indian car market
- ✅ More diverse price ranges and types
- ✅ Real-world specifications (not synthetic)

### For ML Model
- ✅ Better training data (real queries possible)
- ✅ Higher accuracy (more examples)
- ✅ Better generalization (diverse patterns)
- ✅ Reduced overfitting

### For User Experience
- ✅ More relevant recommendations
- ✅ Better matches for specific needs
- ✅ Current market options
- ✅ Realistic pricing information

## Troubleshooting

### Issue: Kaggle API Authentication

If download fails with authentication error:

1. Get Kaggle API credentials:
   - Go to https://www.kaggle.com/account
   - Create API token
   - Download `kaggle.json`

2. Place credentials:
   ```bash
   mkdir -p ~/.kaggle
   cp kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

### Issue: Column Name Mismatch

If dataset structure changed:

1. Check actual columns:
   ```python
   import pandas as pd
   df = pd.read_csv("path/to/dataset.csv")
   print(df.columns)
   ```

2. Update `download_kaggle_dataset.py`:
   - Modify column name mappings in `process_kaggle_data()`
   - Adjust normalization functions

### Issue: Memory Error

If dataset is too large:

1. Process in chunks:
   ```python
   # Edit download_kaggle_dataset.py
   df = pd.read_csv(csv_path, chunksize=1000)
   ```

2. Filter data:
   ```python
   # Keep only Indian market cars
   df = df[df['location'].str.contains('India')]
   ```

## Advanced Usage

### Custom Filtering

Filter specific car types before merging:

```python
# Edit download_kaggle_dataset.py, add before saving:

# Keep only cars under 30 lakhs
processed_cars = [c for c in processed_cars 
                  if c['price_range'] != 'above_30L']

# Keep only specific brands
target_brands = ['Toyota', 'Honda', 'Hyundai', 'Maruti Suzuki']
processed_cars = [c for c in processed_cars 
                  if c['brand'] in target_brands]
```

### Data Enrichment

Add custom attributes:

```python
# Add seating capacity
car['seating'] = 5  # Default

# Add year/age
if 'year' in df.columns:
    car['year'] = int(row['year'])
    car['age'] = 2024 - car['year']
```

### Dataset Statistics

Analyze the expanded dataset:

```python
import pandas as pd

df = pd.read_csv('data/car_data_expanded.csv')

print(f"Total cars: {len(df)}")
print(f"\nBrands: {df['brand'].nunique()}")
print(f"\nPrice distribution:")
print(df['price_range'].value_counts())
print(f"\nBody types:")
print(df['body_type'].value_counts())
print(f"\nFuel types:")
print(df['fuel_type'].value_counts())
```

## Next Steps

After successful integration:

1. ✅ Test expert system with new dataset
2. ✅ Regenerate ML training data
3. ✅ Retrain ML model for better accuracy
4. ✅ Update documentation with new car count
5. ✅ Test UI with expanded options

## References

- **Dataset Source**: https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho
- **KaggleHub Docs**: https://github.com/Kaggle/kagglehub
- **AutoMind Expert System**: `EXPERT_SYSTEM_GUIDE.md`
- **ML Integration**: `docs/ML_INTEGRATION.md`

---

**Status**: Ready to expand from 50 to 100s+ cars  
**Impact**: Better accuracy, more options, real-world data ✨
