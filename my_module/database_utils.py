import sqlite3


def get_last_8_dates():
    """Retrieve the last 8 distinct dates from the database."""
    conn = sqlite3.connect('Fivos_Data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT DATE FROM WEATHER ORDER BY DATE ASC LIMIT 8")
    last_8_dates = cursor.fetchall()

    conn.close()

    return last_8_dates
