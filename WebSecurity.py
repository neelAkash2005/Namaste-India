# WebSecurity.py
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from flask import session, request, redirect, url_for, render_template_string
import bleach

# --- Assume 'app' is imported from app.py ---
from app import app  # IMPORTANT: import the existing Flask app

# --- Session & security config ---
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # Set True in production
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

# --- Database setup ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- CSRF & Login ---
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# --- User model (for DB) ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- Security headers ---
@app.after_request
def set_security_headers(resp):
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return resp

# --- XSS-safe comment posting ---
ALLOWED_TAGS = ["b", "i", "strong", "em", "a", "code"]
ALLOWED_ATTRS = {"a": ["href", "title", "rel"]}

@app.route("/comment", methods=["GET", "POST"])
def post_comment():
    comments = session.get("comments", [])
    if request.method == "POST":
        raw = request.form.get("comment", "")
        cleaned = bleach.clean(raw, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
        comments.append(cleaned)
        session["comments"] = comments
        return redirect(url_for("post_comment"))
    return render_template_string("""
        <h2>Comments (XSS-safe)</h2>
        <form method="post">{{ csrf_token() }}
            <textarea name="comment" rows="3" cols="40" placeholder="Say hi (HTML allowed but sanitized)"></textarea>
            <button>Post</button>
        </form>
        <ul>{% for c in comments %}<li>{{ c|safe }}</li>{% endfor %}</ul>
    """, comments=comments)

# --- Optional: session hijack / integrity checks ---
@app.before_request
def enforce_session_controls():
    if current_user.is_authenticated:
        if session.get("ua") != request.headers.get("User-Agent", "")[:120]:
            logout_user()
            session.clear()
            return "Session integrity check failed. Please sign in again.", 401
        
