import io
import pandas as pd
import requests
from datetime import datetime

# Load the CSV data
data = pd.read_csv("D:/Data_Engineer/Uber_DE_Project/uber_data.csv")

# Rename columns to match PostgreSQL schema
column_rename_map = {
    'VendorID': 'vendor_id',
    'tpep_pickup_datetime': 'pickup_datetime',
    'tpep_dropoff_datetime': 'dropoff_datetime',
    'passenger_count': 'passenger_count',
    'trip_distance': 'trip_distance',
    'pickup_longitude': 'pickup_longitude',
    'pickup_latitude': 'pickup_latitude',
    'RatecodeID': 'rate_code_id',
    'payment_type': 'payment_type',
    'fare_amount': 'fare_amount',
    'extra': 'extra',
    'mta_tax': 'mta_tax',
    'tip_amount': 'tip_amount',
    'tolls_amount': 'tolls_amount',
    'improvement_surcharge': 'improvement_surcharge',
    'total_amount': 'total_amount'
}

data.rename(columns=column_rename_map, inplace=True)

data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'])
data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime'])


# Drop duplicate rows and reset index properly
data = data.drop_duplicates().reset_index(drop=True)

# Assign trip_id as new index
data['trip_id'] = data.index

datetime_dim = data[['pickup_datetime', 'dropoff_datetime']].reset_index(drop=True)


# Extract components from pickup datetime
datetime_dim['pickup_hour'] = datetime_dim['pickup_datetime'].dt.hour
datetime_dim['pickup_day'] = datetime_dim['pickup_datetime'].dt.day
datetime_dim['pickup_month'] = datetime_dim['pickup_datetime'].dt.month
datetime_dim['pickup_year'] = datetime_dim['pickup_datetime'].dt.year
datetime_dim['pickup_weekday'] = datetime_dim['pickup_datetime'].dt.weekday


# Extract components from dropoff datetime
datetime_dim['dropoff_hour'] = datetime_dim['dropoff_datetime'].dt.hour
datetime_dim['dropoff_day'] = datetime_dim['dropoff_datetime'].dt.day
datetime_dim['dropoff_month'] = datetime_dim['dropoff_datetime'].dt.month
datetime_dim['dropoff_year'] = datetime_dim['dropoff_datetime'].dt.year
datetime_dim['dropoff_weekday'] = datetime_dim['dropoff_datetime'].dt.weekday


# Create datetime_id as index
datetime_dim['datetime_id'] = datetime_dim.index

# Reorder columns to match PostgreSQL schema if needed
datetime_dim = datetime_dim[['datetime_id', 'pickup_datetime', 'pickup_hour', 'pickup_day', 'pickup_month', 'pickup_year', 'pickup_weekday',
                             'dropoff_datetime', 'dropoff_hour', 'dropoff_day', 'dropoff_month', 'dropoff_year', 'dropoff_weekday']]


# Save the cleaned Dataset to a new CSV file
cleaned_csv_path = 'D:/Data_Engineer/Uber_DE_Project/cleaned_uber_data.csv'

# Save to CSV with header and without index column
data.to_csv(cleaned_csv_path, index=False, header=True)


passenger_count_dim = data[['passenger_count']].reset_index(drop=True)
passenger_count_dim['passenger_count_id'] = passenger_count_dim.index
passenger_count_dim = passenger_count_dim[['passenger_count_id','passenger_count']]

trip_distance_dim = data[['trip_distance']].reset_index(drop=True)
trip_distance_dim['trip_distance_id'] = trip_distance_dim.index
trip_distance_dim = trip_distance_dim[['trip_distance_id','trip_distance']]


rate_code_mapping = {
    1: 'Standard rate',
    2: 'JFK',
    3: 'Newark',
    4: 'Nassau or Westchester',
    5: 'Negotiated fare',
    6: 'Group ride'
}

data['rate_code_name'] = data['rate_code_id'].map(rate_code_mapping)
rate_code_dim = data[['rate_code_id', 'rate_code_name']].drop_duplicates().reset_index(drop=True)
rate_code_dim['rate_code_dim_id'] = rate_code_dim.index
rate_code_dim = rate_code_dim[['rate_code_dim_id', 'rate_code_id', 'rate_code_name']]
