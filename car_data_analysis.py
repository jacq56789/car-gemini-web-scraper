#!/usr/bin/env python3
"""Analyze car data for cargo efficiency and fuel economy."""

import csv
import os

def load_car_data(csv_file):
    """Load car data from CSV file."""
    cars = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        cars = [row for row in reader if row.get('Make') and row.get('Model')]
    return cars

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load car data from same directory
    csv_file = os.path.join(script_dir, "car_data.csv")
    cars = load_car_data(csv_file)

    # data 1: length to cargo ratio
    data_1 = []
    for car in cars:
        try:
            length = float(car.get('Length', 0))
            cargo = float(car.get('CargoTotal', 0))
            mpgCombo = float(car.get('MpgCombo', 0))
        except:
            continue
        if length > 0:
            cargo_to_length_ratio = cargo / length
            data_1.append({
                "Make": car['Make'],
                "Model": car['Model'],
                "Length": length,
                "CargoTotal": cargo,
                "CargoToLengthRatio": cargo_to_length_ratio,
                "MpgCombo": mpgCombo
            })
    
    data_1 = sorted(data_1, key=lambda x: x['CargoToLengthRatio'], reverse=True)

    # for entry in data_1[0:10]:
        # print(f"{entry['Make']} {entry['Model']}: {entry['CargoToLengthRatio']:.2f}")
    
    # data 2: above ratio to MPG
    data_2 = []
    for car in data_1:
        make = car['Make']
        model = car['Model']
        cargo_to_length_ratio = car['CargoToLengthRatio']
        mpg_combo = car['MpgCombo']

        if mpg_combo > 0:
            data_2.append({
                "Make": make,
                "Model": model,
                "CargoToLengthRatio": cargo_to_length_ratio,
                "MpgCombo": mpg_combo,
                "RatioToMpg": cargo_to_length_ratio * mpg_combo
            })

    data_2 = sorted(data_2, key=lambda x: x['RatioToMpg'], reverse=True)

    for entry in data_2[2:17]:
        print(f"{entry['Make']} {entry['Model']}: {entry['RatioToMpg']:.2f}")

if __name__ == "__main__":
    main()