import argparse
from src.api_client import WeatherAPIClient
from src.processor import SolarDataProcessor
from src.database import DatabaseManager
from src.visualizer import generate_solar_chart

def main():
    # CLI Argument Parsing
    parser = argparse.ArgumentParser(description="Solar & Weather Data ETL Pipeline")
    parser.add_argument("--lat", type=float, default=52.52, help="Latitude (default: 52.52 for Berlin)")
    parser.add_argument("--lon", type=float, default=13.41, help="Longitude (default: 13.41 for Berlin)")
    parser.add_argument("--days", type=int, default=7, help="Number of past days to fetch (default: 7)")
    args = parser.parse_args()

    print(f"[INFO] Running pipeline for Lat: {args.lat}, Lon: {args.lon} over {args.days} days...")

    # 1. Fetch Data
    client = WeatherAPIClient(timeout=10)
    raw_data = client.fetch_solar_data(latitude=args.lat, 
                                       longitude=args.lon, 
                                       past_days=args.days)

    if not raw_data:
        print("[ERROR] Failed to fetch data. Exiting pipeline.")
        return

    # 2. Process Data
    df_raw = SolarDataProcessor.process_raw_response(raw_data)

    if df_raw is None or df_raw.empty:
        print("[ERROR] Could not process raw response.")
        return
    
    summary_df = SolarDataProcessor.calculate_daily_summary(df_raw)

    print("\n--- Processed Summary Data ---")
    print(summary_df.to_string(index=False))

    # 3. Store Data
    db = DatabaseManager("solar_data.sqlite")
    db.save_summary(summary_df)

    # 4. Generate Visualization
    generate_solar_chart(summary_df)

if __name__ == "__main__":
    main()