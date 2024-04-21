from google.cloud import bigquery
from google.oauth2 import service_account

def setup_bigquery_client() -> bigquery.Client:
    """
    Sets up and returns a BigQuery client using credentials from a service account file.
    """
    credentials = service_account.Credentials.from_service_account_file('./gcp_key.json')
    project_id = 'nice-etching-420812'
    return bigquery.Client(credentials=credentials, project=project_id)

def insert_weather_data(temperature: float, pressure: float, humidity: float) -> bool:
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
        {"temperature": temperature, "pressure": pressure, "humidity": humidity}
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
        return {"temperature": row.temperature, "pressure": row.pressure, "humidity": row.humidity}

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
