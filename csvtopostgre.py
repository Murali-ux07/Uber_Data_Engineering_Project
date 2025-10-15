import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection URL, replace placeholders with your values
db_url = "postgresql+psycopg2://postgres:murali@localhost:5432/uber_analytics"
engine = create_engine(db_url)

# Function to load a CSV file to a PostgreSQL table
def load_csv_to_postgres(csv_file, table_name):
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"{table_name} loaded successfully.")


# Load all dimension tables
load_csv_to_postgres('D:/Data_Engineer/Uber_DE_Project/passenger_count_dim.csv', 'passenger_count_dim')
load_csv_to_postgres('D:/Data_Engineer/Uber_DE_Project/trip_distance_dim.csv', 'trip_distance_dim')
load_csv_to_postgres('D:/Data_Engineer/Uber_DE_Project/rate_code_dim.csv', 'rate_code_dim')
load_csv_to_postgres('D:/Data_Engineer/Uber_DE_Project/payment_type_dim.csv', 'payment_type_dim')
load_csv_to_postgres('D:/Data_Engineer/Uber_DE_Project/pickup_location_dim.csv', 'pickup_location_dim')
load_csv_to_postgres('D:/Data_Engineer/Uber_DE_Project/dropoff_location_dim.csv', 'dropoff_location_dim')
load_csv_to_postgres('D:/Data_Engineer/Uber_DE_Project/datetime_dim.csv', 'datetime_dim')

# Load fact table
load_csv_to_postgres('D:/Data_Engineer/Uber_DE_Project/fact_table.csv', 'fact_table')
