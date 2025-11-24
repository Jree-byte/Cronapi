#!/usr/bin/env python3
import os
from datetime import datetime
import requests
import mysql.connector
from dotenv import load_dotenv

# --- Lataa .env ---
load_dotenv()

# --- Hae asetukset ---
API_KEY = os.getenv('WEATHER_API_KEY')
CITY = 'Helsinki'
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# --- OpenWeatherMap API ---
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

# --- MySQL-yhteys ---
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()

# --- Luo taulu jos ei ole ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    description VARCHAR(100),
    timestamp DATETIME
)
''')

# --- Hae säätiedot ja lisää tietokantaan ---
response = requests.get(URL)
data = response.json()

temp = data['main']['temp']
desc = data['weather'][0]['description']
timestamp = datetime.now()

cursor.execute('''
INSERT INTO weather_data (city, temperature, description, timestamp)
VALUES (%s, %s, %s, %s)
''', (CITY, temp, desc, timestamp))

conn.commit()
cursor.close()
conn.close()

print(f"Weather data tallennettu: {CITY} {temp}°C {desc}")
