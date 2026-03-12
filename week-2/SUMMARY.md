# Week 2: Classroom Usage Forecasting

## Overview
This project is a real-time forecasting system that predicts classroom electricity consumption based on Wi-Fi occupancy data. It utilizes ARIMA time series modeling to provide next-hour predictions.

## Key Features
- **ARIMA Forecasting**: Time series modeling (ARIMA 2,1,2) for next-hour electricity prediction.
- **Occupancy Tracking**: Correlates Wi-Fi connection data with electricity usage.
- **Real-time Dashboard**: Visualizes predictions with 95% confidence intervals.
- **Live Metrics**: Displays RMSE, MAE, and correlation analysis.

## Technical Stack
- **Python**: Backend logic.
- **Flask**: API server.
- **Statsmodels**: ARIMA implementation.
- **Plotly/Chart.js**: Frontend visualizations.

## Setup & Execution
1. **Dependencies**: `pip install -r requirements.txt`
2. **Data**: Uses `classroom_data.csv` (can be generated via `data_generator.py`).
3. **Training**: `python arima_model.py` to train/retrain the model.
4. **Run**: `python app.py`
5. **Access**: `http://localhost:5001` (or 5000, depending on availability).
