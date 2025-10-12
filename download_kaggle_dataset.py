#!/usr/bin/env python3
"""
Download and integrate Kaggle CarDekho dataset into AutoMind.

This script:
1. Downloads the CardDekho dataset from Kaggle
2. Processes and cleans the data
3. Converts it to AutoMind's format
4. Merges with existing car data
5. Updates the knowledge base for the expert system
"""

import os
import sys
import csv

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️  pandas not installed. Install with: pip install pandas")

def download_dataset():
    """Download the CardDekho dataset from Kaggle."""
    try:
        import kagglehub
        
        print("📥 Downloading CardDekho dataset from Kaggle...")
        path = kagglehub.dataset_download("nehalbirla/vehicle-dataset-from-cardekho")
        print(f"✅ Dataset downloaded to: {path}")
        return path
    except ImportError:
        print("❌ kagglehub not installed. Installing...")
        os.system("pip install kagglehub")
        import kagglehub
        path = kagglehub.dataset_download("nehalbirla/vehicle-dataset-from-cardekho")
        print(f"✅ Dataset downloaded to: {path}")
        return path
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return None


def find_csv_file(path):
    """Find the CSV file in the downloaded directory."""
    if not path or not os.path.exists(path):
        return None
    
    # Look for CSV files
    for file in os.listdir(path):
        if file.endswith('.csv'):
            return os.path.join(path, file)
    
    return None


def categorize_price(price_lakhs):
    """Categorize price into AutoMind ranges."""
    if price_lakhs < 10:
        return "under_10L"
    elif price_lakhs < 20:
        return "10-20L"
    elif price_lakhs < 30:
        return "20-30L"
    else:
        return "above_30L"


def categorize_luxury(price_lakhs, brand):
    """Determine if car is luxury based on price and brand."""
    luxury_brands = ['BMW', 'Mercedes-Benz', 'Audi', 'Volvo', 'Jaguar', 
                     'Land Rover', 'Porsche', 'Lexus', 'Tesla']
    
    if brand in luxury_brands:
        return "Yes"
    elif price_lakhs >= 30:
        return "Yes"
    else:
        return "No"


def normalize_body_type(body_type):
    """Normalize body type to AutoMind categories."""
    body_type_lower = str(body_type).lower()
    
    if any(x in body_type_lower for x in ['suv', 'muv', 'crossover']):
        return "SUV"
    elif any(x in body_type_lower for x in ['sedan', 'saloon']):
        return "Sedan"
    elif any(x in body_type_lower for x in ['hatchback', 'hatch']):
        return "Hatchback"
    else:
        return "SUV"  # Default fallback


def normalize_fuel_type(fuel_type):
    """Normalize fuel type to AutoMind categories."""
    fuel_type_lower = str(fuel_type).lower()
    
    if any(x in fuel_type_lower for x in ['petrol', 'gasoline']):
        return "Petrol"
    elif any(x in fuel_type_lower for x in ['diesel']):
        return "Diesel"
    elif any(x in fuel_type_lower for x in ['electric', 'ev', 'battery']):
        return "Electric"
    elif any(x in fuel_type_lower for x in ['hybrid']):
        return "Electric"  # Treat hybrid as electric for now
    else:
        return "Petrol"  # Default fallback


def process_kaggle_data(csv_path):
    """Process the Kaggle dataset and convert to AutoMind format."""
    print(f"\n📊 Processing dataset from: {csv_path}")
    
    if not HAS_PANDAS:
        print("❌ pandas is required for dataset processing")
        print("   Install with: pip install pandas")
        return []
    
    try:
        # Read the dataset
        df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        
        # Display sample
        print("\n📋 Sample data:")
        print(df.head())
        
        # Process and convert to AutoMind format
        processed_cars = []
        
        for idx, row in df.iterrows():
            try:
                # Extract relevant fields (adjust based on actual column names)
                car = {}
                
                # Handle different possible column name variations
                if 'name' in df.columns:
                    full_name = str(row['name'])
                elif 'car_name' in df.columns:
                    full_name = str(row['car_name'])
                else:
                    full_name = str(row[df.columns[0]])  # Use first column
                
                # Split name into brand and model
                parts = full_name.split()
                if len(parts) >= 2:
                    car['brand'] = parts[0]
                    car['model'] = ' '.join(parts[1:])
                else:
                    car['brand'] = parts[0]
                    car['model'] = parts[0]
                
                # Get price (try different column names)
                price_lakhs = 0
                if 'selling_price' in df.columns:
                    price_lakhs = float(row['selling_price'])
                elif 'price' in df.columns:
                    price_lakhs = float(row['price'])
                elif 'ex_showroom_price' in df.columns:
                    price_lakhs = float(row['ex_showroom_price'])
                
                car['price_range'] = categorize_price(price_lakhs)
                
                # Body type
                if 'body_type' in df.columns:
                    car['body_type'] = normalize_body_type(row['body_type'])
                else:
                    car['body_type'] = "SUV"  # Default
                
                # Fuel type
                if 'fuel' in df.columns:
                    car['fuel_type'] = normalize_fuel_type(row['fuel'])
                elif 'fuel_type' in df.columns:
                    car['fuel_type'] = normalize_fuel_type(row['fuel_type'])
                else:
                    car['fuel_type'] = "Petrol"  # Default
                
                # Luxury status
                car['luxury'] = categorize_luxury(price_lakhs, car['brand'])
                
                # Engine CC (if available)
                if 'engine' in df.columns:
                    engine_str = str(row['engine'])
                    # Extract numeric value from engine string
                    import re
                    match = re.search(r'(\d+)', engine_str)
                    car['engine_cc'] = int(match.group(1)) if match else 1200
                else:
                    car['engine_cc'] = 1200  # Default
                
                processed_cars.append(car)
                
            except Exception as e:
                print(f"⚠️  Skipping row {idx}: {e}")
                continue
        
        print(f"\n✅ Processed {len(processed_cars)} cars")
        return processed_cars
        
    except Exception as e:
        print(f"❌ Error processing dataset: {e}")
        return []


def save_to_automind_format(cars, output_path="data/car_data_kaggle.csv"):
    """Save processed cars to AutoMind CSV format."""
    print(f"\n💾 Saving to {output_path}...")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='') as f:
        fieldnames = ['model', 'brand', 'body_type', 'fuel_type', 'price_range', 'luxury', 'engine_cc']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for car in cars:
            writer.writerow(car)
    
    print(f"✅ Saved {len(cars)} cars to {output_path}")


def merge_with_existing(kaggle_path="data/car_data_kaggle.csv", 
                        existing_path="data/car_data.csv",
                        output_path="data/car_data_expanded.csv"):
    """Merge Kaggle dataset with existing car data."""
    print(f"\n🔗 Merging datasets...")
    
    existing_cars = []
    kaggle_cars = []
    
    # Read existing data
    if os.path.exists(existing_path):
        with open(existing_path, 'r') as f:
            reader = csv.DictReader(f)
            existing_cars = list(reader)
        print(f"✅ Loaded {len(existing_cars)} existing cars")
    
    # Read Kaggle data
    if os.path.exists(kaggle_path):
        with open(kaggle_path, 'r') as f:
            reader = csv.DictReader(f)
            kaggle_cars = list(reader)
        print(f"✅ Loaded {len(kaggle_cars)} Kaggle cars")
    
    # Merge (remove duplicates based on brand+model)
    seen = set()
    merged_cars = []
    
    for car in existing_cars:
        key = f"{car['brand']}_{car['model']}"
        if key not in seen:
            merged_cars.append(car)
            seen.add(key)
    
    for car in kaggle_cars:
        key = f"{car['brand']}_{car['model']}"
        if key not in seen:
            merged_cars.append(car)
            seen.add(key)
    
    # Save merged data
    with open(output_path, 'w', newline='') as f:
        fieldnames = ['model', 'brand', 'body_type', 'fuel_type', 'price_range', 'luxury', 'engine_cc']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for car in merged_cars:
            writer.writerow(car)
    
    print(f"✅ Merged dataset saved to {output_path}")
    print(f"📊 Total unique cars: {len(merged_cars)}")
    
    return output_path


def main():
    """Main execution flow."""
    print("="*60)
    print("KAGGLE DATASET INTEGRATION FOR AUTOMIND")
    print("="*60)
    
    # Step 1: Download dataset
    dataset_path = download_dataset()
    if not dataset_path:
        print("❌ Failed to download dataset")
        return
    
    # Step 2: Find CSV file
    csv_file = find_csv_file(dataset_path)
    if not csv_file:
        print(f"❌ No CSV file found in {dataset_path}")
        print("Please check the downloaded directory and update the script.")
        return
    
    # Step 3: Process data
    processed_cars = process_kaggle_data(csv_file)
    if not processed_cars:
        print("❌ No cars processed")
        return
    
    # Step 4: Save to AutoMind format
    save_to_automind_format(processed_cars)
    
    # Step 5: Merge with existing data
    merged_path = merge_with_existing()
    
    print("\n" + "="*60)
    print("✅ DATASET INTEGRATION COMPLETE!")
    print("="*60)
    print(f"\nOutput files:")
    print(f"  • Kaggle only: data/car_data_kaggle.csv")
    print(f"  • Merged data: {merged_path}")
    print(f"\nNext steps:")
    print(f"  1. Review the merged dataset")
    print(f"  2. Update expert_system.py to use expanded dataset")
    print(f"  3. Regenerate training data for ML model")
    print(f"  4. Test the system with new data")


if __name__ == "__main__":
    main()
