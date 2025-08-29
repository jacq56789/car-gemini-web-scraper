#!/usr/bin/env python3
"""Generate detailed prompts for car specification searches."""

def generate_car_search_prompt(make, model, year_range="2015-2020"):   
    prompt = f"""
SEARCH PROMPT FOR: {make} {model}

Please find the following specifications for the {make} {model} ({year_range}):

REQUIRED DATA POINTS:
0. Year: [Model year: XXXX]
1. BodyType [Sedan, Coupe, SUV, etc.]
2. Cost: [Edmunds, Kelly Blue Book, CarGurus, etc.]
3. Length: [Overall length in inches: XXX.X]
4. CargoRear: [Rear cargo space in cubic feet: XX.X]
5. CargoTotal: [Total cargo space with seats folded in cubic feet: XX.X]
6. MpgCity: [EPA city fuel economy: XX]
7. MpgHwy: [EPA highway fuel economy: XX]
8. MpgCombo: [EPA combined fuel economy: XX]
9. FuelType: [Gasoline/Diesel/Hybrid/Electric/Plug-in Hybrid]
10. Drive: [FWD/RWD/AWD/4WD]
11. Reliability: [Edmunds, Kelly Blue Book, CarGurus, etc.]

SEARCH TERMS TO USE:
- "{make} {model} {year_range} specifications"
- "{make} {model} {year_range} MSRP price"
- "{make} {model} {year_range} dimensions cargo space"
- "{make} {model} {year_range} fuel economy MPG"
- "{make} {model} {year_range} drivetrain"

PREFERRED SOURCES:
- Official manufacturer websites ({make.lower()}.com)
- Edmunds.com
- KBB.com (Kelley Blue Book)
- Cars.com
- MotorTrend.com
- Car and Driver
- EPA fuel economy database

FORMAT YOUR FINDINGS AS:
Year: [value]
BodyType: [value]
Cost: [value]
Length: [value]
CargoRear: [value]
CargoTotal: [value]
MpgCity: [value]
MpgHwy: [value]
MpgCombo: [value]
FuelType: [value]
Drive: [value]
Reliability: [value]

NOTES:
- If multiple trim levels exist, use the BASE/ENTRY level specifications
- If data varies by year within range, use the MOST COMMON year (typically 2015-2020)
- Mark any unavailable data as "N/A"
- For electric vehicles, use "Electric" for FuelType and MPGe values for fuel economy
"""
    
    return prompt.strip()

def main():
    import pyperclip
    make = "Mazda"
    model = "3 Hatchback"
    prompt = generate_car_search_prompt(make, model)
    pyperclip.copy(prompt)
    print(f"Generated prompt for {make} {model} and copied to clipboard.")
    print(prompt)

if __name__ == "__main__":
    main()
