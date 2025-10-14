#!/usr/bin/env python3
"""Add 'era' attribute to car database to help differentiate similar models from different generations.

Era Categories:
- current: 2020+ (Latest models currently sold)
- recent: 2015-2019 (Recent but not latest)
- older: 2010-2014 (Older generation)
- classic: Pre-2010 (Vintage/discontinued)
"""

import csv
import re
from pathlib import Path

def extract_year_from_model(model_name: str) -> int:
    """Extract year from model name if available.
    
    Examples:
    - "Swift VXi [2014-2017]" -> 2017 (take end year)
    - "Innova 2.5 GX BS IV 7 STR" -> None
    - "Ritz VXI BS-IV" -> None (but we know Ritz is discontinued 2016)
    """
    # Look for year range in brackets [YYYY-YYYY]
    match = re.search(r'\[(\d{4})-(\d{4})\]', model_name)
    if match:
        return int(match.group(2))  # Return end year
    
    # Look for single year [YYYY]
    match = re.search(r'\[(\d{4})\]', model_name)
    if match:
        return int(match.group(1))
    
    return None

def determine_era_by_model_knowledge(brand: str, model_name: str, year: int = None) -> str:
    """Determine era based on model knowledge and year hints.
    
    Uses a combination of:
    1. Extracted year from model name
    2. Known discontinuation dates
    3. BS (Bharat Stage) emission standards
    """
    model_lower = model_name.lower()
    brand_lower = brand.lower()
    
    # If we have year from model name, use it
    if year:
        if year >= 2020:
            return 'current'
        elif year >= 2015:
            return 'recent'
        elif year >= 2010:
            return 'older'
        else:
            return 'classic'
    
    # Known discontinued models (classic era)
    discontinued_models = [
        'ritz', 'zen', 'esteem', 'omni', 'gypsy', 'palio', 'indigo', 
        'logan', 'sumo', 'safari dicor', 'venture', 'ambassador',
        'figo aspire', 'punto', 'linea', 'aveo', 'optra', 'sail'
    ]
    
    for disc in discontinued_models:
        if disc in model_lower:
            return 'classic'
    
    # BS-II, BS-III = very old (classic)
    if 'bs-ii' in model_lower or 'bs-iii' in model_lower or 'bs ii' in model_lower:
        return 'classic'
    
    # BS-IV = older generation (2010-2019)
    if 'bs-iv' in model_lower or 'bs iv' in model_lower:
        return 'older'
    
    # BS-VI = recent to current (2020+)
    if 'bs-vi' in model_lower or 'bs vi' in model_lower or 'bs6' in model_lower:
        return 'current'
    
    # Current generation models (known popular current models)
    current_models = [
        'nexon', 'harrier', 'safari', 'punch', 'altroz',  # Tata
        'venue', 'creta', 'alcazar', 'tucson', 'ioniq',  # Hyundai
        'seltos', 'sonet', 'carens', 'carnival', 'ev6',  # Kia
        'hector', 'astor', 'zs ev', 'gloster',  # MG
        'compass', 'meridian',  # Jeep
        'xuv700', 'xuv300', 'scorpio-n', 'thar',  # Mahindra
        'grand vitara', 'jimny', 'fronx',  # Maruti new models
        'kushaq', 'slavia', 'kodiaq',  # Skoda
        'taigun', 'virtus',  # VW
        'hyryder',  # Toyota
    ]
    
    for current in current_models:
        if current in model_lower:
            return 'current'
    
    # If model has "2.0", "2.5", "3.0" and is luxury brand, likely recent
    if brand_lower in ['bmw', 'mercedes-benz', 'audi', 'jaguar', 'land rover', 'porsche', 'volvo']:
        # Luxury brands - default to recent unless proven otherwise
        return 'recent'
    
    # Default: assume recent for models without clear indicators
    return 'recent'

def add_era_column(input_csv: Path, output_csv: Path):
    """Add era column to CSV file."""
    rows_processed = 0
    era_counts = {'current': 0, 'recent': 0, 'older': 0, 'classic': 0}
    
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['era']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            brand = row['brand']
            model = row['model']
            
            # Extract year from model name
            year = extract_year_from_model(model)
            
            # Determine era
            era = determine_era_by_model_knowledge(brand, model, year)
            
            # Add era to row
            row['era'] = era
            writer.writerow(row)
            
            rows_processed += 1
            era_counts[era] += 1
            
            # Print some examples
            if rows_processed <= 10 or era == 'classic':
                print(f"{brand} {model[:40]:<40} -> {era:>8} (year: {year or 'N/A'})")
    
    print(f"\n✅ Processed {rows_processed} rows")
    print(f"\nEra Distribution:")
    for era, count in sorted(era_counts.items()):
        percentage = (count / rows_processed) * 100
        print(f"  {era:>8}: {count:4d} ({percentage:5.1f}%)")

if __name__ == '__main__':
    input_file = Path('data/car_data_enriched.csv')
    output_file = Path('data/car_data_enriched_with_era.csv')
    
    print("Adding 'era' attribute to car database...\n")
    add_era_column(input_file, output_file)
    print(f"\n✅ Saved to: {output_file}")
    print("\n💡 Review the output and then replace the original file:")
    print(f"   mv {output_file} {input_file}")
