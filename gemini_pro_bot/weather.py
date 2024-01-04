import requests
import os
def print_weather_data(api_key, location):
    base_url = "http://api.weatherstack.com/forecast"
    params = {"access_key": api_key, "query": location}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract relevant weather information
            weather_info = data.get("current", {})
            location_info = data.get("location", {})
            temperature = weather_info.get("temperature")
            description = weather_info.get("weather_descriptions", [])[0]
            humidity = weather_info.get("humidity")
            localtime = location_info.get("localtime")
            country = location_info.get("country")

            # Extract forecast information
            forecast_info = data.get("forecast", {})
            forecast_str = ""
            if forecast_info:
                forecast_date = list(forecast_info.keys())[0]
                forecast_temp_min = forecast_info[forecast_date].get("mintemp")
                forecast_temp_max = forecast_info[forecast_date].get("maxtemp")
                forecast_avg_temp = forecast_info[forecast_date].get("avgtemp")

                forecast_str = f"\nForecast for {forecast_date}: Min Temp {forecast_temp_min}°C, Max Temp {forecast_temp_max}°C, Avg Temp {forecast_avg_temp}°C"

            # Build and return the weather report
            report = (
                f"Weather Report for {location}, {country}\n"
                f"Temperature: {temperature}°C\n"
                f"Condition: {description}\n"
                f"Humidity: {humidity}%\n"
                f"Observed at: {localtime}{forecast_str}"
            )
            print(report)
            return report

        else:
            return f"Error: {response.status_code}, {data.get('error', {}).get('info', 'Unknown error')}"

    except Exception as e:
        return f"An error occurred: {e}"
