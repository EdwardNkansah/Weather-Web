import csv
import sqlite3
# from flask import Flask, render_template

# def populate_database():
conn = sqlite3.connect('weather.db')
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                    country TEXT,
                    location_name TEXT,
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
    
with open('weather_records/weather-dataset.csv', 'r') as file:
    csv_data = csv.reader(file)
    headers = next(csv_data)  # Skip the header row


  # Insert data into table
    for row in csv_data:
      print(row)
      cursor.execute('INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)

conn.commit()
conn.close()