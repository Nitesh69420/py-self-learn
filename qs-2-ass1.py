"""
Assignment 1 - Question 2: Automated Weather Data Fetcher & JSON Parser
Subject: Python Laboratory (DJS23APC203L)
Description: Retrieves live weather data from Open-Meteo REST API, extracts metrics,
             and logs them to weather_report.txt with defensive exception handling.
"""

import sys
from datetime import datetime
import requests


# WMO Weather interpretation codes dictionary for human-readable output
WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm"
}


def fetch_weather_data(latitude: float, longitude: float) -> dict:
    """
    Sends an HTTP GET request to Open-Meteo public API with defensive exception handling.
    """
    endpoint = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "timezone": "auto"
    }

    try:
        print(f"[*] Sending HTTP GET request to {endpoint}...")
        response = requests.get(endpoint, params=params, timeout=10)
        
        # Raise HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        
        print(f"[+] HTTP Status Code: {response.status_code} OK")
        return response.json()

    except requests.exceptions.Timeout:
        print("[-] Error: Connection timed out while trying to reach the server.")
        sys.exit(1)
    except requests.exceptions.HTTPError as http_err:
        print(f"[-] HTTP Error encountered: {http_err}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("[-] Network Error: Unable to establish connection. Check your internet connectivity.")
        sys.exit(1)
    except requests.exceptions.RequestException as req_err:
        print(f"[-] An unexpected network error occurred: {req_err}")
        sys.exit(1)


def parse_and_save_weather(data: dict, filename: str = "weather_report.txt") -> str:
    """
    Parses required metrics from JSON response, formats a summary report,
    and persists it to the specified local text file.
    """
    try:
        current = data["current_weather"]
        temperature = current["temperature"]
        windspeed = current["windspeed"]
        weathercode = current["weathercode"]
        timezone = data.get("timezone", "UTC")
        weather_description = WMO_WEATHER_CODES.get(weathercode, "Unknown Weather Condition")
        observation_time = current.get("time", datetime.now().isoformat())

        # Format Human-Readable Report
        report_content = (
            "====================================================\n"
            "         AUTOMATED REAL-TIME WEATHER REPORT         \n"
            "====================================================\n"
            f"Timestamp of Query    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Observation Time      : {observation_time}\n"
            f"Timezone              : {timezone}\n"
            f"Latitude / Longitude  : {data.get('latitude')}°N, {data.get('longitude')}°E\n"
            "----------------------------------------------------\n"
            f"Temperature           : {temperature} °C\n"
            f"Wind Speed            : {windspeed} km/h\n"
            f"Weather Code          : {weathercode} ({weather_description})\n"
            "====================================================\n"
        )

        # Write to local persistence file using context manager
        with open(filename, "w", encoding="utf-8") as report_file:
            report_file.write(report_content)

        return report_content

    except KeyError as key_err:
        print(f"[-] Parsing Error: Expected key {key_err} not found in the API response.")
        sys.exit(1)
    except IOError as io_err:
        print(f"[-] File I/O Error: Unable to write to {filename}: {io_err}")
        sys.exit(1)


def main():
    # Coordinates for Mumbai (College Location: 19.1075° N, 72.8372° E)
    mumbai_lat = 19.1075
    mumbai_lon = 72.8372

    print("=== Automated Weather Data Fetcher & JSON Parser ===")
    print(f"Target Location: Mumbai, Maharashtra (Lat: {mumbai_lat}, Lon: {mumbai_lon})\n")

    # Step 1 & 2: Fetch and defensively handle errors
    json_data = fetch_weather_data(latitude=mumbai_lat, longitude=mumbai_lon)

    # Step 3 & 4: Parse JSON, display summary, and write to weather_report.txt
    report_text = parse_and_save_weather(json_data, filename="weather_report.txt")

    print("\n--- Processed Weather Summary ---")
    print(report_text)
    print("[+] Successfully logged weather data to 'weather_report.txt'")


if __name__ == "__main__":
    main()