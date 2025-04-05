import os

import requests
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ВСТАВЬ В .env СВОЙ ТОКЕН
API_TOKEN = os.getenv('API_TOKEN')

# Координаты акватории Чёрного моря: north, south, west, east
BOUNDS = '46.5,40.5,27.0,41.5'

# URL API
FLIGHT_POSITIONS_URL = 'https://fr24api.flightradar24.com/api/live/flight-positions/full'
AIRLINES_URL = 'https://fr24api.flightradar24.com/api'

# Заголовки с токеном
headers = {
    'Accept': 'application/json',
    'Accept-Version': 'v1',
    'Authorization': f'Bearer {API_TOKEN}',
}

params = {
    'bounds': BOUNDS
}

def fetch_flights():
    """Получение списка рейсов над Чёрным морем."""
    response = requests.get(FLIGHT_POSITIONS_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json().get('data', [])
    return data

def fetch_airlines(icao_code):
    """Получение названия авиакомпании по ICAO-коду."""
    if not icao_code:
        return 'Unknown'
    try:
        url = f"{AIRLINES_URL}/static/airlines/{icao_code.lower()}/light"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get('name', 'Unknown')
    except Exception as e:
        print(f"⚠ Не удалось получить авиакомпанию для {icao_code}: {e}")
        return 'Unknown'

def save_to_csv(flights):
    """Сохранение рейсов в CSV-файл."""
    filename = f'flights_black_sea_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'callsign', 'icao_code', 'aircraft_model', 'airline_name',
            'origin', 'destination', 'lat', 'lon', 'altitude', 'gspeed', 'timestamp'
        ])

        for flight in flights:
            callsign = flight.get('callsign', '')
            icao_code = flight.get('painted_as', '')
            model = flight.get('type', '')
            lat = flight.get('lat', '')
            lon = flight.get('lon', '')
            alt = flight.get('alt', '')
            gspeed = flight.get('gspeed', '')
            timestamp = flight.get('timestamp', '')
            origin = flight.get('orig_icao', '')
            destination = flight.get('dest_icao', '')

            airline_name = fetch_airlines(icao_code)

            writer.writerow([
                callsign, icao_code, model, airline_name,
                origin, destination, lat, lon, alt, gspeed, timestamp
            ])

    print(f"✅ Данные сохранены в: {filename}")


def main():
    print("📡 Сбор данных...")
    flights = fetch_flights()
    save_to_csv(flights)


if __name__ == '__main__':
    main()