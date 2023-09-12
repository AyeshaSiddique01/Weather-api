""" Sever of application"""
from flask import Flask, jsonify, request
from flask_migrate import Migrate

from file_handling import FileHandling
from models import db

app = Flask(__name__)
app.config.from_object("config")
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{app.config['USER']}:{app.config['PASSWORD']}@{app.config['HOST']}:{app.config['PORT']}/{app.config['DATABASE']}"

db.init_app(app)
migrate = Migrate(app, db)

from models import WeatherModel


@app.route("/", methods=["POST"])
def populate_record():
    """Populate weather records in the databse"""
    if request.method == "POST":
        if not WeatherModel.is_record_exists():
            directory_path = request.args.get("directory_path")
            file_handling = FileHandling(directory_path)
            records = file_handling.weather_record

            add_weather_response = [WeatherModel.add_weather(rc) for rc in records]

            if any(res for res in add_weather_response if res[1] != 200):
                return jsonify("Invalid data")
            else:
                return jsonify("Data uploded")
        else:
            return jsonify("Data already exists")


@app.route("/get_weather", methods=["GET"])
def get_weather():
    """Get weathers in a specific interval"""
    if request.method == "GET":
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        weathers = WeatherModel.get_weather(start_date=start_date, end_date=end_date)

        return [weather.to_dict() for weather in weathers], 200

    return jsonify("Invalid request method"), 405


@app.route("/add_weather", methods=["POST"])
def add_weather():
    """Add a new weather record"""
    if request.method == "POST":
        if request.is_json:
            try:
                data = request.get_json()
                weather = WeatherModel(**data)
                return WeatherModel.add_weather(weather)
            except KeyError as key_error:
                return (f"Missing field in JSON data: {str(key_error)}", 400)
        else:
            return jsonify("Invalid Content-Type. Use application/json"), 400

    return jsonify("Invalid request method"), 405


@app.route("/update", methods=["PUT"])
def update():
    """Update weather of the specific day"""
    if request.method == "PUT":
        weather_id = request.args.get("id")
        old_weather = WeatherModel.get_by_id(weather_id)

        new_weather = request.get_json()

        old_weather.date = new_weather["date"]
        old_weather.max_temperature_celcius = new_weather["max_temperature_celcius"]
        old_weather.min_temperature_celcius = new_weather["min_temperature_celcius"]
        old_weather.max_humidity = new_weather["max_humidity"]
        old_weather.mean_humidity = new_weather["mean_humidity"]
        old_weather.min_humidity = new_weather["min_humidity"]

        response = WeatherModel.add_weather(old_weather)
        if response[1] == 200:
            return jsonify("weather updated!")

        return response

    return jsonify("Invalid request method"), 405


@app.route("/delete", methods=["delete"])
def delete():
    """Delete weather of a specific day"""
    if request.method == "DELETE":
        weather_id = request.args.get("id")

        return WeatherModel.delete(weather_id)

    return jsonify("Invalid request method"), 405


# Running app
if __name__ == "__main__":
    app.run(debug=True)
