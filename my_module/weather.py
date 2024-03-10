from my_module import weather_api
import sqlite3
from my_module import ahu_schedule
from .file_utils import read_api_key_from_file
from .datetime_utils import is_weekend


def weather():

    """Retrieve weather data and store it in the database."""
    # We subtract the time we want to get the data from the given time
    time_in_sec = 1800

    # Openweather Parameters:
    file_path = 'open_weather_api_key.txt'
    weather_api_key = read_api_key_from_file(file_path)

    if weather_api_key:
        """
        lat (str): Latitude of the location.
        lon (str): Longitude of the location.
        """

        lat = '38.02859624338345'
        lon = '23.828109220677746'
        # call the function that brings us the weather data via api
        weather_data = weather_api.weather_api(weather_api_key, lat, lon, time_in_sec)

        print("Next 8-days temperature forecast:")
        for info in weather_data:
            print(info)

        # Establish a connection to the database
        conn = sqlite3.connect('Fivos_Data.db')

        # Create WEATHER SQL Table
        conn.execute('''CREATE TABLE IF NOT EXISTS WEATHER
                        (DATE CHAR(50),
                        MORNING INT,
                        EVENING INT,
                        NIGHT INT);''')

        for info in weather_data:
            conn.cursor().execute("INSERT OR IGNORE INTO WEATHER VALUES (?, ?, ?, ?)",
                                  (info.date, info.morning, info.evening, info.night))
            conn.commit()

        # Create AHU_SCHEDULE SQL Table
        conn.execute('''CREATE TABLE IF NOT EXISTS AHU_SCHEDULE
                        (DATE CHAR(50),
                        TIME CHAR(50),
                        VALUE INT);''')

        # Create a schedule table for the AHU. Best office temperature between 22 and 24°C.
        # Cold air:-1 / Hot air:1 / No air:0
        for info in weather_data:
            if is_weekend(info.date):
                ahu_schedule.ahu_schedule(info.date, 0, 24, 0)
            else:
                ahu_schedule.ahu_schedule(info.date, 0, 7, 0)
                if info.morning < 22:
                    ahu_schedule.ahu_schedule(info.date, 7, 14, 1)
                elif info.morning > 24:
                    ahu_schedule.ahu_schedule(info.date, 7, 14, -1)
                else:
                    ahu_schedule.ahu_schedule(info.date, 7, 14, 0)

                if info.evening < 22:
                    ahu_schedule.ahu_schedule(info.date, 14, 18, 1)
                elif info.evening > 24:
                    ahu_schedule.ahu_schedule(info.date, 14, 18, -1)
                else:
                    ahu_schedule.ahu_schedule(info.date, 14, 18, 0)

                ahu_schedule.ahu_schedule(info.date, 18, 24, 0)

        conn.commit()
        conn.close()
    else:
        print("Failed to read API key from file.")
