import sqlite3
from datetime import datetime


def is_weekend(date_string):
    """Check if a given date is a weekend."""
    # Convert date string to 'YYYY-MM-DD' format
    date_obj = datetime.strptime(date_string, '%d/%m/%Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')

    conn = sqlite3.connect('Fivos_Data.db')
    cursor = conn.cursor()

    # SQLite function to extract day of the week (0-6, where 0 is Sunday)
    cursor.execute("SELECT strftime('%w', ?)", (formatted_date,))
    day_of_week = int(cursor.fetchone()[0])

    conn.close()

    # Check if the day of the week is Saturday (6) or Sunday (0)
    return day_of_week == 0 or day_of_week == 6
