import os
import pickle
from flask import Flask, request, jsonify, send_from_directory, session
import hashlib
import json
import pandas as pd

# ---------------------------
# User handling
# ---------------------------
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

# ---------------------------
# Flask app setup
# ---------------------------
app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-please-change')


# ---------------------------
# WebSecurity integration
# ---------------------------
# Import init function from WebSecurity.py and initialize



MODEL_PATH = 'model.pkl'

# ---------------------------
# Model loading
# ---------------------------
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
    # placeholders to avoid NameError
    vectorizer = None
    tfidf = None
    sim_matrix = None
    city_df = None
    city_col = None
    dur_col = None
    time_col = None
    city_to_idx = None

# ---------------------------
# Routes
# ---------------------------

@app.route('/recommend', methods=['GET'])
def recommend_route():
    """Return top-n similar cities for a given city name."""
    city = request.args.get('city')
    if not city:
        return jsonify({'error': "Missing required query parameter: city"}), 400

    try:
        topn = int(request.args.get('topn', 5))
    except ValueError:
        return jsonify({'error': "topn must be an integer"}), 400

    if artifacts is None or city_to_idx is None or sim_matrix is None:
        return jsonify({'error': 'Model not loaded. Please run the notebook to create model.pkl'}), 500

    # fuzzy match if exact not found
    if city not in city_to_idx:
        candidates = [c for c in city_to_idx.keys() if c.lower() == city.lower()]
        if candidates:
            city = candidates[0]
        else:
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


# ---- Static HTML pages ----
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/login')
def login_page():
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/signup')
def signup_page():
    return send_from_directory(app.static_folder, 'signup.html')

@app.route('/kolkata')
def kolkata_page():
    return send_from_directory(app.static_folder, 'kolkatapage.html')

@app.route('/varanasi')
def varanasi_page():
    return send_from_directory(app.static_folder, 'varanasipage.html')

@app.route('/goa')
def goa_page():
    return send_from_directory(app.static_folder, 'goapage.html')

@app.route('/mumbai')
def mumbai_page():
    return send_from_directory(app.static_folder, 'mumbaipage.html')

@app.route('/shimla')
def shimla_page():
    return send_from_directory(app.static_folder, 'shimlapage.html')

@app.route('/chennai')
def chennai_page():
    return send_from_directory(app.static_folder, 'chennaipage.html')

@app.route('/jaipur')
def jaipur_page():
    return send_from_directory(app.static_folder, 'jaipurpage.html')

@app.route('/delhi')
def delhi_page():
    return send_from_directory(app.static_folder, 'delhipage.html')

@app.route('/tips')
def tips_page():
    return send_from_directory(app.static_folder, 'tips.html')

@app.route('/time')
def time_page():
    return send_from_directory(app.static_folder, 'time.html')

@app.route('/market')
def market_page():
    return send_from_directory(app.static_folder, 'market.html')

@app.route('/index')
def index_page():
    return send_from_directory(app.static_folder, 'index.html')





# ---- Auth API ----
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

# ---------------------------
# chat bot

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_msg = (data.get("message") or "").lower()

    # Simple rule-based responses
    if any(word in user_msg for word in ["hello", "hi", "hey"]):
        reply = "👋 Hello! I’m your travel assistant. How can I help you today?"
    elif "help" in user_msg:
        reply = "💡 You can ask me about cities, booking options, best time to visit, food, or travel tips!"
    elif "recommend" in user_msg or "suggest" in user_msg:
        reply = "🌍 Looking for ideas? Try beaches in Goa, forts in Jaipur, backwaters in Kerala, or mountains in Himachal Pradesh!"
    elif "book" in user_msg or "ticket" in user_msg or "hotel" in user_msg:
        reply = "🛫 You can book flights, trains, buses, or hotels in the 'Book Now' section."
    
    # City-specific answers
    elif "kolkata" in user_msg:
        reply = "🌆 Kolkata is the City of Joy — famous for Durga Puja, Howrah Bridge, Victoria Memorial, and street food."
    elif "goa" in user_msg:
        reply = "🏖 Goa is perfect for beaches, nightlife, water sports, and fun!"
    elif "delhi" in user_msg:
        reply = "🏰 Delhi is rich with history — visit Red Fort, India Gate, Lotus Temple, and Chandni Chowk for food!"
    elif "mumbai" in user_msg or "bombay" in user_msg:
        reply = "🌇 Mumbai is the City of Dreams — don’t miss Marine Drive, Gateway of India, Bollywood vibes, and street food!"
    elif "jaipur" in user_msg:
        reply = "🏯 Jaipur is the Pink City — famous for Hawa Mahal, Amber Fort, and vibrant bazaars!"
    elif "kerala" in user_msg:
        reply = "🌴 Kerala is God’s Own Country — enjoy houseboats in Alleppey, Munnar tea gardens, and backwaters."
    elif "himachal" in user_msg or "manali" in user_msg or "shimla" in user_msg:
        reply = "⛰ Himachal is great for mountains, trekking, snow, and adventure — perfect for Manali and Shimla trips."
    elif "chennai" in user_msg:
        reply = "🌊 Chennai is famous for Marina Beach, temples, and delicious South Indian food!"
    elif "bengaluru" in user_msg or "bangalore" in user_msg:
        reply = "🌳 Bengaluru is the Garden City — famous for IT hub, parks, pubs, and pleasant weather!"
    elif "agra" in user_msg or "taj mahal" in user_msg:
        reply = "🏛 Agra is home to the Taj Mahal — one of the Seven Wonders of the World!"
    
    # Experience-specific questions
    elif "food" in user_msg:
        reply = "🍴 India is a food paradise! Try pani puri in Mumbai, rosogolla in Kolkata, biryani in Hyderabad, and dosa in Chennai!"
    elif "festival" in user_msg:
        reply = "🎉 India celebrates many festivals — Durga Puja in Kolkata, Diwali across India, Holi in Mathura, and Ganesh Chaturthi in Mumbai."
    elif "best time" in user_msg or "season" in user_msg:
        reply = "🗓 Best time to visit depends on the city! Winter (Oct–Feb) is great for most places, while Goa & Kerala are perfect in November–March."
    elif "mountain" in user_msg or "hill station" in user_msg:
        reply = "⛰ For mountains, try Manali, Shimla, Darjeeling, Ooty, or Leh-Ladakh!"
    elif "beach" in user_msg:
        reply = "🏝 For beaches, try Goa, Pondicherry, Andaman & Nicobar Islands, or Kerala!"
    elif "shopping" in user_msg:
        reply = "🛍 For shopping, visit Chandni Chowk (Delhi), New Market (Kolkata), Commercial Street (Bengaluru), and Colaba Causeway (Mumbai)."
    elif "itinerary" in user_msg or "plan trip" in user_msg:
        reply = "📅 Sure! Tell me the city and days, and I can suggest a short travel plan."
    
     # City-specific answers
    elif "kolkata" in user_msg:
        reply = ("🌆 Kolkata, the City of Joy — famous for Durga Puja, Howrah Bridge, Victoria Memorial, "
                 "and street food like rosogolla and puchka.")
    elif "varanasi" in user_msg:
        reply = ("🛕 Varanasi — spiritual heart of India on the Ganges, known for ghats, "
                 "sunrise boat rides, Kashi Vishwanath Temple, and silk weaving.")
    elif "goa" in user_msg:
        reply = ("🏖 Goa — beaches, nightlife, water sports, Portuguese heritage, and seafood delights!")
    elif "mumbai" in user_msg:
        reply = ("🌇 Mumbai, the City of Dreams — visit Gateway of India, Marine Drive, Bollywood spots, "
                 "and street food like vada pav and pav bhaji.")
    elif "shimla" in user_msg:
        reply = ("⛰ Shimla — queen of hills, perfect for snow in winter, Mall Road shopping, "
                 "and scenic viewpoints.")
    elif "chennai" in user_msg:
        reply = ("🌊 Chennai — Marina Beach, Kapaleeshwarar Temple, rich South Indian culture, "
                 "and filter coffee!")
    elif "jaipur" in user_msg:
        reply = ("🏯 Jaipur, the Pink City — Amber Fort, Hawa Mahal, city palaces, and traditional Rajasthani cuisine.")
    elif "delhi" in user_msg:
        reply = ("🏛 Delhi — Red Fort, India Gate, Lotus Temple, Chandni Chowk for street food, "
                 "blend of modern & historical India.")

    # Theme-based queries
    elif "food" in user_msg:
        reply = ("🍴 Try Kolkata’s puchka, Mumbai’s vada pav, Chennai’s dosa, Jaipur’s dal baati, "
                 "Varanasi’s kachori, and Goa’s seafood!")
    elif "festival" in user_msg:
        reply = ("🎉 Major festivals: Durga Puja in Kolkata, Diwali nationwide, Holi in Mathura, "
                 "Ganesh Chaturthi in Mumbai, and Ganga Aarti in Varanasi.")
    elif "best time" in user_msg or "season" in user_msg:
        reply = ("🗓 Best travel times: Oct–Feb is ideal for most cities. Hill stations like Shimla in summer, "
                 "Goa and Kerala in winter.")
    elif "mountain" in user_msg or "hill station" in user_msg:
        reply = "⛰ For mountains: Shimla, Manali, Darjeeling, Ooty, or Himachal Pradesh regions."
    elif "beach" in user_msg:
        reply = "🏝 For beaches: Goa, Kerala, Pondicherry, Andaman & Nicobar Islands."
    elif "shopping" in user_msg:
        reply = ("🛍 Best shopping: Chandni Chowk (Delhi), New Market (Kolkata), Colaba Causeway (Mumbai), "
                 "Johari Bazaar (Jaipur), Mall Road (Shimla).")
    elif "itinerary" in user_msg or "plan trip" in user_msg:
        reply = "📅 Tell me the city and number of days, and I can suggest a mini travel plan!"

    elif "help" in user_msg:
        reply = "🆘 How can I assist you further?"
    
    #Detailed city guides
    # Kolkata  
    elif "kolkata" in user_msg:
        reply = (
        "🌆 Kolkata — the City of Joy!\n\n"
        "🏛 Famous Landmarks: Victoria Memorial, Howrah Bridge, Indian Museum, Marble Palace.\n"
        "🍴 Food & Cuisine: Street food like puchka, kathi rolls, rosogolla, mishti doi.\n"
        "🎉 Festivals: Durga Puja (main event), Diwali, Kali Puja.\n"
        "🗓 Best Time to Visit: October to February (cool & festive season).\n"
        "🏞 Activities: Tram rides, river cruises on Hooghly, exploring colonial architecture.\n"
        "🛍 Shopping: New Market, Gariahat Market, Kumartuli crafts.\n"
        "💡 Travel Tips: Avoid peak hours for traffic; use metro for faster travel.\n"
        "📅 Suggested Itinerary: "
        "Day 1 – Victoria Memorial, Indian Museum, Park Street for dinner; "
        "Day 2 – Howrah Bridge, Kumartuli, Princep Ghat boat ride."
    )

    # Varanasi
    elif "varanasi" in user_msg:
        reply = (
        "🛕 Varanasi — spiritual heart of India!\n\n"
        "🏛 Famous Landmarks: Kashi Vishwanath Temple, Dashashwamedh Ghat, Sarnath.\n"
        "🍴 Food & Cuisine: Kachori sabzi, Banarasi paan, Malaiyo in winter.\n"
        "🎉 Festivals: Ganga Mahotsav, Dev Deepawali, Diwali.\n"
        "🗓 Best Time to Visit: October to March.\n"
        "🏞 Activities: Sunrise boat ride on the Ganges, attend Ganga Aarti, explore silk weaving streets.\n"
        "🛍 Shopping: Banarasi sarees, brassware, handicrafts.\n"
        "📅 Suggested Itinerary: Day 1 – Ghats + evening Ganga Aarti; Day 2 – Sarnath + local shopping."
    )

# Goa
    elif "goa" in user_msg:
        reply = (
        "🏖 Goa — beaches, nightlife, and Portuguese heritage!\n\n"
        "🏛 Famous Landmarks: Basilica of Bom Jesus, Fort Aguada, Chapora Fort.\n"
        "🍴 Food & Cuisine: Goan fish curry, vindaloo, bebinca, seafood.\n"
        "🎉 Festivals: Carnival (Feb), Shigmo, Christmas, Sunburn Music Festival.\n"
        "🗓 Best Time to Visit: November to March.\n"
        "🏞 Activities: Beaches, water sports, nightclubs, island hopping.\n"
        "🛍 Shopping: Flea markets in Anjuna & Mapusa.\n"
        "📅 Suggested Itinerary: Day 1 – North Goa beaches + Fort Aguada; Day 2 – South Goa beaches + Basilica."
    )

# Mumbai
    elif "mumbai" in user_msg:
        reply = (
        "🌇 Mumbai — City of Dreams!\n\n"
        "🏛 Famous Landmarks: Gateway of India, Marine Drive, Chhatrapati Shivaji Terminus, Elephanta Caves.\n"
        "🍴 Food & Cuisine: Vada pav, pav bhaji, bhel puri, seafood.\n"
        "🎉 Festivals: Ganesh Chaturthi, Diwali, Mumbai Film Festival.\n"
        "🗓 Best Time to Visit: November to February.\n"
        "🏞 Activities: Bollywood tours, nightlife, beaches, street food tour.\n"
        "🛍 Shopping: Colaba Causeway, Linking Road, Crawford Market.\n"
        "📅 Suggested Itinerary: Day 1 – Gateway of India, Colaba, Marine Drive; Day 2 – Elephanta Caves + shopping."
    )

# Shimla
    elif "shimla" in user_msg:
        reply = (
        "⛰ Shimla — Queen of Hills!\n\n"
        "🏛 Famous Landmarks: Mall Road, The Ridge, Jakhoo Temple.\n"
        "🍴 Food & Cuisine: Himachali cuisine, chha gosht, siddu.\n"
        "🎉 Festivals: Summer Festival, Winter Carnival.\n"
        "🗓 Best Time to Visit: March to June (summer), December to February (snow).\n"
        "🏞 Activities: Trekking, toy train rides, mountain walks.\n"
        "🛍 Shopping: Mall Road shops, Lakkar Bazaar.\n"
        "📅 Suggested Itinerary: Day 1 – Mall Road + Ridge + Christ Church; Day 2 – Jakhoo Hill + Kufri trip."
    )

# Chennai
    elif "chennai" in user_msg:
        reply = (
        "🌊 Chennai — Gateway to South India!\n\n"
        "🏛 Famous Landmarks: Marina Beach, Kapaleeshwarar Temple, Fort St. George.\n"
        "🍴 Food & Cuisine: Dosa, idli, filter coffee, Chettinad cuisine.\n"
        "🎉 Festivals: Pongal, Diwali, Chennai Music Season.\n"
        "🗓 Best Time to Visit: November to February.\n"
        "🏞 Activities: Beach walks, temple tours, cultural shows.\n"
        "🛍 Shopping: T Nagar, Pondy Bazaar.\n"
        "📅 Suggested Itinerary: Day 1 – Marina Beach + Fort St. George; Day 2 – Kapaleeshwarar Temple + shopping."
    )

# Jaipur
    elif "jaipur" in user_msg:
        reply = (
        "🏯 Jaipur — The Pink City!\n\n"
        "🏛 Famous Landmarks: Amber Fort, Hawa Mahal, City Palace, Jantar Mantar.\n"
        "🍴 Food & Cuisine: Dal Baati Churma, Ghevar, Laal Maas.\n"
        "🎉 Festivals: Jaipur Literature Festival, Teej, Gangaur.\n"
        "🗓 Best Time to Visit: October to March.\n"
        "🏞 Activities: Fort tours, cultural shows, traditional markets.\n"
        "🛍 Shopping: Johari Bazaar, Bapu Bazaar, Tripolia Bazaar.\n"
        "📅 Suggested Itinerary: Day 1 – Amber Fort + City Palace; Day 2 – Hawa Mahal + shopping + local food."
    )

# Delhi
    elif "delhi" in user_msg:
        reply = (
        "🏛 Delhi — Capital of India!\n\n"
        "🏛 Famous Landmarks: Red Fort, India Gate, Qutub Minar, Lotus Temple, Chandni Chowk.\n"
        "🍴 Food & Cuisine: Chole Bhature, Parathas, Street food in Chandni Chowk.\n"
        "🎉 Festivals: Diwali, Republic Day, Holi.\n"
        "🗓 Best Time to Visit: October to March.\n"
        "🏞 Activities: Sightseeing tours, heritage walks, food walks.\n"
        "🛍 Shopping: Dilli Haat, Sarojini Nagar, Janpath.\n"
        "📅 Suggested Itinerary: Day 1 – Red Fort + Chandni Chowk + India Gate; Day 2 – Qutub Minar + Lotus Temple."
    )

#Extra
    elif "travel tips" in user_msg:
        reply = "💡 Always check weather, local transport, and book popular attractions in advance!"
    elif "visa" in user_msg or "entry" in user_msg:
        reply = "🛂 Indian visa info: Most travelers need an e-visa; check government website for details."
    elif "transport" in user_msg or "getting around" in user_msg:
        reply = "🚗 Use metro, buses, taxis, or rideshares. For hill stations, taxis or local buses work best."
    elif "budget" in user_msg or "cheap trip" in user_msg:
        reply = "💰 Budget tips: Use local transport, street food, and book hotels in advance for savings."

    else:
        reply = "🤔 I’m not sure, but you can explore destinations on the site!"

    return jsonify({"reply": reply})



# ---------------------------
# Run server
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)