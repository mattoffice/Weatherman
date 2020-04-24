from flask import Flask, jsonify, render_template
from tronald import tronald_dumps
import flight_service
import weather_service

app = Flask(__name__)
target_port = 3000

fs = flight_service.Flight_Service('Madrid', '2020-08-01')
res = fs.call_amadeus()
ws = weather_service.Weather_Service('Madrid')
w_data = ws.call_weather_api()
print(res)


@app.route('/', methods=['GET'])
def home_s():
    return render_template('home.html', random_var="Sick weather", random_list=[1, 2, 3, 4, 5, 6])


@app.route('/flights', methods=['GET'])
def serve_something():
    return render_template('flights.html', flight_data=fs.data, random_list=[4, 5, 6, 7, 8, 9])


@app.route('/weather', methods=['GET'])
def serve_weather():
    return render_template('weather.html', weather_data=w_data)


if __name__ == '__main__':
    app.run(host="localhost", port=target_port)
