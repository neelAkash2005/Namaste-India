from datetime import timedelta
from flask import Flask, request, render_template_string, redirect, url_for, session, make_response, abort
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
import bleach
import os
import stripe
from flask import jsonify 

# --- Flask app setup ---
app = Flask(__name__)
# --- Session & secret config (Session Hijack mitigation) ---
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["SESSION_COOKIE_HTTPONLY"] = True           # helps stop XSS stealing cookies
app.config["SESSION_COOKIE_SECURE"] = False            # set True in production (HTTPS only)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"          # 'Strict' or 'Lax' reduces CSRF via cross-site requests
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)  # idle timeout

# --- Database (SQL Injection prevention via ORM/params) ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- CSRF protection for all POST/PUT/PATCH/DELETE ---
csrf = CSRFProtect(app)

# --- Login manager (Broken Auth & session controls) ---
login_manager = LoginManager(app)
login_manager.login_view = "login"

# --- Simple model ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- Security headers (XSS & Clickjacking & MIME sniffing) ---
@app.after_request
def set_security_headers(resp):
    # Content Security Policy: restrict where scripts/styles/images can load from
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    resp.headers["X-Frame-Options"] = "DENY"               # anti clickjacking
    resp.headers["X-Content-Type-Options"] = "nosniff"      # stop MIME sniffing
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return resp

# --- TEMPLATES (Jinja auto-escapes by default => XSS mitigation) ---
BASE = """
<!doctype html>
<title>Secure Demo</title>
<h1>Secure Demo</h1>
{% if current_user.is_authenticated %}
  <p>Hi, {{ current_user.username }}!</p>
  <form method="post" action="{{ url_for('logout') }}">{{ csrf_token() }}
    <button type="submit">Logout</button>
  </form>
{% else %}
  <a href="{{ url_for('register') }}">Register</a> |
  <a href="{{ url_for('login') }}">Login</a>
{% endif %}
<hr>
<nav>
  <a href="{{ url_for('index') }}">Home</a> |
  <a href="{{ url_for('search') }}">Search (safe SQL)</a> |
  <a href="{{ url_for('post_comment') }}">Post Comment (XSS-safe)</a>
</nav>
<hr>
{% block body %}{% endblock %}
"""


# --------- 1) SQL INJECTION SAFE SEARCH ---------
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        q = request.form.get("q", "")
        # EXAMPLE A (ORM): safe by default
        users = User.query.filter(User.username.like(f"%{q}%")).all()

        # EXAMPLE B (raw SQL parameters): NEVER format strings directly; use bound params
        rows = db.session.execute(text("SELECT username FROM user WHERE username LIKE :q"), {"q": f"%{q}%"}).fetchall()

        return render_template_string(
            BASE + """
{% block body %}
<h2>Search results (safe)</h2>
<p>You searched for: {{ q }}</p>
<h3>ORM results</h3>
<ul>{% for u in users %}<li>{{ u.username }}</li>{% endfor %}</ul>
<h3>Raw SQL (param-bound) results</h3>
<ul>{% for r in rows %}<li>{{ r.username }}</li>{% endfor %}</ul>
<form method="post">{{ csrf_token() }}<input name="q" placeholder="username"><button>Search</button></form>
{% endblock %}
""",
            q=q,
            users=users,
            rows=rows,
        )
    return render_template_string(
        BASE + """
{% block body %}
<h2>Search</h2>
<form method="post">{{ csrf_token() }}<input name="q" placeholder="username"><button>Search</button></form>
{% endblock %}
"""
    )

# --------- 2) XSS-SAFE COMMENT POSTING ---------
ALLOWED_TAGS = ["b", "i", "strong", "em", "a", "code"]
ALLOWED_ATTRS = {"a": ["href", "title", "rel"]}

@app.route("/comment", methods=["GET", "POST"])
def post_comment():
    # if you accept rich text, sanitize it before storing or rendering
    comments = session.get("comments", [])
    if request.method == "POST":
        raw = request.form.get("comment", "")
        # bleach sanitizes potentially dangerous HTML (on top of Jinja auto-escape)
        cleaned = bleach.clean(raw, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
        comments.append(cleaned)
        session["comments"] = comments
        return redirect(url_for("post_comment"))
    return render_template_string(
        BASE + """
{% block body %}
<h2>Comments (XSS-safe)</h2>
<form method="post">{{ csrf_token() }}
  <textarea name="comment" rows="3" cols="40" placeholder="Say hi (HTML allowed but sanitized)"></textarea>
  <button>Post</button>
</form>
<ul>
  {% for c in comments %}
    <li>{{ c|safe }}</li>  {# safe because we sanitized with bleach first #}
  {% endfor %}
</ul>
{% endblock %}
""",
        comments=comments,
    )

# --------- 3) CSRF PROTECTION EXAMPLE ---------
# (Already enforced globally via @csrf.exempt default == False)
# Every form includes {{ csrf_token() }} and non-GET methods are verified.

# --------- 4) BROKEN AUTH PREVENTION ---------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            abort(400)
        if User.query.filter_by(username=username).first():
            return "Username taken", 400

        # store HASHES only (never plaintext)
        pw_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
        db.session.add(User(username=username, password_hash=pw_hash))
        db.session.commit()
        return redirect(url_for("login"))

    return render_template_string(
        BASE + """
{% block body %}
<h2>Register</h2>
<form method="post">{{ csrf_token() }}
  <input name="username" placeholder="username" required>
  <input name="password" type="password" placeholder="password" required>
  <button>Create</button>
</form>
{% endblock %}
"""
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            # avoid username enumeration: same message
            return "Invalid credentials", 401

        # --- Session fixation defense: rotate session on login ---
        session.clear()
        login_user(user, remember=False, duration=timedelta(hours=1))
        session.permanent = True  # enable PERMANENT_SESSION_LIFETIME
        # bind some fingerprint (very light heuristic)
        session["ua"] = request.headers.get("User-Agent", "")[:120]
        return redirect(url_for("profile"))
    return render_template_string(
        BASE + """
{% block body %}
<h2>Login</h2>
<form method="post">{{ csrf_token() }}
  <input name="username" placeholder="username" required>
  <input name="password" type="password" placeholder="password" required>
  <button>Login</button>
</form>
{% endblock %}
"""
    )

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    session.clear()  # drop session server-side
    return redirect(url_for("index"))

@app.route("/profile")
@login_required
def profile():
    # --- Session hijack check: crude user-agent match (optional stronger: IP, signed nonce) ---
    if session.get("ua") != request.headers.get("User-Agent", "")[:120]:
        logout_user()
        session.clear()
        return "Session integrity check failed. Please sign in again.", 401

    return render_template_string(
        BASE + """
{% block body %}
<h2>Profile</h2>
<p>Your private area. (Requires auth.)</p>
{% endblock %}
"""
    )

# --------- 5) SESSION HIJACK HARDENING HOOKS ---------
@app.before_request
def enforce_session_controls():
    # Force HTTPS in production (behind a proxy, use ProxyFix / SECURE headers)
    # Here, just demonstrate rejection of insecure cookies if needed.
    pass

# Minimal health check
@app.route("/healthz")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)