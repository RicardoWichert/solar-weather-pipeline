import sqlite3
import pandas as pd
from typing import Optional

class DatabaseManager:
    """Handles persistent storage of processed solar data using SQLite."""

    def __init__(self, db_path: str = "solar_data.sqlite"):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Returns a database connection."""
        return sqlite3.connect(self.db_path)

    def save_summary(self, summary_df: pd.DataFrame, table_name: str = "daily_summaries") -> bool:
        """Saves or updates daily summary data in the database."""
        if summary_df is None or summary_df.empty:
            print("[WARN] No data provided to save.")
            return False

        try:
            with self._get_connection() as conn:
                summary_df.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"[SUCCESS] Saved {len(summary_df)} records to database table '{table_name}'.")
                return True
        except sqlite3.Error as e:
            print(f"[ERROR] Database save failed: {e}")
            return False

    def load_summary(self, table_name: str = "daily_summaries") -> Optional[pd.DataFrame]:
        """Reads summary data back from the database."""
        try:
            with self._get_connection() as conn:
                query = f"SELECT * FROM {table_name}"
                return pd.read_sql_query(query, conn)
        except sqlite3.Error as e:
            print(f"[ERROR] Database read failed: {e}")
            return None