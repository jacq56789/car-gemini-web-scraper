#!/usr/bin/env python3
"""Car search using Google Gemini AI to extract vehicle specifications."""

import csv
import json
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai
from car_search_prompt import generate_car_search_prompt

GEMINI_MODEL = "gemini-2.0-flash-lite"
REQUESTS_PER_MINUTE = 30
request_times = []

def wait_for_rate_limit():
    """Implement rate limiting to respect API limits."""
    global request_times
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(minutes=1)
    request_times = [req for req in request_times if req > cutoff_time]
    
    if len(request_times) >= REQUESTS_PER_MINUTE:
        oldest_request = min(request_times)
        wait_seconds = (oldest_request + timedelta(minutes=1) - current_time).total_seconds()
        if wait_seconds > 0:
            print(f"⏳ Rate limit reached. Waiting {wait_seconds:.1f}s...")
            time.sleep(wait_seconds)
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(minutes=1)
            request_times = [req for req in request_times if req > cutoff_time]
    
    request_times.append(current_time)
    print(f"📊 Requests in last minute: {len(request_times)}/{REQUESTS_PER_MINUTE}")

def load_car_data(csv_file):
    """Load car data from CSV file."""
    cars = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        cars = [row for row in reader if row.get('Make') and row.get('Model')]
    return cars

def search_car_with_gemini(make: str, model: str, client: genai.Client):
    """Search for car specifications using Gemini AI."""
    prompt = generate_car_search_prompt(make, model)
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt]
        )
        return response.text
    except Exception as e:
        if 'API key not valid' in str(e):
            raise ValueError("Invalid API Key. Please check your GEMINI_API_KEY in the .env file.")
        print(f"Error searching for {make} {model}: {e}")
        return None

def main():
    """Main function to process car data with Gemini AI"""
    # Load environment variables from local .env file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    load_dotenv(env_path)
    
    # The Gemini client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client()
    
    # Load car data from same directory
    csv_file = os.path.join(script_dir, "car_data.csv")
    cars = load_car_data(csv_file)
    
    print(f"Processing {len(cars)} cars with Gemini AI...")
    
    results = []

    # Process all cars
    for i, car in enumerate(cars):
        make = car['Make']
        model = car['Model']

        print(f"[{i+1}/{len(cars)}] Searching for {make} {model}...")
        
        # Wait for rate limit before making request
        wait_for_rate_limit()
        
        # Search with Gemini
        response = search_car_with_gemini(make, model, client)
        
        # Store result
        result = {
            "make": make,
            "model": model,
            "gemini_response": response
        }
        results.append(result)
    
    # Save results to JSON in same directory
    output_file = os.path.join(script_dir, "car_search.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Results saved to {output_file}")

if __name__ == "__main__":
    main()
