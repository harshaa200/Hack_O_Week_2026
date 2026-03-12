import os
import sys

# Ensure src can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_processor import DataProcessor
from src.predictor import PeakPredictor
from src.dashboard import ElectricityDashboard

def main():
    try:
        # Initialize components
        print("Initializing components...")
        processor = DataProcessor()
        predictor = PeakPredictor()
        
        # Load and prepare data
        # Check if data file exists, otherwise use synthetic
        data_path = 'data/electricity_data.csv'
        if os.path.exists(data_path):
            processor.load_data(data_path)
        else:
            print(f"Data file not found at {data_path}. Using synthetic data.")
            processor.load_data()
            
        processor.clean_data()
        
        # Dashboard handles the rest (smoothing, feature extraction, training) via callbacks
        # But we initialize the dashboard with the components
        
        dashboard = ElectricityDashboard(processor, predictor)
        
        # Run the dashboard
        dashboard.run(debug=False)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
