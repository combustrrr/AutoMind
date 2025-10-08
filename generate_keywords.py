import csv
import json

# Load YOUR completed dataset (Sarthak's Week 1-2 work)
with open("data/car_data.csv", "r") as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Extract unique values for each category
brands = set()
body_types = set()
fuel_types = set()

for row in data:
    brands.add(row["brand"].lower())
    body_types.add(row["body_type"].lower())
    fuel_types.add(row["fuel_type"].lower())

# Generate domain-specific patterns for Experiment 5 with enhanced synonym mappings
keywords = {
    "brands": sorted(list(brands)),
    "body_types": sorted(list(body_types)),
    "fuel_types": sorted(list(fuel_types)),
    "price_bins": ["under_10l", "10-20l", "20-30l", "above_30l"],  # From YOUR schema
    "synonyms": {
        "body_types": {
            "suv": ["suv", "suvs", "crossover", "crossovers", "4x4", "off-road", "sport utility"],
            "sedan": ["sedan", "sedans", "saloon", "saloons"],
            "hatchback": ["hatchback", "hatchbacks", "hatch"]
        },
        "fuel_types": {
            "electric": ["electric", "ev", "battery", "e-car", "zero-emission"],
            "diesel": ["diesel"],
            "petrol": ["petrol", "gasoline", "gas"]
        },
        "luxury": {
            "yes": ["luxury", "premium", "high-end", "expensive", "flagship", "elite", "prestige"],
            "no": ["cheap", "affordable", "budget", "economical", "value", "entry-level", "basic", "low-cost"]
        }
    }
}

# Save as JSON for Experiment 5 (required deliverable)
with open("src/keywords.json", "w") as f:
    json.dump(keywords, f, indent=2)

print("✅ Experiment 5 pattern database created! (keywords.json)")
print(f"Generated keywords for:")
print(f"  - {len(keywords['brands'])} brands")
print(f"  - {len(keywords['body_types'])} body types") 
print(f"  - {len(keywords['fuel_types'])} fuel types")
print(f"  - {len(keywords['price_bins'])} price bins")
print(f"  - Enhanced with synonym mappings for improved NLP matching")