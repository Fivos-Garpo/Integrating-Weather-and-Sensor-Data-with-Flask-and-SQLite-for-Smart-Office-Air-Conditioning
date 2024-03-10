# my_module/__init__.py

# Importing modules to make them accessible when the package is imported
from . import sensor
from . import weather
from . import ahu_schedule
from . import database_utils
from . import datetime_utils
from . import file_utils
from . import weather_api
from . import yodiwo_api

# Defining variables or constants
VERSION = '1.0'

# Specifying explicitly exposed items
__all__ = ['sensor', 'weather', 'ahu_schedule', 'database_utils', 'datetime_utils', 'file_utils'
    ,'weather_api', 'yodiwo_api', 'VERSION']
