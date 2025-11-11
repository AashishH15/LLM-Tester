import os
import requests
from flask import jsonify, request, Flask, render_template_string

app = Flask(__name__)

def fetch_weather_data(lat, lng):
    """
    Fetches weather data for given coordinates using OpenWeatherAPI

    Args:
        lat (float): Latitude of the location
        lng (float): Longitude of the location

    Returns:
        dict: Weather data including temperature, humidity, wind speed and condition
              or error message if something goes wrong
    """
    api_key = os.getenv('OPENWEATHER_API_KEY')

    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather'
            f'?lat={lat}'
            f'&lon={lng}'
            f'&units=metric'
            f'&appid={api_key}')
        weather_data = response.json()

        # Extract relevant data
        temp = round(weather_data['main']['temp'], 1)
        humidity = int(weather_data['main']['humidity'])
        wind_speed = round(weather_data['wind']['speed'], 1)
        weather_condition = weather_data['weather'][0]['description'].capitalize()

        return {
            'temperature': temp,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'weather_condition': weather_condition
        }

    except requests.exceptions.RequestException as e:
        return {
            'error': f'Failed to fetch weather data: {str(e)}'
        }

@app.route('/', methods=['GET'])
def landing_page():
    """
    Route to handle GET request for the landing page
    """
    return render_template_string('<h1>Landing Page</h1>')

@app.route('/weather', methods=['POST'])
def get_weather():
    """
    Route to handle POST request for coordinates and calculate severity
    """
    try:
        data = request.get_json()
        lat = data.get('latitude')
        lng = data.get('longitude')

        if not lat or not lng:
            return jsonify({'error': 'Latitude and Longitude are required'}), 400

        weather_data = fetch_weather_data(lat, lng)
        return jsonify(weather_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)