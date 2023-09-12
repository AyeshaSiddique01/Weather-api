""" Data Manipulator for weatherman application """
import glob
from csv import DictReader
from datetime import datetime

from models import WeatherModel
from utils import WeatherAttribute


class FileHandling:
    """Fetch and manipulate data of the weather files"""

    def __init__(self, directory_path):
        """
        Get file directory and read data of all files

        Args:
            directory_path: directory of files

        Returns:
            list of data of all files
        """
        files = glob.glob(f"{directory_path}/*.txt", recursive=True)
        weather_record = []

        for file in files:
            weather_record += self.get_weather_record(file)

        self.weather_record = weather_record

    def get_weather_record(self, file_name):
        """
        Get file name and read data of it

        Args:
            file_name: Name of file

        Returns:
            list of weather of all days of month
        """
        with open(file_name, "r", encoding="utf-8") as file:
            file_reader = DictReader(file, skipinitialspace=True)
            return [self.create_weather_obj(rc) for rc in file_reader if self.is_valid_record(rc)]

    def is_valid_record(self, record):
        """
        Validate is record is valid or not

        Args:
            record: data to validate

        Returns:
            Boolean if data is valid returns ture else false
        """
        if (
            (record.get(WeatherAttribute.DATE.value) or record["PKST"])
            and record.get(WeatherAttribute.MAX_TEMP.value)
            and record.get(WeatherAttribute.MIN_TEMP.value)
            and record.get(WeatherAttribute.MAX_HUMIDITY.value)
            and record.get(WeatherAttribute.MEAN_HUMIDITY.value)
            and record.get(WeatherAttribute.MIN_HUMIDITY.value)
        ):
            return True

        return False

    def create_weather_obj(self, record):
        """
        Creates object of weather of corresponding record

        Args:
            record: dictionary object to create object

        Returns:
            WeatherModel object of that record
        """
        date = record.get(WeatherAttribute.DATE.value) or record["PKST"]
        return WeatherModel(
            date=datetime.strptime(date, "%Y-%m-%d"),
            max_temperature_celcius=int(record[WeatherAttribute.MAX_TEMP.value]),
            min_temperature_celcius=int(record[WeatherAttribute.MIN_TEMP.value]),
            max_humidity=int(record[WeatherAttribute.MAX_HUMIDITY.value]),
            mean_humidity=int(record[WeatherAttribute.MEAN_HUMIDITY.value]),
            min_humidity=int(record[WeatherAttribute.MIN_HUMIDITY.value]),
        )
