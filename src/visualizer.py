import matplotlib.pyplot as plt
import pandas as pd

def generate_solar_chart(df: pd.DataFrame, output_path: str = "solar_summary.png"):
    """
    Generates and saves a summary chart comparing GHI radiation and temperature.
    """
    if df.empty:
        print("[WARNING] DataFrame is empty. Skipping plot generation.")
        return
    
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Primary axis: Solar Radiation
    color = 'tab:green'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Avg Direct Irradiance (W/m²)', color=color)
    ax1.plot(df['date'], df['avg_direct_irradiance'], color=color, marker='o', linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45)

    # Secondary axis: Temperature
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Avg Temperature (°C)', color=color)
    ax2.plot(df['date'], df['avg_temperature'], color=color, marker='s', linestyle='--', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Solar Irradiance & Temperature Summary')
    fig.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[SUCCESS] Chart saved to {output_path}")