import pandas as pd
import re
import os

def get_price_range(price):
    if pd.isna(price) or price < 1000000:
        return "under_10l"
    elif 1000000 <= price < 2000000:
        return "10-20l"
    elif 2000000 <= price < 3000000:
        return "20-30l"
    else:
        return "above_30l"

def get_engine_cc(engine_str):
    if isinstance(engine_str, str):
        match = re.search(r'(\d+)\s*cc', engine_str, re.I)
        if match:
            return int(match.group(1))
    return 1200  # Default to a common engine size

def infer_body_type(model_name, seating_capacity):
    model_lower = str(model_name).lower()
    
    # Check for explicit mentions
    if any(keyword in model_lower for keyword in ["suv", "sport utility", "creta", "venue", "seltos", "compass", "harrier", "xuv", "thar", "brezza", "nexon"]):
        return "suv"
    if any(keyword in model_lower for keyword in ["sedan", "dzire", "city", "verna", "ciaz", "amaze", "aspire"]):
        return "sedan"
    if any(keyword in model_lower for keyword in ["hatchback", "swift", "i10", "i20", "alto", "wagon", "baleno", "polo", "jazz", "glanza"]):
        return "hatchback"
    if any(keyword in model_lower for keyword in ["muv", "mpv", "innova", "ertiga", "marazzo", "xl6", "carens"]):
        return "muv"
    
    # Use seating capacity as a hint
    if pd.notna(seating_capacity):
        capacity = int(seating_capacity)
        if capacity >= 7:
            return "muv"
        elif capacity == 5:
            # Default small 5-seaters to hatchback, larger ones to sedan
            if any(keyword in model_lower for keyword in ["compact", "small", "mini"]):
                return "hatchback"
            return "sedan"
    
    # Default to hatchback for unknown cases (most common body type)
    return "hatchback"

def infer_luxury(make, price):
    luxury_brands = ["mercedes-benz", "mercedes", "bmw", "audi", "jaguar", "land rover", "volvo", "lexus", "porsche", "bentley", "rolls-royce"]
    make_lower = str(make).lower()
    if any(brand in make_lower for brand in luxury_brands):
        return True
    if pd.notna(price) and price > 3000000:
        return True
    return False

def clean_fuel_type(fuel_type):
    fuel_str = str(fuel_type).lower()
    if "diesel" in fuel_str:
        return "diesel"
    elif "petrol" in fuel_str or "gasoline" in fuel_str:
        return "petrol"
    elif "cng" in fuel_str:
        return "cng"
    elif "electric" in fuel_str or "ev" in fuel_str:
        return "electric"
    elif "hybrid" in fuel_str:
        return "hybrid"
    else:
        return "petrol"  # Default

def process_data(input_path, output_path):
    df = pd.read_csv(input_path)
    
    print(f"Original dataset size: {len(df)} rows")
    
    # Remove duplicates based on Make and Model
    df = df.drop_duplicates(subset=['Make', 'Model'], keep='first')
    print(f"After removing duplicates: {len(df)} rows")

    new_df = pd.DataFrame()
    new_df['brand'] = df['Make'].fillna('Unknown')
    new_df['model'] = df['Model'].fillna('Unknown Model')
    new_df['body_type'] = df.apply(lambda row: infer_body_type(row['Model'], row.get('Seating Capacity')), axis=1)
    new_df['fuel_type'] = df['Fuel Type'].apply(clean_fuel_type)
    new_df['price_range'] = df['Price'].apply(get_price_range)
    new_df['luxury'] = df.apply(lambda row: infer_luxury(row['Make'], row.get('Price')), axis=1)
    new_df['engine_cc'] = df['Engine'].apply(get_engine_cc)
    new_df['keywords'] = new_df['brand'] + ',' + new_df['body_type'] + ',' + new_df['fuel_type']

    # Remove only truly invalid rows
    new_df = new_df[new_df['brand'] != 'Unknown']
    new_df = new_df[new_df['model'] != 'Unknown Model']
    
    new_df.to_csv(output_path, index=False)
    print(f"\n✅ Processed data saved to {output_path}")
    print(f"Final dataset size: {len(new_df)} cars")
    print("\n📊 Body type distribution:")
    print(new_df['body_type'].value_counts())
    print("\n⛽ Fuel type distribution:")
    print(new_df['fuel_type'].value_counts())
    print("\n💰 Price range distribution:")
    print(new_df['price_range'].value_counts())


if __name__ == "__main__":
    # Find the new dataset file
    dataset_dir = '/home/codespace/.cache/kagglehub/datasets/nehalbirla/vehicle-dataset-from-cardekho/versions/4'
    csv_file = None
    for file in os.listdir(dataset_dir):
        if file.endswith('.csv'):
            csv_file = os.path.join(dataset_dir, file)
            break
    
    if csv_file:
        process_data(csv_file, "data/car_data_enriched.csv")
    else:
        print("Could not find the new dataset's CSV file.")
