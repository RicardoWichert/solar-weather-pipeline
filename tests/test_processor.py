import pandas as pd
from src.processor import SolarDataProcessor

def test_process_raw_response():
    # Simulated API Response
    mock_raw_data = {
        "hourly": {
            "time": ["2026-07-21T00:00", "2026-07-21T01:00"],
            "direct_normal_irradiance": [0.0, 100.0],
            "global_tilted_irradiance": [0.0, 80.0],
            "temperature_2m": [15.0, 16.0]
        }
    }
    
    df = SolarDataProcessor.process_raw_response(mock_raw_data)
    
    assert df is not None
    assert len(df) == 2
    assert "direct_irradiance" in df.columns
    assert df["direct_irradiance"].iloc[1] == 100.0

def test_calculate_daily_summary():
    # Sample DataFrame
    mock_df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2026-07-21 10:00", "2026-07-21 12:00"]),
        "direct_irradiance": [200.0, 400.0],
        "global_irradiance": [150.0, 300.0],
        "temperature": [20.0, 22.0]
    })
    
    summary = SolarDataProcessor.calculate_daily_summary(mock_df)
    
    assert len(summary) == 1
    assert summary["avg_direct_irradiance"].iloc[0] == 300.0
    assert summary["max_direct_irradiance"].iloc[0] == 400.0