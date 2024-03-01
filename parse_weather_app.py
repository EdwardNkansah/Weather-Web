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