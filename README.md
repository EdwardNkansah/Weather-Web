### Weather-Web Application
The main objective of this project was to create a flask App. I chose to develop a weather website to provide 
individuals with historical weather data according to the country and location.

Step 1) To help create the database driven web application. I obtained the data from an open source at https://www.kaggle.com/datasets. I then unpacked the zip folder to access the csv file.
This process helped me to practices data import which will aid in building my application. 

### Table Relationship for the Data
We will import our table listed weather-datasets.csv.
We decided to clean our data to suit our perfection which will be useful for our application. The parse_weather_app.py file is responsible to generate the table
which can be readable by the sql.   

Step 2) We began creating the software that will display the imported data. Create a new folder called "Weather-Web".
After we use the terminal to cd into the folder and run the following commands:

  pyenv local 3.7.9 # this sets the local version of python to 3.7.9
  python3 -m venv .venv # this creates the virtual environment for you
  source .venv/bin/activate # this activates the virtual environment
  pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
  
  We will use Flask (https://flask.palletsprojects.com/en/1.1.x/) as our web framework for the application. We install that with

  pip install flask

### We need to parse a csv file and the data to a database
We must enter the spreadsheet data into a database to store the weather_app information on the website, which was our main motive.
There are series of method to do that, but we will choose the simplest method. 

Since reading a csv file is straight forward, lets start there. Insert this code in the weather.csv.py file. This implies that you have placed 
the entire weather data directory (folder) in the application folder. This is opened, and reader is created that iterates through each row before printing it on the screen.
Since we are unsure of the expected line ending, the newline=" flag is the default.

Between the line that reads "import csv" and the line that opens the csv file, insert this code. 



  import csv
  import sqlite3
  # from flask import Flask, render_template

  # def populate_database():
  conn = sqlite3.connect('weather.db')
  cursor = conn.cursor()

  conn.execute('DROP TABLE IF EXISTS country')
  conn.execute('DROP TABLE IF EXISTS weather')

  # Create table
  cursor.execute('''CREATE TABLE IF NOT EXISTS country (
                    id INTEGER,
                    country TEXT,
                    location_name TEXT
                )''')
  print("table created successfully")

  cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER,
                    latitude REAL,
                    longitude REAL,
                    timezone TEXT,
                    last_updated_epoch INTEGER,
                    last_updated TEXT,
                    temperature_celsius REAL,
                    temperature_fahrenheit REAL,
                    condition_text TEXT,
                    humidity INTEGER,
                    cloud INTEGER,
                    sunrise TEXT,
                    sunset TEXT,
                    moonrise TEXT,
                    moonset TEXT
                )''')
 print("table created successfully")

Put this code after the lines that parse the csv file. Keeep in mind that (a) when the query has been created, we must "commit()" it
and (b) at the very end, we must also shut the database connection. We define the values we want to store. 

  with open('Weather-Web/weather_records/weather-dataset.csv', 'r') as file:
  csv_data = csv.reader(file)
  headers = next(csv_data)  # Skip the header row


  # Insert data into table
  count = 0
  for row in csv_data:
      print(row)
      con = row[0]
      loc = row[1]

      cursor.execute('INSERT INTO country VALUES (?, ?, ?)', (count,con,loc))
      count = count + 1

  with open('Weather-Web/weather_records/weather-dataset.csv', 'r') as file:
  csv_data = csv.reader(file)
  headers = next(csv_data)  # Skip the header row


  # Insert data into table
  count = 0
  for row in csv_data:
      print(row)
      array = row[2:]
      array.insert(0,count)

      cursor.execute('INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', array)      
      count = count + 1
conn.commit()
conn.close()


Now that the data is in the database we can build the web front end to see the data.

### Building the web components
We can now start the actual file app after a successful database connection.
  

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
        try:
        #query = "SELECT * FROM country"
          query = "SELECT id FROM country WHERE country=? AND location_name=?"
          cursor.execute(query, (country, location_name))
          #cursor.execute(query)
          id = cursor.fetchone()
          print(id)
          query = "SELECT * FROM weather WHERE id=?"
          cursor.execute(query, (id))
          result = cursor.fetchone()
          print(result)

          conn.close()

          if result is None:
              return render_template('index.html', error='No matching weather data found')

          columns = ['id', 'Latitude', 'Longitude', 'Timezone', 'Last Updated Epoch',
                    'Last Updated', 'Temperature (Celsius)', 'Temperature (Fahrenheit)', 'Condition Text',
                    'Humidity', 'Cloud', 'Sunrise', 'Sunset', 'Moonrise', 'Moonset']
        except: 
          return render_template('Results.html', error='No matching weather data found')

        weather_data = dict(zip(columns, result))

        return render_template('Results.html', country=country, weather_data=weather_data)

  return render_template('index.html')

@app.route('/aboutUs.html', methods=['GET'])
def aboutUs():
  return render_template('aboutUs.html')


@app.route('/Results.html', methods=['GET'])
def Results():
  return render_template('Results.html')

if __name__ == '__main__':
  app.run()

In order to view the query data by a user, we now create the html page.
we store all our html and CSS pages in the template folder. 

###Index.html
  <!DOCTYPE html>
  <html>
  <head>
    <title>Weather App</title>
    <style>
        body {
            background-image: url("https://i.postimg.cc/fTLg9RcY/temp-Image-Zo-M1-KN.avif");
            background-size: cover;
            background-repeat: no-repeat;
            font-family: Arial, sans-serif;
        }        
        nav {
            background-color: #333;
            overflow: hidden;
            padding: 20px;
        }        
        nav ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            text-align: center; /* Center the links horizontally */
        }        
        nav ul li {
            display: inline;
            margin-right: 10px;
        }        
        nav ul li a {
            text-decoration: none;
            color: white;
        }
        
        form input[type="text"] {
    width: 300px;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    outline: none;
  }

  form input[type="submit"] {
    padding: 10px 20px;
    background-color: #4CAF50;
    border: none;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  form input[type="submit"]:hover {
    background-color: #45a049;
  }
        form {
            text-align: center; /* Center the form elements horizontally */
            margin-top: 20px; /* Add some spacing between the navbar and forms */
        }
        
        form label {
            display: block;
            margin-bottom: 5px;
        }
        
        form input[type="text"] {
            width: 200px;
            padding: 5px;
        }
        
        form input[type="submit"] {
            padding: 5px 10px;
            background-color: #4CAF50;
            border: none;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        form input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
  </head>
  <body>
    <h1>Historical Weather App</h1>
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="aboutUs.html">About Us</a></li>
        </ul>
    </nav>

    <br> <!-- Add a break between the navbar and forms -->
    <h4>Find historical weather by searching for a Country and Location.</h4>

    {% if error %}
    <p>{{ error }}</p>
    {% endif %}

    <form method="POST" action="/">
        <label for="country">Country:</label>
        <input type="text" id="country" name="country" required>
        
        <label for="location_name">Location Name:</label>
        <input type="text" id="location_name" name="location_name" required>
        
        <br> <!-- Add a line break between the input fields and submit button -->
        
        <br><input type="submit" value="Search"></br>
    </form>
  </body>
  </html>

###Results.html
<!DOCTYPE html>
<html>
<head>
    <title>Weather App - Results</title>
    <style>
        body {
            background-image: url("https://i.postimg.cc/fTLg9RcY/temp-Image-Zo-M1-KN.avif");
            background-size: cover;
            background-repeat: no-repeat;
            font-family: Arial, sans-serif;
        }
        
        nav {
            background-color: #333;
            overflow: hidden;
            padding: 20px;
        }
        
        nav ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            text-align: center; /* Center the links horizontally */
        }
        
        nav ul li {
            display: inline;
            margin-right: 10px;
        }
        
        nav ul li a {
            text-decoration: none;
            color: white;
        }
        
        h1 {
            color: #333;
            text-align: center;
            margin-top: 50px;
        }
        
        table {
            margin: 0 auto;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        
        th, td {
            padding: 10px;
            text-align: left;
        }
        
        th {
            background-color: #333;
            color: white;
        }
        
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        tr:hover {
            background-color: #ddd;
        }
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="aboutUs.html">About Us</a></li>
        </ul>
    </nav>

    <h1>Weather Data Results</h1>

    {% if weather_data %}
    <table>
        <thead>
            <tr><th colspan="2">{{country}}</th></tr>
            <tr>
                <th>Attribute</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
            {% for key, value in weather_data.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ value }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No weather data found.</p>
    {% endif %}
</body>
</html>

 Now the main objective of developing our weather_app using flask is achieved

 Below is the render deployment url
