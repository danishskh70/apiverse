import httpx

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 10.0

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


async def get_current_weather(
    latitude: float,
    longitude: float,
) -> dict:
    """Fetch and normalize current weather data from Open-Meteo."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "auto",
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,is_day,precipitation,"
            "weather_code,wind_speed_10m"
        ),
    }

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

    if not isinstance(data, dict) or not isinstance(data.get("current"), dict):
        raise TypeError("Invalid weather data received from Open-Meteo.")

    current = data["current"]
    weather_code = current.get("weather_code")

    if not isinstance(weather_code, int):
        raise TypeError("Invalid weather code received from Open-Meteo.")

    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timezone": data.get("timezone"),
        "current": current,
        "condition": WEATHER_CODES.get(
            weather_code,
            "Unknown weather condition",
        ),
    }
