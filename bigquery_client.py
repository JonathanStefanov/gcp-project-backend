from google.cloud import bigquery
from google.oauth2 import service_account
import os.path

def setup_bigquery_client() -> bigquery.Client:
    """
    Sets up and returns a BigQuery client using credentials from a service account file.
    """
    # Checks if local environment or Google Cloud environment
    # check if file ./gcp_key.json exists
    project_id = 'nice-etching-420812'

    if os.path.isfile('./gcp_key.json'):
        credentials = service_account.Credentials.from_service_account_file('./gcp_key.json')
        return bigquery.Client(credentials=credentials, project=project_id)
    else:
        return bigquery.Client(project=project_id)

def insert_weather_data(temperature: float, pressure: float, humidity: float, co2: float) -> bool:
    """
    Inserts weather data into the BigQuery table.

    Parameters:
    temperature (float): The temperature value to insert.
    pressure (float): The pressure value to insert.
    humidity (float): The humidity value to insert.
    """
    client = setup_bigquery_client()
    table_id = "nice-etching-420812.project.indoor_weather"
    
    rows_to_insert = [
        {"temperature": temperature, "pressure": pressure, "humidity": humidity, "co2": co2}
    ]
    
    errors = client.insert_rows_json(table_id, rows_to_insert)
    
    return errors == []

def get_last_weather_data() -> dict:
    """
    Retrieves the most recent weather data record from the BigQuery table.
    """
    client = setup_bigquery_client()
    table_id = "nice-etching-420812.project.indoor_weather"
    
    query = f"""
    SELECT *
    FROM `{table_id}`
    ORDER BY entry_timestamp DESC
    LIMIT 1
    """
    
    query_job = client.query(query)  # Make an API request.
    results = query_job.result()  # Wait for the job to complete.
    
    for row in results:
        return {"temperature": row.temperature, "pressure": row.pressure, "humidity": row.humidity, "co2": row.co2}
    
def get_current_user_name() -> dict:
    """
    Retrieves a user name from the BigQuery table `current_user`.
    """
    client = setup_bigquery_client()
    table_id = "nice-etching-420812.project.current_user"
    
    query = f"""
    SELECT name
    FROM `{table_id}`
    LIMIT 1
    """
    
    query_job = client.query(query)  # Make an API request.
    results = query_job.result()  # Wait for the job to complete.
    
    for row in results:
        return row.name

    return "Unknown User"  # Return None if no rows are found

def update_current_user_name(new_name: str):
    """
    Updates the user name in the BigQuery table `current_user`.
    """
    client = setup_bigquery_client()
    table_id = "nice-etching-420812.project.current_user"
    
    query = f"""
    UPDATE `{table_id}`
    SET name = '{new_name}'
    WHERE TRUE  -- Updates all rows in the table. Adjust the condition as needed.
    """
    
    query_job = client.query(query)  # Make an API request.
    query_job.result()  # Wait for the job to complete.
    
    print(f"User name updated to '{new_name}'.")

def get_all_weather_data() -> list:
    """
    Retrieves all weather data records from the BigQuery table.
    """
    client = setup_bigquery_client()
    table_id = "nice-etching-420812.project.indoor_weather"
    
    query = f"""
    SELECT *
    FROM `{table_id}`
    ORDER BY entry_timestamp DESC
    """
    
    query_job = client.query(query)  # Make an API request.
    results = query_job.result()  # Wait for the job to complete.
    
    all_data = []
    for row in results:
        all_data.append({"temperature": row.temperature, "pressure": row.pressure, "humidity": row.humidity})
    
    return all_data

def get_mean_weather_data_per_hour() -> list:
    """
    Retrieves mean temperature, pressure, and humidity per hour from the BigQuery table.
    """
    client = setup_bigquery_client()
    table_id = "nice-etching-420812.project.indoor_weather"

    query = f"""
    SELECT
        TIMESTAMP_TRUNC(entry_timestamp, HOUR) as hour,
        AVG(temperature) as avg_temperature,
        AVG(pressure) as avg_pressure,
        AVG(humidity) as avg_humidity
    FROM `{table_id}`
    GROUP BY hour
    ORDER BY hour DESC
    """

    query_job = client.query(query)  # Make an API request.
    results = query_job.result()  # Wait for the job to complete.

    hourly_data = []
    for row in results:
        hourly_data.append({
            "hour": row.hour,
            "avg_temperature": row.avg_temperature,
            "avg_pressure": row.avg_pressure,
            "avg_humidity": row.avg_humidity
        })

    return hourly_data


def get_last_ping_time() -> str:
    """
    Retrieves the most recent ping time from the BigQuery table.
    """
    client = setup_bigquery_client()
    table_id = "nice-etching-420812.project.indoor_weather"
    
    query = f"""
    SELECT *
    FROM `{table_id}`
    ORDER BY entry_timestamp DESC
    LIMIT 1
    """
    
    query_job = client.query(query)  # Make an API request.
    results = query_job.result()  # Wait for the job to complete.
    
    for row in results:
        return row.entry_timestamp
    



