import requests
import time
from datetime import datetime, timezone


class Yodiwo:
    """Class to represent Yodiwo data."""
    def __init__(self, timestamp, date, value):
        self.timestamp = timestamp
        self.date = date
        self.value = value

    def __str__(self):
        return f"Timestamp: {self.timestamp} Date: {self.date} Temperature {self.value}"


def yodiwo_api(yodi_api_key, measurement_id, device_id, time_in_sec):
    from schedule_manager import main
    """
    Retrieve Yodiwo data from the API.

    Parameters:
        yodi_api_key (str): API key for accessing the Yodiwo API.
        measurement_id (str): Measurement ID for the data.
        device_id (str): Device ID for the data.
        time_in_sec (int): Time in seconds for which to retrieve data.

    Returns:
        Yodiwo: Yodiwo object representing retrieved data.
    """
    # Yodiwo API endpoint and headers
    api_endpoint = 'https://fm2service.yodiwo.com/fm/data'
    headers = {
        'Authorization': 'Bearer YourAccessToken',  # Replace YourAccessToken with actual token
        'Content-Type': 'application/json',
        'x-api-key': yodi_api_key
    }
    # Get the current time
    current_timestamp = int(time.time())

    # Subtract from the current time
    time_sub = current_timestamp - time_in_sec

    # Construct the API request URL
    api_url = f'{api_endpoint}?mid={measurement_id}&id={device_id}&start={time_sub}'

    # Make the API request
    try:
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            json_response = response.json()

            # Extract relevant data
            data = json_response['Results'][0]['Entries'][0]['Temperature']
            timestamp_str = json_response['Results'][0]['Entries'][0]['Time']

            # Convert the time string to a timestamp
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()

            # Format date and create Yodiwo object
            formatted_date = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
            yodiwo_data = Yodiwo(int(timestamp), formatted_date, round(float(data), 2))

            return yodiwo_data
        else:
            return f'Error: {response.status_code}, {response.text}'

    except requests.exceptions.ConnectionError as connection_error:
        print("Connection Error:", connection_error)
        # Wait for 30 minutes
        time.sleep(1800)
        main()
    except TypeError as type_error:
        print("TypeError:", type_error)
        # Wait for 30 minutes
        time.sleep(1800)
        main()
