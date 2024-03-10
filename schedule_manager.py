# schedule_manager.py
import schedule
import time
from my_module import sensor
from my_module import weather


def main():
    # Run the weather and sensor functions once at the beginning
    weather.weather()
    sensor.sensor()

    # Schedule the weather function to run once every 8 days
    schedule.every(8).days.do(weather.weather)

    # Schedule the sensor function to run every 30 minutes
    schedule.every(30).minutes.do(sensor.sensor)

    # Infinite loop to continuously check and execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
