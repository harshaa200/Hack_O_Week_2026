# Week 1: Peak Hour Electricity Analysis

## Overview
This project is an interactive dashboard for analyzing hourly electricity consumption data. It focuses on predicting evening peak loads using linear regression and moving average smoothing.

## Key Features
- **Moving Average Smoothing**: Configurable window to reduce noise.
- **Predictive Modeling**: Linear Regression to forecast evening peak hours.
- **Interactive Dashboard**: Built with Plotly Dash, featuring real-time visualization of:
  - Raw vs. Smoothed Data
  - Actual vs. Predicted Load
  - Evening Peak Trends
  - Weekly Consumption Heatmap

## Technical Stack
- **Python**: Core logic.
- **Dash & Plotly**: Web dashboard and visualizations.
- **Scikit-learn**: Linear Regression model.
- **Pandas/NumPy**: Data manipulation.

## Setup & Execution
1. **Dependencies**: `pip install -r requirements.txt`
2. **Data**: Uses `data/electricity_data.csv` or generates synthetic data automatically.
3. **Run**: `python run_dashboard.py` (Note: This script was recreated to fix a missing entry point).
4. **Access**: `http://localhost:8050`
