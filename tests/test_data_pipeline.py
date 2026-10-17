"""
Unit tests for Delhi Weather Data Pipeline
Sprint 1: Automated testing for CI/CD validation
Compatible with pytest (CI runner) and standalone unittest.
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    import pytest
except ImportError:
    pytest = None

from app import load_and_clean_data, find_available_datasets


def test_dataset_files_exist():
    """Verify that expected CSV datasets are present in project directory."""
    datasets = find_available_datasets()
    assert len(datasets) > 0, "No CSV datasets found in project root."
    assert any("DailyDelhiClimateTrain.csv" in f or "DailyDelhiClimateTest.csv" in f for f in datasets), (
        "Expected Delhi Climate dataset files not found."
    )


def test_data_loading_combined():
    """Verify combined data loading pipeline produces a valid DataFrame."""
    df, name = load_and_clean_data("Combined (Train + Test)")
    assert df is not None, "Dataframe should not be None."
    assert not df.empty, "Dataframe should not be empty."
    assert len(df) >= 1000, f"Expected >1000 observations in combined dataset, got {len(df)}."


def test_required_canonical_columns():
    """Ensure all required meteorological columns exist after cleaning."""
    df, _ = load_and_clean_data("Combined (Train + Test)")
    required_cols = ["date", "meantemp", "humidity", "wind_speed", "meanpressure"]
    for col in required_cols:
        assert col in df.columns, f"Required column '{col}' is missing from cleaned DataFrame."


def test_date_column_properties():
    """Ensure date column is converted to datetime, deduplicated, and sorted."""
    df, _ = load_and_clean_data("Combined (Train + Test)")
    
    # Check datetime dtype
    assert pd.api.types.is_datetime64_any_dtype(df["date"]), "Date column must be datetime64."
    
    # Check for no null dates
    assert df["date"].isnull().sum() == 0, "Date column must not contain null values."
    
    # Check for no duplicate dates
    assert df["date"].duplicated().sum() == 0, "Date column must not contain duplicate records."
    
    # Check chronological ordering
    assert df["date"].is_monotonic_increasing, "Dataset must be chronologically sorted by date."


def test_numerical_ranges():
    """Verify that numerical meteorological readings fall within realistic physical ranges."""
    df, _ = load_and_clean_data("Combined (Train + Test)")
    
    # Temperature in Delhi (between 0°C and 55°C)
    assert df["meantemp"].min() >= 0, f"Unrealistic minimum temperature: {df['meantemp'].min()}"
    assert df["meantemp"].max() <= 55, f"Unrealistic maximum temperature: {df['meantemp'].max()}"
    
    # Relative humidity (between 0% and 100%)
    assert df["humidity"].min() >= 0, f"Humidity cannot be negative: {df['humidity'].min()}"
    assert df["humidity"].max() <= 100.1, f"Humidity cannot exceed 100%: {df['humidity'].max()}"
    
    # Wind speed (positive values)
    assert df["wind_speed"].min() >= 0, f"Wind speed cannot be negative: {df['wind_speed'].min()}"


def test_monthly_aggregation():
    """Verify that month-based aggregation computes valid mean temperature for all 12 calendar months."""
    df, _ = load_and_clean_data("Combined (Train + Test)")
    monthly = df.groupby("month_name", as_index=False)["meantemp"].mean()
    
    assert len(monthly) == 12, f"Expected 12 months in monthly aggregation, got {len(monthly)}."
    assert not monthly["meantemp"].isnull().any(), "Monthly mean temperatures must not be null."


if __name__ == "__main__":
    test_dataset_files_exist()
    test_data_loading_combined()
    test_required_canonical_columns()
    test_date_column_properties()
    test_numerical_ranges()
    test_monthly_aggregation()
    print("All unit tests passed successfully!")
