import pandas as pd

# Load cleaned Uber dataset
data = pd.read_csv('D:/Data_Engineer/Uber_DE_Project/cleaned_uber_data.csv')

# Map rate_code_id to descriptive names
rate_code_mapping = {
    1: 'Standard rate',
    2: 'JFK',
    3: 'Newark',
    4: 'Nassau or Westchester',
    5: 'Negotiated fare',
    6: 'Group ride'
}
data['rate_code_name'] = data['rate_code_id'].map(rate_code_mapping)

# Map payment_type to descriptive names (Replace as per your actual values)
payment_type_mapping = {
    1: 'Credit card',
    2: 'Cash',
    3: 'No charge',
    4: 'Dispute',
    5: 'Unknown',
    6: 'Voided trip'
}
data['payment_type_name'] = data['payment_type'].map(payment_type_mapping)

# Passenger Count Dimension
passenger_count_dim = data[['passenger_count']].drop_duplicates().reset_index(drop=True)
passenger_count_dim['passenger_count_id'] = passenger_count_dim.index
passenger_count_dim = passenger_count_dim[['passenger_count_id', 'passenger_count']]
passenger_count_dim.to_csv('D:/Data_Engineer/Uber_DE_Project/passenger_count_dim.csv', index=False)

# Trip Distance Dimension
trip_distance_dim = data[['trip_distance']].drop_duplicates().reset_index(drop=True)
trip_distance_dim['trip_distance_id'] = trip_distance_dim.index
trip_distance_dim = trip_distance_dim[['trip_distance_id', 'trip_distance']]
trip_distance_dim.to_csv('D:/Data_Engineer/Uber_DE_Project/trip_distance_dim.csv', index=False)

# Rate Code Dimension
rate_code_dim = data[['rate_code_id', 'rate_code_name']].drop_duplicates().reset_index(drop=True)
rate_code_dim['rate_code_dim_id'] = rate_code_dim.index
rate_code_dim = rate_code_dim[['rate_code_dim_id', 'rate_code_id', 'rate_code_name']]
rate_code_dim.to_csv('D:/Data_Engineer/Uber_DE_Project/rate_code_dim.csv', index=False)

# Payment Type Dimension
payment_type_dim = data[['payment_type', 'payment_type_name']].drop_duplicates().reset_index(drop=True)
payment_type_dim['payment_type_id'] = payment_type_dim.index
payment_type_dim = payment_type_dim[['payment_type_id', 'payment_type', 'payment_type_name']]
payment_type_dim.to_csv('D:/Data_Engineer/Uber_DE_Project/payment_type_dim.csv', index=False)

# Pickup Location Dimension
pickup_location_dim = data[['pickup_latitude', 'pickup_longitude']].drop_duplicates().reset_index(drop=True)
pickup_location_dim['pickup_location_id'] = pickup_location_dim.index
pickup_location_dim = pickup_location_dim[['pickup_location_id', 'pickup_latitude', 'pickup_longitude']]
pickup_location_dim.to_csv('D:/Data_Engineer/Uber_DE_Project/pickup_location_dim.csv', index=False)

# Dropoff Location Dimension
dropoff_location_dim = data[['dropoff_latitude', 'dropoff_longitude']].drop_duplicates().reset_index(drop=True)
dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.index
dropoff_location_dim = dropoff_location_dim[['dropoff_location_id', 'dropoff_latitude', 'dropoff_longitude']]
dropoff_location_dim.to_csv('D:/Data_Engineer/Uber_DE_Project/dropoff_location_dim.csv', index=False)

# Datetime Dimension
data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'])
data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime'])
datetime_dim = data[['pickup_datetime', 'dropoff_datetime']].drop_duplicates().reset_index(drop=True)
datetime_dim['pickup_hour'] = datetime_dim['pickup_datetime'].dt.hour
datetime_dim['pickup_day'] = datetime_dim['pickup_datetime'].dt.day
datetime_dim['pickup_month'] = datetime_dim['pickup_datetime'].dt.month
datetime_dim['pickup_year'] = datetime_dim['pickup_datetime'].dt.year
datetime_dim['pickup_weekday'] = datetime_dim['pickup_datetime'].dt.weekday
datetime_dim['dropoff_hour'] = datetime_dim['dropoff_datetime'].dt.hour
datetime_dim['dropoff_day'] = datetime_dim['dropoff_datetime'].dt.day
datetime_dim['dropoff_month'] = datetime_dim['dropoff_datetime'].dt.month
datetime_dim['dropoff_year'] = datetime_dim['dropoff_datetime'].dt.year
datetime_dim['dropoff_weekday'] = datetime_dim['dropoff_datetime'].dt.weekday
datetime_dim['datetime_id'] = datetime_dim.index
datetime_dim = datetime_dim[['datetime_id', 'pickup_datetime', 'pickup_hour', 'pickup_day',
                             'pickup_month', 'pickup_year', 'pickup_weekday',
                             'dropoff_datetime', 'dropoff_hour', 'dropoff_day',
                             'dropoff_month', 'dropoff_year', 'dropoff_weekday']]
datetime_dim.to_csv('D:/Data_Engineer/Uber_DE_Project/datetime_dim.csv', index=False)

# Create fact table by joining surrogate keys
fact_table = data.copy()

# Map each surrogate key column in fact table by matching original column with dimension
fact_table = fact_table.merge(passenger_count_dim, on='passenger_count', how='left')
fact_table = fact_table.merge(trip_distance_dim, on='trip_distance', how='left')
fact_table = fact_table.merge(rate_code_dim, on=['rate_code_id', 'rate_code_name'], how='left')
fact_table = fact_table.merge(payment_type_dim, on=['payment_type', 'payment_type_name'], how='left')
fact_table = fact_table.merge(pickup_location_dim, on=['pickup_latitude', 'pickup_longitude'], how='left')
fact_table = fact_table.merge(dropoff_location_dim, on=['dropoff_latitude', 'dropoff_longitude'], how='left')
fact_table = fact_table.merge(datetime_dim, left_on=['pickup_datetime', 'dropoff_datetime'], right_on=['pickup_datetime', 'dropoff_datetime'], how='left')

# Select only surrogate keys and fact measures for optimized fact table
fact_table_final = fact_table[['trip_id', 'passenger_count_id', 'trip_distance_id', 'rate_code_dim_id',
                               'payment_type_id', 'pickup_location_id', 'dropoff_location_id', 'datetime_id',
                               'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
                               'improvement_surcharge', 'total_amount']]

fact_table_final.to_csv('D:/Data_Engineer/Uber_DE_Project/fact_table.csv', index=False)

print("All dimension tables and fact table created and saved successfully.")
