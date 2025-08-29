#!/usr/bin/env python3
"""Parse Gemini AI responses and update car_data.csv with extracted specifications."""

import csv
import json
import os
import re
from datetime import datetime

def parse_gemini_response(response_text):
    """Extract car specifications from Gemini AI response."""
    if not response_text:
        return {}
    
    specs = {}
    patterns = {
        'Year': r'Year:\s*(.+?)(?:\n|$)',
        'BodyType': r'BodyType:\s*(.+?)(?:\n|$)',
        'Cost': r'Cost:\s*(.+?)(?:\n|$)',
        'Length': r'Length:\s*(.+?)(?:\n|$)',
        'CargoRear': r'CargoRear:\s*(.+?)(?:\n|$)',
        'CargoTotal': r'CargoTotal:\s*(.+?)(?:\n|$)',
        'MpgCity': r'MpgCity:\s*(.+?)(?:\n|$)',
        'MpgHwy': r'MpgHwy:\s*(.+?)(?:\n|$)',
        'MpgCombo': r'MpgCombo:\s*(.+?)(?:\n|$)',
        'FuelType': r'FuelType:\s*(.+?)(?:\n|$)',
        'Drive': r'Drive:\s*(.+?)(?:\n|$)',
        'Reliability': r'Reliability:\s*(.+?)(?:\n|$)'
    }
    
    for field, pattern in patterns.items():
        match = re.search(pattern, response_text, re.IGNORECASE | re.DOTALL)
        if match:
            value = match.group(1).strip()
            if "N/A" in value:
                specs[field] = "N/A"
                continue
            
            # Clean up values based on field type
            if field == 'Year':
                year_match = re.search(r'\b(19|20)\d{2}\b', value)
                specs[field] = year_match.group(0) if year_match else value
            elif field in ['Length', 'CargoRear', 'CargoTotal', 'MpgCity', 'MpgHwy', 'MpgCombo']:
                num_match = re.search(r'([0-9]+\.?[0-9]*)', value)
                specs[field] = num_match.group(1) if num_match else value
            elif field == 'Cost':
                price_matches = re.findall(r'\$([0-9,]+)', value)
                if price_matches:
                    # If multiple prices found, show the range
                    if len(price_matches) > 1:
                        specs[field] = f"${price_matches[0]} - ${price_matches[-1]}"
                    else:
                        specs[field] = f"${price_matches[0]}"
                else:
                    specs[field] = value
            elif field == 'BodyType':
                # Standardize body type
                value_lower = value.lower()
                if 'hatchback' in value_lower:
                    specs[field] = 'Hatchback'
                elif 'sedan' in value_lower:
                    specs[field] = 'Sedan'
                elif 'suv' in value_lower:
                    specs[field] = 'SUV'
                elif 'crossover' in value_lower:
                    specs[field] = 'Crossover'
                elif 'wagon' in value_lower:
                    specs[field] = 'Wagon'
                elif 'coupe' in value_lower:
                    specs[field] = 'Coupe'
                elif 'convertible' in value_lower:
                    specs[field] = 'Convertible'
                else:
                    # Extract the first word if it looks like a body type
                    first_word = value.split()[0] if value.split() else value
                    specs[field] = first_word.title()
                    
            elif field == 'FuelType':
                # Standardize fuel type
                fuel_lower = value.lower()
                if 'gasoline' in fuel_lower or 'gas' in fuel_lower:
                    specs[field] = 'Gasoline'
                elif 'hybrid' in fuel_lower:
                    specs[field] = 'Hybrid'
                elif 'electric' in fuel_lower:
                    specs[field] = 'Electric'
                elif 'diesel' in fuel_lower:
                    specs[field] = 'Diesel'
                else:
                    # Extract first word that looks like a fuel type
                    first_word = value.split()[0] if value.split() else value
                    specs[field] = first_word.title()
                    
            elif field == 'Drive':
                # Standardize drive type
                drive_lower = value.lower()
                if 'fwd' in drive_lower or 'front' in drive_lower:
                    specs[field] = 'FWD'
                elif 'rwd' in drive_lower or 'rear' in drive_lower:
                    specs[field] = 'RWD'
                elif 'awd' in drive_lower or 'all' in drive_lower:
                    specs[field] = 'AWD'
                elif '4wd' in drive_lower or 'four' in drive_lower:
                    specs[field] = '4WD'
                else:
                    # Look for drive type pattern
                    drive_match = re.search(r'\b(FWD|RWD|AWD|4WD)\b', value, re.IGNORECASE)
                    if drive_match:
                        specs[field] = drive_match.group(1).upper()
                    else:
                        specs[field] = value
                        
            elif field == 'Reliability':
                rating_match = re.search(r'([0-9]+\.?[0-9]*)\s*(?:out of|/)\s*[0-9]+', value)
                specs[field] = f"{rating_match.group(1)}/5" if rating_match else value
            else:
                specs[field] = value
    
    return specs

def load_json_data(json_file):
    """Load car search results from JSON file."""
    if not os.path.exists(json_file):
        print(f"JSON file not found: {json_file}")
        return []
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_csv_data(csv_file):
    """Load existing car data from CSV file."""
    if not os.path.exists(csv_file):
        return []
    with open(csv_file, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def update_csv_with_extracted_data(csv_file, json_file, script_dir):
    """Update CSV file with data extracted from JSON responses."""
    json_data = load_json_data(json_file)
    csv_data = load_csv_data(csv_file)
    
    if not json_data:
        print("No JSON data to process")
        return
    
    if not csv_data:
        print("No CSV data found")
        return
    
    print(f"Processing {len(json_data)} cars from JSON...")
    
    # Create mapping of make/model to extracted specs
    extracted_specs = {}
    for item in json_data:
        make = item.get('make', '')
        model = item.get('model', '')
        response = item.get('gemini_response', '')
        
        key = f"{make}|{model}"
        specs = parse_gemini_response(response)
        extracted_specs[key] = specs
        
        print(f"Extracted {len(specs)} specs for {make} {model}")
    
    # Update CSV data with extracted specs
    updated_count = 0
    for car in csv_data:
        make = car.get('Make', '')
        model = car.get('Model', '')
        key = f"{make}|{model}"
        
        if key in extracted_specs:
            specs = extracted_specs[key]
            updated_fields = []
            
            # Update each field if we have new data
            for field, value in specs.items():
                car[field] = value
                updated_fields.append(field)
            
            if updated_fields:
                updated_count += 1
    
    # Create backup in history folder
    history_dir = os.path.join(script_dir, "history")
    os.makedirs(history_dir, exist_ok=True)
    backup_file = os.path.join(history_dir, f"car_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    if os.path.exists(csv_file):
        import shutil
        shutil.copy2(csv_file, backup_file)
        print(f"Backup created: {backup_file}")
    
    # Write updated data back to CSV
    headers = ["Make", "Model", "Year", "BodyType", "Cost", "Length", "CargoRear", 
               "CargoTotal", "MpgCity", "MpgHwy", "MpgCombo", "FuelType", "Drive", "Reliability"]
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"\n✓ Updated {updated_count} cars in {csv_file}")

def main():
    """Main function to extract data from JSON and update CSV"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, "car_search.json")
    csv_file = os.path.join(script_dir, "car_data.csv")
    
    update_csv_with_extracted_data(csv_file, json_file, script_dir)

if __name__ == "__main__":
    main()