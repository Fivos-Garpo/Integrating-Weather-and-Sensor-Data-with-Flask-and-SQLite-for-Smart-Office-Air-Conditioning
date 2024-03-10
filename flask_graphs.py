from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)


# Function to fetch data from SQLite
def fetch_data(query):
    """
    Fetch data from SQLite database.

    Parameters:
        query (str): SQL query to execute.

    Returns:
        list: List of fetched data.
    """
    conn = sqlite3.connect('Fivos_Data.db')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


@app.route('/')
def index():
    """Render index page."""
    return render_template('index.html')


@app.route('/Yodiwo_Data')
def get_yodiwo_data():
    """Fetch and return Yodiwo data."""
    data = fetch_data("SELECT date, value FROM YODIWO")
    return jsonify(data)


@app.route('/OpenWeather_Data')
def get_openweather_data():
    """Fetch and return OpenWeather data."""
    data = fetch_data("SELECT date, morning, evening, night FROM WEATHER")
    return jsonify(data)


@app.route('/Schedule_Weather_Data')
def get_schedule_weather_data():
    """Fetch and return schedule weather data."""
    data = fetch_data("SELECT date, value FROM AHU_SCHEDULE")
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
