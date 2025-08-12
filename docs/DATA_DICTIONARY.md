# Data Dictionary for car_data.csv

This document describes the structure and content of the `car_data.csv` file containing information about 50 popular Indian market cars.

## File Overview
- **File Name**: car_data.csv
- **Format**: Comma-separated values (CSV)
- **Encoding**: UTF-8
- **Total Records**: 50 cars
- **Header Row**: Yes (first row contains column names)

## Column Definitions

### 1. model
- **Type**: String
- **Description**: The specific model name of the car
- **Required**: Yes
- **Example Values**: "Swift", "Creta", "Nexon EV", "Fortuner"
- **Notes**: Represents the official model name as marketed by the manufacturer

### 2. brand
- **Type**: String
- **Description**: The manufacturer or brand name of the car
- **Required**: Yes
- **Allowed Values**: 
  - Maruti Suzuki
  - Hyundai
  - Tata
  - Mahindra
  - Honda
  - Toyota
  - Ford
  - Kia
  - Skoda
  - Volkswagen
  - MG
  - Jeep
  - Renault
  - Datsun
- **Notes**: Official brand names as registered in the Indian market

### 3. body_type
- **Type**: String (Categorical)
- **Description**: The body style or type of the vehicle
- **Required**: Yes
- **Allowed Values**:
  - `Hatchback`: Compact cars with rear door that opens upwards
  - `Sedan`: Four-door cars with separate trunk compartment
  - `SUV`: Sport Utility Vehicles, including crossovers and compact SUVs
- **Notes**: Classification based on Indian market categorization

### 4. fuel_type
- **Type**: String (Categorical)
- **Description**: The primary fuel type used by the vehicle
- **Required**: Yes
- **Allowed Values**:
  - `Petrol`: Gasoline-powered vehicles
  - `Diesel`: Diesel-powered vehicles
  - `Electric`: Battery electric vehicles (BEV)
- **Notes**: Represents the primary or most common fuel variant for each model

### 5. price_range
- **Type**: String (Categorical)
- **Description**: Price bracket of the vehicle in Indian Rupees (₹)
- **Required**: Yes
- **Allowed Values**:
  - `under_10L`: Below ₹10 lakhs
  - `10-20L`: ₹10 lakhs to ₹20 lakhs
  - `20-30L`: ₹20 lakhs to ₹30 lakhs
  - `above_30L`: Above ₹30 lakhs
- **Notes**: 
  - "L" stands for "Lakh" (100,000)
  - Prices are approximate ex-showroom prices for base variants
  - Prices may vary by location and time

### 6. luxury
- **Type**: String (Boolean)
- **Description**: Indicates whether the car is positioned as a luxury vehicle
- **Required**: Yes
- **Allowed Values**:
  - `Yes`: Positioned as luxury/premium vehicle
  - `No`: Positioned as mass market/mainstream vehicle
- **Notes**: Based on brand positioning and market segment in India

### 7. engine_cc
- **Type**: Integer
- **Description**: Engine displacement in cubic centimeters (cc)
- **Required**: Yes
- **Range**: 0 - 2755
- **Special Values**:
  - `0`: Electric vehicles (no internal combustion engine)
- **Notes**: 
  - Represents the most common engine variant for each model
  - For electric vehicles, engine_cc is set to 0

## Data Quality Notes

1. **Uniqueness**: Each car model appears only once in the dataset
2. **Accuracy**: All data represents real vehicles available in the Indian market as of 2023-2024
3. **Completeness**: No missing values in any column
4. **Consistency**: Naming conventions and categorizations are standardized across all records
5. **Currency**: Prices and specifications reflect recent market conditions

## Usage Guidelines

- This dataset is suitable for automotive market analysis in India
- Price ranges are indicative and may vary with trim levels and optional features
- Engine displacements represent the most popular variant for each model
- Electric vehicle specifications focus on the drivetrain type rather than engine displacement

## Data Sources

The information in this dataset has been compiled from:
- Official manufacturer websites and brochures
- Indian automotive market reports
- Ex-showroom price listings from major Indian cities
- Technical specifications from certified sources

---
*Last Updated: December 2024*