import requests
from typing import Dict, Any, Optional

class WeatherAPIClient:
    """Client to fetch weather and solar radiation data from Open-Meteo API."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch_solar_data(self, latitude: float, longitude: float, past_days: int = 7) -> Optional[Dict[str, Any]]:
        """
        Fetches hourly direct normal irradiance (DNI) and global horizontal irradiance (GHI).
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "past_days": past_days,
            "hourly": "direct_normal_irradiance,global_tilted_irradiance,temperature_2m",
            "timezone": "auto"
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            response.raise_for_status()  # Raises HTTPError for 4xx or 5xx status codes
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch data from API: {e}")
            return None