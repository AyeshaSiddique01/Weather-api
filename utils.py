"""Helper functions for application"""
from enum import Enum


class WeatherAttribute(Enum):
    """Enum for Weather Attribute"""

    DATE = "PKT"
    MAX_TEMP = "Max TemperatureC"
    MIN_TEMP = "Min TemperatureC"
    MAX_HUMIDITY = "Max Humidity"
    MEAN_HUMIDITY = "Mean Humidity"
    MIN_HUMIDITY = "Min Humidity"
