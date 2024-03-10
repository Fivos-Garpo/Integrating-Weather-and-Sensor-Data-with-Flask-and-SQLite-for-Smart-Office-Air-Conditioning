import requests
import time
from datetime import datetime


class Weather:
    """Class to represent weather data."""
    def __init__(self, date, morning, evening, night):
        self.date = date
        self.morning = morning
        self.evening = evening
        self.night = night

    def __str__(self):
        return f"Date: {self.date} Morning: {self.morning} Evening: {self.evening} Night: {self.night}"


def weather_api(weather_api_key, lat, lon, time_in_sec):
    from schedule_manager import main
    """
    Retrieve weather data from the OpenWeatherMap API.

    Parameters:
        weather_api_key (str): API key for accessing the OpenWeatherMap API.
        lat (str): Latitude of the location.
        lon (str): Longitude of the location.
        time_in_sec (int): Time in seconds for which to retrieve weather data.

    Returns:
        list: List of Weather objects representing weather information.
    """
    # OpenWeather API endpoint
    api_endpoint = 'https://api.openweathermap.org/data/3.0/onecall'

    # Get the current time
    current_timestamp = int(time.time())

    # Subtract from the current time
    time_sub = current_timestamp - time_in_sec

    # Construct the API request URL
    api_url = f'{api_endpoint}?lat={lat}&lon={lon}&exclude=current,minutely,hourly,' \
              f'alerts&units=metric&dt={time_sub}&appid={weather_api_key}'

    # Make the API request
    try:
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            json_response = response.json()
            weekly_weather_info = []

            data = json_response['daily']

            for x in data:
                formatted_date = datetime.fromtimestamp(x['dt']).strftime('%d/%m/%Y')
                weekly_weather_info.append(Weather(formatted_date, x['temp']['morn'], x['temp']['eve'],
                                                   x['temp']['night']))

            return weekly_weather_info
        else:
            return f'Error: {response.status_code}, {response.text}'

    # If there is a problem with the connection or with the type of data, retries after 30 minutes.
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
