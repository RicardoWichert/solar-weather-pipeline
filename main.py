import os
import argparse
from dotenv import load_dotenv
from src.api_client import WeatherAPIClient
from src.processor import SolarDataProcessor
from src.database import DatabaseManager
from src.visualizer import generate_solar_chart

def main():
    load_dotenv()
    default_lat = float(os.getenv("DEFAULT_LAT", 52.52))
    default_lon = float(os.getenv("DEFAULT_LON", 13.41))
    # CLI Argument Parsing
    parser = argparse.ArgumentParser(description="Solar & Weather Data ETL Pipeline")
    parser.add_argument("--lat", type=float, default=default_lat, help=f"Latitude (default: {default_lat})")
    parser.add_argument("--lon", type=float, default=default_lon, help=f"Longitude (default: {default_lon})")
    parser.add_argument("--days", type=int, default=7, help="Number of past days to fetch (default: 7)")
    args = parser.parse_args()

    print(f"[INFO] Running pipeline for Lat: {args.lat}, Lon: {args.lon} over {args.days} days...")

    # 1. Fetch Data
    try:
        client = WeatherAPIClient(timeout=10)
        raw_data = client.fetch_solar_data(latitude=args.lat, 
                                           longitude=args.lon, 
                                           past_days=args.days)
    except Exception as e:
        print(f"[ERROR] Network or API connection failed: {e}")
        return

    if not raw_data:
        print("[ERROR] Failed to fetch data. Exiting pipeline.")
        return

    # 2. Process Data
    try:
        df_raw = SolarDataProcessor.process_raw_response(raw_data)
    except Exception as e:
        print(f"[ERROR] Failed to process raw response data: {e}")
        return

    if df_raw is None or df_raw.empty:
        print("[ERROR] Could not process raw response.")
        return
    
    summary_df = SolarDataProcessor.calculate_daily_summary(df_raw)

    print("\n--- Processed Summary Data ---")
    print(summary_df.to_string(index=False))

    # 3. Store Data
    try:
        db = DatabaseManager("solar_data.sqlite")
        db.save_summary(summary_df)
    except Exception as e:
        print(f"[ERROR] Failed to save data to the database: {e}")
        return
    
    # 4. Generate Visualization
    try:
        generate_solar_chart(summary_df)
    except Exception as e:
        print(f"[WARNING] Could not generate visualization chart: {e}")

if __name__ == "__main__":
    main()