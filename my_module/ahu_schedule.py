import sqlite3


def ahu_schedule(date, start_hour, end_hour, ahu_value):
    """
    Insert AHU schedule values into the database.

    Parameters:
        date (str): Date for which the schedule is applied.
        start_hour (int): Start hour of the schedule.
        end_hour (int): End hour of the schedule.
        ahu_value (int): Value to set in the schedule (Cold air:-1 / Hot air:1 / No air:0).
    """
    # Establish a connection to the database
    conn = sqlite3.connect('Fivos_Data.db')

    # Insert the values (Date, Time, Value) in the table at a specific time
    for hour in range(start_hour, end_hour):
        for minute in range(0, 60, 30):
            ahu_time = f"{hour:02d}:{minute:02d}"
            conn.cursor().execute("INSERT OR IGNORE INTO AHU_SCHEDULE VALUES (?, ?, ?)",
                                  (date, ahu_time, ahu_value))
            conn.commit()
    conn.close()


def ahu_schedule_overwrite(date, start_hour, end_hour, ahu_value):
    """
    Update existing AHU schedule entries in the database.

    Parameters:
        date (str): Date for which the schedule is applied.
        start_hour (int): Start hour of the schedule.
        end_hour (int): End hour of the schedule.
        ahu_value (int): Value to set in the schedule (Cold air:-1 / Hot air:1 / No air:0).
    """
    # Establish a connection to the database
    conn = sqlite3.connect('Fivos_Data.db')

    # Update existing entries from the AHU_SCHEDULE SQL Table, for the given date and time
    for hour in range(start_hour, end_hour):
        for minute in range(0, 60, 30):
            ahu_time = f"{hour:02d}:{minute:02d}"
            conn.cursor().execute("UPDATE AHU_SCHEDULE SET VALUE = ? WHERE DATE = ? AND TIME = ?",
                                  (ahu_value, date, ahu_time))
            conn.commit()
    conn.close()
