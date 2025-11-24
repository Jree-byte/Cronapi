#!/usr/bin/env python3
import os
from datetime import datetime
import requests
import mysql.connector
from dotenv import load_dotenv

# --- Lataa .env ---
load_dotenv()

# --- Hae asetukset ---
API_KEY = os.getenv('AVIATION_API_KEY')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# --- API URL  ---
API_URL = f'https://api.aviationstack.com/v1/flights?access_key=84924720cd2c1a5f0af672c807851d2a'

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
CREATE TABLE IF NOT EXISTS aviation_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight VARCHAR(20),
    status VARCHAR(20),
    departure DATETIME,
    arrival DATETIME,
    timestamp DATETIME
)
''')

# --- Hae data API:sta ---
response = requests.get(API_URL)
data = response.json()

count = 0
for flight in data.get('data', []):
    flight_number = flight['flight'].get('iata') if flight.get('flight') else 'Unknown'
    status = flight.get('flight_status', 'Unknown')

    departure_time = flight['departure'].get('scheduled') if flight.get('departure') else None
    arrival_time = flight['arrival'].get('scheduled') if flight.get('arrival') else None

    cursor.execute('''
        INSERT INTO aviation_data (flight, status, departure, arrival, timestamp)
        VALUES (%s, %s, %s, %s, %s)
    ''', (flight_number, status, departure_time, arrival_time, datetime.now()))
    count += 1

conn.commit()
cursor.close()
conn.close()

print(f"Aviation data tallennettu: {count} lentoa")
