from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd, numpy as np, pickle, os

app = Flask(__name__, static_folder='static'); CORS(app)
data, model_bundle, heatmap_cache = None, None, None

def load():
    global data, model_bundle, heatmap_cache

    if os.path.exists('hvac_data.csv'):
        data = pd.read_csv('hvac_data.csv')
        data['timestamp'] = pd.to_datetime(data['timestamp'])

    if os.path.exists('model.pkl'):
        with open('model.pkl', 'rb') as f:
            model_bundle = pickle.load(f)

    # Precompute heatmap for faster API responses
    if data is not None:
        pivot = data.pivot_table(
            values='cooling_kwh',
            index='zone_name',
            columns='hour',
            aggfunc='mean'
        ).fillna(0)

        heatmap_cache = {
            'zones': list(pivot.index),
            'hours': list(pivot.columns),
            'matrix': np.round(pivot.values, 2).tolist()
        }

@app.route('/')
def index(): return send_from_directory('static', 'index.html')

@app.route('/api/historical')
def historical():
    if data is None:
        return jsonify({'success': False}), 400

    # Limit dataset size for faster charts
    sample_size = min(1200, len(data))
    d = data.sample(sample_size).copy()

    d['timestamp'] = d['timestamp'].astype(str)

    return jsonify({'success': True, 'data': d.to_dict(orient='records')})

@app.route('/api/stats')
def stats():
    if model_bundle is None: return jsonify({'success': False}), 400
    return jsonify({'success': True, 'metrics': model_bundle['metrics'],
        'summary': {'records': len(data), 'avg_cooling': round(float(data['cooling_kwh'].mean()), 2),
            'zones': data['zone_name'].nunique()}})

@app.route('/api/heatmap')
def heatmap():
    """Return precomputed Zone × Hour heatmap."""

    if heatmap_cache is None:
        return jsonify({'success': False}), 400

    return jsonify({
        'success': True,
        'zones': heatmap_cache['zones'],
        'hours': heatmap_cache['hours'],
        'matrix': heatmap_cache['matrix']
    })

if __name__ == '__main__':
    print("=" * 50); print("HVAC Optimization in Labs — Dashboard"); print("=" * 50)
    load(); print("-> http://localhost:5004"); app.run(host='0.0.0.0', port=5004, debug=False, threaded=True)
