Description: 
This project aims to create a smart office air conditioning system by integrating weather data from the OpenWeatherMap API and sensor data from the Yodiwo platform into a Flask web application. 
The data is stored in a SQLite database and used to optimize the office air conditioner's schedule for maximum efficiency. Key features include:

1.	Data Retrieval: Fetches weather data from the OpenWeatherMap API and sensor data from the Yodiwo platform. Only necessary sensor data is stored to avoid database clutter.
2.	Data Storage: Stores weather and sensor data in a SQLite database for easy retrieval and management. The database is optimized to store only relevant sensor data.
3.	Dynamic Schedule Optimization: Utilizes the next week's weather data to generate a one-week schedule for the office air conditioner. The schedule is adjusted dynamically
    based on real-time sensor data to maintain optimal indoor temperatures. Whenever the sensor detects temperatures outside the desired range for an office space, the air conditioner's schedule is automatically adjusted to improve efficiency.
5.	Web Interface: Provides a user-friendly web interface using Flask to visualize weather and sensor data, as well as the current air conditioning schedule.
6.	API Endpoints: Exposes endpoints to retrieve weather and sensor data in JSON format, facilitating integration with other applications or services.
   
Technologies Used:
•	Python
•	Flask
•	SQLite
•	OpenWeatherMap API
•	Yodiwo API

Purpose: The purpose of this project is to demonstrate the integration of external data sources with a web application to create a smart office air conditioning system. 
By dynamically adjusting the air conditioner's schedule based on real-time weather and sensor data, the project showcases how technology can be used to optimize energy consumption and improve comfort in office environments. 
This project can serve as a blueprint for building smart HVAC systems that adapt to changing environmental conditions and user preferences.

Steps:
1. In the file: open_weather_api_key.txt, paste your api key from open weather
2. In the file: yodiwo_api_key.txt, paste your api key from the sensor on the platform where you're drawing your data
3. Change the measurement ID and device ID of your sensor (If available, otherwise comment these inputs) accordingly in lines 21 and 22 of sensor.py module
4. Change the api endpoint and headers on line 32-36, and the api request url on line 45 of yodiwo_api.py accordingly, depending on the api manual provided by the platform you want to get the sensor data from
5. Change the name Fivos_Data.db with the name of your own database, in all modules and files 
6. Run schedule_manager.py to start the schedule where the data will be fetched from the platforms. If you want to change the time at which the data is fetched, change lines 13 and 17 in schedule_manager.py accordingly
7. Run flask_graphs.py to display the data in real-time graphs on the local url of your computer: http://127.0.0.1:5000 or on the url of your WiFi network: http://192.168.1.43:5000

![IoT Platform](https://github.com/Fivos-Garpo/Integrating-Weather-and-Sensor-Data-with-Flask-and-SQLite-for-Smart-Office-Air-Conditioning/assets/101002242/be64f686-87dd-40b7-ac11-b7f918120f54)

