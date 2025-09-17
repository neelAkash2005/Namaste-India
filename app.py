import os
import pickle
from flask import Flask, request, jsonify, send_from_directory
import hashlib
import json

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

def hash_password(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()
import pandas as pd
from flask import current_app, session

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-please-change')

MODEL_PATH = 'model.pkl'

# Try to load artifacts but don't crash the server if the file is missing.
artifacts = None
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as f:
            artifacts = pickle.load(f)
    except Exception as e:
        print(f"Warning: failed to load {MODEL_PATH}: {e}")

if artifacts:
    vectorizer = artifacts.get('vectorizer')
    tfidf = artifacts.get('tfidf')
    sim_matrix = artifacts.get('sim_matrix')
    city_df = artifacts.get('city_df')
    city_col = artifacts.get('city_col')
    dur_col = artifacts.get('dur_col')
    time_col = artifacts.get('time_col')
    city_to_idx = artifacts.get('city_to_idx')
else:
    # placeholders to avoid NameError; endpoints will return a helpful error if model absent
    vectorizer = None
    tfidf = None
    sim_matrix = None
    city_df = None
    city_col = None
    dur_col = None
    time_col = None
    city_to_idx = None


@app.route('/recommend', methods=['GET'])
def recommend_route():
    """Return top-n similar cities for a given city name.

    Query params:
      - city: required, city name string
      - topn: optional, default 5
    """
    city = request.args.get('city')
    if not city:
        return jsonify({'error': "Missing required query parameter: city"}), 400

    try:
        topn = int(request.args.get('topn', 5))
    except ValueError:
        return jsonify({'error': "topn must be an integer"}), 400

    # ensure model loaded
    if artifacts is None or city_to_idx is None or sim_matrix is None:
        return jsonify({'error': 'Model not loaded. Please run the notebook to create model.pkl'}), 500

    # fuzzy match if exact not found
    if city not in city_to_idx:
        # simple case-insensitive match
        candidates = [c for c in city_to_idx.keys() if c.lower() == city.lower()]
        if candidates:
            city = candidates[0]
        else:
            # last resort: try partial contains
            candidates = [c for c in city_to_idx.keys() if city.lower() in c.lower()]
            if candidates:
                city = candidates[0]
            else:
                return jsonify({'error': f"City '{city}' not found"}), 404

    idx = city_to_idx[city]
    scores = list(enumerate(sim_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    results = []
    for i, score in scores:
        if i == idx:
            continue
        results.append({
            'city': str(city_df.loc[i, city_col]),
            dur_col: str(city_df.loc[i, dur_col]),
            time_col: str(city_df.loc[i, time_col]),
            'score': float(score)
        })
        if len(results) >= topn:
            break

    return jsonify({'query_city': city, 'results': results})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/')
def index():
    # Serve the static frontend
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/login')
def login_page():
    return send_from_directory(app.static_folder, 'login.html')


@app.route('/signup')
def signup_page():
    return send_from_directory(app.static_folder, 'signup.html')


@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    users = load_users()
    if username in users:
        return jsonify({'error': 'user exists'}), 400
    users[username] = {'pw': hash_password(password)}
    save_users(users)
    return jsonify({'ok': True})


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    users = load_users()
    if username not in users:
        return jsonify({'error': 'invalid credentials'}), 400
    if users[username].get('pw') != hash_password(password):
        return jsonify({'error': 'invalid credentials'}), 400
    # set session so user remains logged in for this demo
    session['username'] = username
    return jsonify({'ok': True, 'username': username})


@app.route('/auth/whoami', methods=['GET'])
def whoami():
    username = session.get('username')
    if not username:
        return jsonify({'ok': False}), 200
    return jsonify({'ok': True, 'username': username})


@app.route('/auth/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'ok': True})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
