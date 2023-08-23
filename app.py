from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

def get_weather_data(date, lat, lon):
    url = "https://ai-weather-by-meteosource.p.rapidapi.com/time_machine"
    
    querystring = {
        "date": date,
        "lat": lat,
        "lon": lon,
        "units": "auto"
    }
    
    headers = {
        "X-RapidAPI-Key": "021dd48ab3mshbd1939d04b75e3ep1a040fjsna946f7eaa467",
        "X-RapidAPI-Host": "ai-weather-by-meteosource.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        lat = request.form['lat']
        lon = request.form['lon']
        
        weather_data = get_weather_data(date, lat, lon)
        
        formatted_data = []
        for entry in weather_data['data']:
            formatted_entry = {
                'date': entry['date'],
                'temperature': entry['temperature'],
                'climate': entry['weather']
            }
            formatted_data.append(formatted_entry)
        
        return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Weather Information</title>
                <style>
                    .weather-card {
                        border: 1px solid #ccc;
                        padding: 10px;
                        margin: 10px;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }
                </style>
            </head>
            <body>
                <h1>Weather Information</h1>
                <form method="post">
                    <label for="date">Date: </label>
                    <input type="date" name="date" required><br><br>
                    <label for="lat">Latitude: </label>
                    <input type="text" name="lat" required><br><br>
                    <label for="lon">Longitude: </label>
                    <input type="text" name="lon" required><br><br>
                    <input type="submit" value="Get Weather">
                </form>
                
                {% if weather_data %}
                    <h2>Weather Data:</h2>
                    {% for entry in formatted_data %}
                        <div class="weather-card">
                            <p><strong>Date:</strong> {{ entry['date'] }}</p>
                            <p><strong>Temperature:</strong> {{ entry['temperature'] }}</p>
                            <p><strong>Climate:</strong> {{ entry['climate'] }}</p>
                        </div>
                    {% endfor %}
                {% endif %}
            </body>
            </html>
        """, weather_data=weather_data, formatted_data=formatted_data)
    
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Weather Information</title>
        </head>
        <body>
            <h1>Weather Information</h1>
            <form method="post">
                <label for="date">Date: </label>
                <input type="date" name="date" required><br><br>
                <label for="lat">Latitude: </label>
                <input type="text" name="lat" required><br><br>
                <label for="lon">Longitude: </label>
                <input type="text" name="lon" required><br><br>
                <input type="submit" value="Get Weather">
            </form>
        </body>
        </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
