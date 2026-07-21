from src.api_client import WeatherAPIClient
from src.processor import SolarDataProcessor
from src.database import DatabaseManager

BERLIN_LAT = 52.5200
BERLIN_LON = 13.4050

def main():
    print("--- Solar Radiation & Weather Data Pipeline ---")
    
    # 1. Fetch Data
    client = WeatherAPIClient()
    print(f"Fetching data for Berlin (Lat: {BERLIN_LAT}, Lon: {BERLIN_LON})...")
    raw_data = client.fetch_solar_data(latitude=BERLIN_LAT, longitude=BERLIN_LON)
    
    if not raw_data:
        print("[ABORT] Could not retrieve data.")
        return

    # 2. Process Data
    processor = SolarDataProcessor()
    df = processor.process_raw_response(raw_data)
    
    if df is not None:
        summary = processor.calculate_daily_summary(df)
        print("\nDaily Solar Summary:")
        print(summary)
        
        # 3. Save to Database
        db = DatabaseManager()
        db.save_summary(summary)
        
        # 4. Verify by loading back from DB
        loaded_data = db.load_summary()
        print("\nVerification - Data loaded back from SQLite DB:")
        print(loaded_data)
        
    else:
        print("[ABORT] Processing failed.")

if __name__ == "__main__":
    main()