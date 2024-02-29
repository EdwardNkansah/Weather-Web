

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = 'weather.db'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form.get('country')
        location_name = request.form.get('location_name')

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        query = "SELECT * FROM weather WHERE country=? AND location_name=?"
        cursor.execute(query, (country, location_name))
        result = cursor.fetchone()

        conn.close()

        if result is None:
            return render_template('index.html', error='No matching weather data found')

        columns = ['Country', 'Location Name', 'Latitude', 'Longitude', 'Timezone', 'Last Updated Epoch',
                   'Last Updated', 'Temperature (Celsius)', 'Temperature (Fahrenheit)', 'Condition Text',
                   'Humidity', 'Cloud', 'Sunrise', 'Sunset', 'Moonrise', 'Moonset']

        weather_data = dict(zip(columns, result))

        return render_template('index.html', weather_data=weather_data)

    return render_template('index.html')

@app.route('/aboutUs.html', methods=['GET'])
def aboutUs():
  return render_template('aboutUs.html')


@app.route('/weatherNews.html', methods=['GET'])
def weatherNews():
  return render_template('weatherNews.html')

if __name__ == '__main__':
    app.run()