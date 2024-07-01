import os
import json
import random
from datetime import datetime, timedelta
from faker import Faker
import numpy as np

# Configuration
No_of_files = 5000
flight_min = 50 
flight_max = 100
city_min = 100
city_max = 200
L_avg = 0.003

fake = Faker()

random_city_count = random.randint(city_min, city_max)
cities = [fake.city() for c in range(random_city_count)]

# create directory
output_dir = "/tmp/flights"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def generate_random_date():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

def generate_flight_record():
    date = generate_random_date()
    origin_city = random.choice(cities)
    destination_city = random.choice(cities)
    while destination_city == origin_city:
        destination_city = random.choice(cities)
    flight_duration_secs = random.randint(30 * 60, 12 * 60 * 60)
    passengers_on_board = random.randint(50, 300)

    fields = {
        "date": date.isoformat() if date else None,
        "origin_city": origin_city,
        "destination_city": destination_city,
        "flight_duration_secs": flight_duration_secs,
        "passengers_on_board": passengers_on_board
    }
    for key in fields:
        if random.random() < L_avg:
            fields[key] = np.nan

    return fields

def generate_flights_data():
    return [generate_flight_record() for _ in range(random.randint(flight_min, flight_max))]

def main():
    for i in range(No_of_files):
        flights_data = generate_flights_data()
        sample_date = generate_random_date()
        month_year = sample_date.strftime("%m-%y")
        origin_city = random.choice(cities)
        file_name = f"{month_year}-{origin_city}-flights.json"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, 'w') as json_file:
            json.dump(flights_data, json_file, indent=4)
        print("Generated {No_of_files} JSON files in {output_dir}")

if __name__ == "__main__":
    main()