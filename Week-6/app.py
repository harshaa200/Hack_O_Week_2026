from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd, pickle, os
import numpy as np

app = Flask(__name__, static_folder='static'); CORS(app)
data, meta, day_analysis, model = None, None, None, None

def load():
    global data, meta, day_analysis, model
    if os.path.exists('sports_data.csv'):
        data = pd.read_csv('sports_data.csv'); data['timestamp'] = pd.to_datetime(data['timestamp'])
    if os.path.exists('model_meta.pkl'):
        with open('model_meta.pkl', 'rb') as f: meta = pickle.load(f)
    if os.path.exists('day_analysis.pkl'):
        with open('day_analysis.pkl', 'rb') as f: day_analysis = pickle.load(f)
    if os.path.exists('lstm_model.keras'):
        try:
            from tensorflow.keras.models import load_model
            model = load_model('lstm_model.keras')
        except Exception:
            model = None
    elif os.path.exists('lstm_model.pkl'):
        with open('lstm_model.pkl', 'rb') as f:
            model = pickle.load(f)

load()

@app.route('/')
def index(): return send_from_directory('static', 'index.html')

@app.route('/api/health')
def health():
    return jsonify({
        'success': True,
        'has_data': data is not None,
        'has_meta': meta is not None,
        'has_day_analysis': day_analysis is not None,
        'has_model': model is not None,
    })

@app.route('/api/historical')
def historical():
    if data is None: return jsonify({'success': False}), 400
    day_type = request.args.get('day_type')
    d = data if day_type is None else data[data['day_type'] == day_type]
    d = d.copy(); d['timestamp'] = d['timestamp'].astype(str)
    return jsonify({'success': True, 'data': d.to_dict(orient='records'), 'total': len(d)})

@app.route('/api/stats')
def stats():
    if meta is None or data is None: return jsonify({'success': False}), 400
    return jsonify({'success': True, 'metrics': meta.get('metrics', {}), 'day_analysis': day_analysis or {},
        'summary': {'records': len(data), 'avg_energy': round(float(data['energy_kwh'].mean()), 2)}})

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None and data is None:
        return jsonify({'success': False}), 400

    payload = request.get_json(silent=True) or {}
    history = payload.get('history')
    if history is None:
        if data is None:
            return jsonify({'success': False, 'error': 'No data loaded'}), 400
        history = data['energy_kwh'].tail(24).tolist()

    try:
        history = [float(x) for x in history][-24:]
    except Exception:
        return jsonify({'success': False, 'error': 'history must be a list of numbers'}), 400

    if len(history) < 24:
        return jsonify({'success': False, 'error': 'Need at least 24 history points'}), 400

    x = np.array(history, dtype=float)
    try:
        if hasattr(model, 'predict') and 'keras' in type(model).__module__:
            yhat = float(model.predict(x.reshape(1, 24, 1), verbose=0).flatten()[0])
        else:
            yhat = float(model.predict(x.reshape(1, -1)).flatten()[0])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'success': True, 'prediction_kwh': round(yhat, 3), 'seq_length': 24})

@app.route('/api/night-analysis')
def night_analysis():
    if data is None: return jsonify({'success': False}), 400

    d = data.copy()
    is_night = (d['hour'] >= 18) | (d['hour'] < 6)
    night = d[is_night]
    day = d[~is_night]

    def s(df):
        if len(df) == 0:
            return {'count': 0, 'avg_kwh': 0, 'max_kwh': 0}
        return {
            'count': int(len(df)),
            'avg_kwh': round(float(df['energy_kwh'].mean()), 3),
            'max_kwh': round(float(df['energy_kwh'].max()), 3),
        }

    by_type = {}
    for dt in sorted(d['day_type'].unique()):
        by_type[dt] = {'night': s(night[night['day_type'] == dt]), 'day': s(day[day['day_type'] == dt])}

    return jsonify({'success': True, 'overall': {'night': s(night), 'day': s(day)}, 'by_day_type': by_type})

if __name__ == '__main__':
    print("=" * 50); print("Sports Facility Night Usage - Energy Dashboard"); print("=" * 50)
    print("-> http://localhost:5005"); app.run(port=5005, debug=False)
