from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy(session_options={"autoflush": False})


class WeatherModel(db.Model):
    """Weather model"""

    __tablename__ = "weather"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, unique=True)
    max_temperature_celcius = db.Column(db.Integer)
    min_temperature_celcius = db.Column(db.Integer)
    min_temperature_celcius = db.Column(db.Integer)
    max_humidity = db.Column(db.Integer)
    mean_humidity = db.Column(db.Integer)
    min_humidity = db.Column(db.Integer)

    def __repr__(self):
        return f"<Weather {self.date}>"

    def to_dict(self):
        """Convert WeatherModel object to a dictionary"""
        return {
            "id": self.id,
            "date": self.date,
            "max_temperature_celcius": self.max_temperature_celcius,
            "min_temperature_celcius": self.min_temperature_celcius,
            "max_humidity": self.max_humidity,
            "mean_humidity": self.mean_humidity,
            "min_humidity": self.min_humidity,
        }

    @classmethod
    def add_weather(cls, weather):
        """
        Add new record to database

        Args:
            weather: object to add

        Returns:
            tuple: with return message and status
        """
        try:
            db.session.add(weather)
            db.session.commit()
            return ("Weather added successfully", 200)
        except IntegrityError:
            db.session.rollback()
            return ("Record for that date already exists", 409)
        except Exception as exception:
            db.session.rollback()
            return (f"An error occurred: {str(exception)}", 500)
        finally:
            db.session.close()

    @classmethod
    def get_weather(cls, start_date, end_date):
        """
        Get Record of a interval

        Args:
            start_date: from date record will get
            end_date: to date record will get

        Returns:
            record: list of weather
        """
        return cls.query.filter(cls.date >= start_date, cls.date <= end_date).all()

    @classmethod
    def delete(cls, weather_id):
        """
        Delete record of a day

        Args:
            weather_id: id of the weather to delete record
        """
        weather = cls.query.get(weather_id)

        if weather:
            db.session.delete(weather)
            db.session.commit()
            return "Weather deleted!", 200

        return "Weather not found", 404

    @classmethod
    def get_by_id(cls, weather_id):
        """
        Get Record of a day

        Args:
            id: id to get record

        Returns:
            record: Weather object
        """
        weather = cls.query.get(weather_id)

        if weather:
            return weather
        return "Weather not found"

    @classmethod
    def is_record_exists(cls):
        """
        Check is record is present in the database or not
        Returns:
            boolean: return True of records exist
        """
        if len(cls.query.all()) > 0:
            return True

        return False
