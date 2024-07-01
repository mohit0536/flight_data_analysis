import os
import json
import time
import glob
import numpy as np
import pandas as pd

input_dir = "/tmp/flights"

def combine_data():
    data = []
    for file_path in glob.glob(os.path.join(input_dir, '**/*.json'), recursive=True):
        with open(file_path, 'r') as file:
            records = json.load(file)
            data.extend(records)
    return pd.DataFrame(data)

def process_data(df):
    total_records = len(df)
    dirty_records = df.isnull().any(axis=1).sum()
    
    clean_df = df.dropna()
    
    top_25_destinations = clean_df['destination_city'].value_counts().head(25).index
    top_25_df = clean_df[clean_df['destination_city'].isin(top_25_destinations)]
    
    city_stats = top_25_df.groupby('destination_city')['flight_duration_secs'].agg(['mean', lambda x: np.percentile(x, 95)]).reset_index()
    city_stats.columns = ['destination_city', 'avg_duration', 'p95_duration']

    passengers_arrived = clean_df.groupby('destination_city')['passengers_on_board'].sum().reset_index()
    passengers_left = clean_df.groupby('origin_city')['passengers_on_board'].sum().reset_index()

    # for top 2
    max_arrived_city = passengers_arrived.iloc[passengers_arrived['passengers_on_board'].nlargest(2).index]
    max_left_city = passengers_left.iloc[passengers_left['passengers_on_board'].nlargest(2).index]
    # for top
    # max_arrived_city = passengers_arrived.iloc[passengers_arrived['passengers_on_board'].idxmax()]
    # max_left_city = passengers_left.iloc[passengers_left['passengers_on_board'].idxmax()]

    return total_records, dirty_records, city_stats, max_arrived_city, max_left_city

def main():
    start_time = time.time()

    df = combine_data()
    total_records, dirty_records, city_stats, max_arrived_city, max_left_city = process_data(df)

    end_time = time.time()
    run_duration = end_time - start_time

    print("Total records processed: {0}".format(total_records))
    print("Dirty records: {0}".format(dirty_records))
    print("Total run duration: {0} seconds".format(run_duration))

    print("\nStatistics for Top 25 Destination Cities:")
    print(city_stats)
    
    # for city name print
    # print("City with max passengers arrived: {0}".format("|".join(max_arrived_city['destination_city'].tolist())))
    # print("City with max passengers left: {0}".format("|".join(max_left_city['origin_city'].tolist())))
    
    # for passengers count print
    print("City with max passengers arrived: {0}".format(max_arrived_city.to_dict(orient='records')))
    print("City with max passengers left: {0}".format(max_left_city['origin_city'].tolist()))
    lines = [
    "Total records processed: {0}".format(total_records),
    "Dirty records: {0}".format(dirty_records),
    "Total run duration: {0} seconds".format(run_duration),
    "City with max passengers arrived: {0}".format(max_arrived_city.to_dict(orient='records')),
    "City with max passengers left: {0}".format(max_left_city['origin_city'].tolist())]
    with open("results.txt", 'w') as file:
        for line in lines:
            file.write(line + "\n")

if __name__ == "__main__":
    main()