import pandas as pd
from typing import Dict, Any, Optional

class SolarDataProcessor:
    """Processes raw API weather data into structured metrics."""

    @staticmethod
    def process_raw_response(raw_data: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """Converts raw API json into a clean pandas DataFrame."""
        if not raw_data or "hourly" not in raw_data:
            return None

        hourly_data = raw_data["hourly"]
        
        df = pd.DataFrame({
            "timestamp": pd.to_datetime(hourly_data["time"]),
            "direct_irradiance": hourly_data["direct_normal_irradiance"],
            "global_irradiance": hourly_data["global_tilted_irradiance"],
            "temperature": hourly_data["temperature_2m"]
        })
        
        # Fill potential NaN values cleanly
        df.fillna(0, inplace=True)
        now = pd.Timestamp.now()
        df = df[df["timestamp"] <= now]
        return df

    @staticmethod
    def calculate_daily_summary(df: pd.DataFrame) -> pd.DataFrame:
        """Calculates daily average irradiance and peak values."""
        df['date'] = df['timestamp'].dt.date
        
        summary = df.groupby('date').agg(
            avg_direct_irradiance=('direct_irradiance', 'mean'),
            max_direct_irradiance=('direct_irradiance', 'max'),
            avg_temperature=('temperature', 'mean')
        ).reset_index()
        
        return summary