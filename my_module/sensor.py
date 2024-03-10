from my_module import yodiwo_api
import sqlite3
import datetime
from my_module import ahu_schedule
from my_module import weather
from .file_utils import read_api_key_from_file
from .database_utils import get_last_8_dates


def sensor():

    """Retrieve sensor data and update the database."""
    # We subtract the time we want to get the data from the given time
    time_in_sec = 1800

    file_path = 'yodiwo_api_key.txt'
    yodi_api_key = read_api_key_from_file(file_path)

    if yodi_api_key:
        """Measurement ID and Device ID of the sensor from the Yodiwo Platform"""
        measurement_id = '12804'
        device_id = '3474'

        # call the function that brings us the sensor data via api
        yodiwo_data = yodiwo_api.yodiwo_api(yodi_api_key, measurement_id, device_id, time_in_sec)

        print(f"\nTemperature of the office, 30m earlier:\n{yodiwo_data}")

        # Create YODIWO SQL Table:
        # Establish a connection to the database
        conn = sqlite3.connect('Fivos_Data.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS YODIWO
            (TIMESTAMP INT,
            DATE CHAR(50),
            VALUE INT );''')

        # If the table has no data at all, then enter the values you get from the yodiwo api.
        # Then extract the first (and only) tempretature value from the tuple and put it in the valiable 'last_value'

        # Execute a SQL query to count the number of rows in the table
        cursor.execute(f"SELECT COUNT(*) FROM YODIWO")

        # Fetch the result
        row_count = cursor.fetchone()[0]

        # Check if the table is empty
        if row_count == 0:
            cursor.execute("INSERT OR IGNORE INTO YODIWO VALUES (?, ?, ?)",
                           (yodiwo_data.timestamp, yodiwo_data.date, yodiwo_data.value))
            conn.commit()
        else:
            # Execute a SELECT query to fetch the VALUE column of the last row
            cursor.execute("SELECT VALUE FROM YODIWO ORDER BY TIMESTAMP DESC LIMIT 1")
            # Fetch the last row
            last_value = cursor.fetchone()

            if last_value:
                last_value = last_value[0] # Extract the first (and only) element from the tuple

                # Checks if the difference between the new temperature and the previous temperature is between 1 °C,
                # then does not add it to the database
                if abs(last_value - yodiwo_data.value) > 1:
                    cursor.execute("INSERT OR IGNORE INTO YODIWO VALUES (?, ?, ?)",
                                   (yodiwo_data.timestamp, yodiwo_data.date, yodiwo_data.value))
                    conn.commit()

                    # if the office temperature is not between 22 and 24°C, then change the AHU program accordingly
                    dt_object = datetime.datetime.fromtimestamp(yodiwo_data.timestamp)
                    hour = dt_object.hour

                    new_timestamp = yodiwo_data.timestamp - 3600
                    dt_object = datetime.datetime.fromtimestamp(new_timestamp)
                    new_hour = dt_object.hour

                    # Check if the table exists
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name= 'WEATHER'")
                    result = cursor.fetchone()

                    if result:
                        # Query to fetch the distinct last 8 dates
                        last_8_dates = get_last_8_dates()

                        if yodiwo_data.value < 20:
                            for date in last_8_dates:
                                # If it is not a weekend, then update the ahu schedule
                                if not weather.is_weekend(date[0]):
                                    ahu_schedule.ahu_schedule_overwrite(date[0], new_hour, hour, 1)
                            print("The AHU Schedule changed, the office was a little bit cold\n")
                        elif yodiwo_data.value > 24:
                            for date in last_8_dates:
                                if not weather.is_weekend(date[0]):
                                    ahu_schedule.ahu_schedule_overwrite(date[0], new_hour, hour, 0)
                            print("The AHU Schedule changed, the office was a little bit hot\n")
                else:
                    print("The office temperature is fine")
            else:
                print("No data found in the table.")

        conn.close()
    else:
        print("Failed to read API key from file.")
