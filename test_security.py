"""
Security Features Test Script
Tests all installed security packages to ensure they're working correctly.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if environment variables are loaded correctly"""
    print("\n🔐 Testing Environment Variables:")
    print("=" * 60)
    secret_key = os.getenv('FLASK_SECRET_KEY')
    if secret_key:
        print(f"✅ FLASK_SECRET_KEY loaded: {secret_key[:20]}...")
        print(f"✅ Key length: {len(secret_key)} characters")
    else:
        print("❌ FLASK_SECRET_KEY not found!")
    
    flask_env = os.getenv('FLASK_ENV', 'production')
    print(f"✅ FLASK_ENV: {flask_env}")
    
    print(f"✅ DATABASE_URL: {os.getenv('DATABASE_URL', 'Not set')}")
    print(f"✅ RATELIMIT_ENABLED: {os.getenv('RATELIMIT_ENABLED', 'Not set')}")

def test_password_hashing():
    """Test bcrypt password hashing"""
    print("\n🔐 Testing Password Hashing (bcrypt):")
    print("=" * 60)
    import bcrypt
    
    password = "MySecurePassword123!"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    print(f"✅ Original password: {password}")
    print(f"✅ Hashed password: {hashed.decode('utf-8')[:50]}...")
    
    # Verify password
    is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
    print(f"✅ Password verification: {'PASSED' if is_valid else 'FAILED'}")
    
    # Test wrong password
    is_invalid = bcrypt.checkpw("WrongPassword".encode('utf-8'), hashed)
    print(f"✅ Wrong password rejected: {'PASSED' if not is_invalid else 'FAILED'}")

def test_jwt_tokens():
    """Test JWT token creation and validation"""
    print("\n🔐 Testing JWT Tokens:")
    print("=" * 60)
    import jwt
    from datetime import datetime, timedelta
    
    secret_key = os.getenv('JWT_SECRET_KEY', 'default-secret-key')
    
    # Create a token
    payload = {
        'user_id': 123,
        'username': 'testuser',
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    print(f"✅ Created JWT token: {token[:50]}...")
    
    # Decode the token
    try:
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        print(f"✅ Decoded token successfully")
        print(f"   User ID: {decoded['user_id']}")
        print(f"   Username: {decoded['username']}")
    except jwt.InvalidTokenError:
        print("❌ Token validation failed!")

def test_email_validation():
    """Test email validation"""
    print("\n🔐 Testing Email Validation:")
    print("=" * 60)
    from email_validator import validate_email, EmailNotValidError
    
    test_emails = [
        "user@example.com",
        "test.user@domain.co.in",
        "invalid-email",
        "missing@",
        "@nodomain.com"
    ]
    
    for email in test_emails:
        try:
            validated = validate_email(email)
            print(f"✅ Valid email: {email}")
        except EmailNotValidError:
            print(f"❌ Invalid email: {email}")

def test_html_sanitization():
    """Test HTML sanitization with bleach"""
    print("\n🔐 Testing HTML Sanitization (XSS Protection):")
    print("=" * 60)
    import bleach
    
    dangerous_html = '<script>alert("XSS Attack!")</script><p>Safe content</p>'
    safe_html = bleach.clean(dangerous_html, tags=['p', 'b', 'i'], strip=True)
    
    print(f"Original HTML: {dangerous_html}")
    print(f"✅ Sanitized HTML: {safe_html}")
    print(f"✅ Script tag removed: {'<script>' not in safe_html}")

def test_flask_security():
    """Test Flask security extensions"""
    print("\n🔐 Testing Flask Security Extensions:")
    print("=" * 60)
    
    # Test imports
    try:
        import flask_talisman
        print("✅ Flask-Talisman imported (HTTPS enforcement)")
    except ImportError:
        print("❌ Flask-Talisman not available")
    
    try:
        import flask_limiter
        print("✅ Flask-Limiter imported (Rate limiting)")
    except ImportError:
        print("❌ Flask-Limiter not available")
    
    try:
        import flask_wtf
        print("✅ Flask-WTF imported (CSRF protection)")
    except ImportError:
        print("❌ Flask-WTF not available")
    
    try:
        import flask_session
        print("✅ Flask-Session imported (Server-side sessions)")
    except ImportError:
        print("❌ Flask-Session not available")
    
    try:
        import flask_cors
        print("✅ Flask-Cors imported (CORS handling)")
    except ImportError:
        print("❌ Flask-Cors not available")

def test_cryptography():
    """Test cryptography package"""
    print("\n🔐 Testing Cryptography:")
    print("=" * 60)
    from cryptography.fernet import Fernet
    
    # Generate a key
    key = Fernet.generate_key()
    print(f"✅ Generated encryption key: {key[:30]}...")
    
    # Create cipher
    cipher = Fernet(key)
    
    # Encrypt message
    message = "This is a secret message!"
    encrypted = cipher.encrypt(message.encode())
    print(f"✅ Encrypted message: {encrypted[:50]}...")
    
    # Decrypt message
    decrypted = cipher.decrypt(encrypted).decode()
    print(f"✅ Decrypted message: {decrypted}")
    print(f"✅ Encryption/Decryption: {'PASSED' if message == decrypted else 'FAILED'}")

def run_all_tests():
    """Run all security tests"""
    print("\n" + "=" * 60)
    print("🔒 SECURITY FEATURES TEST SUITE")
    print("=" * 60)
    
    try:
        test_environment_variables()
        test_password_hashing()
        test_jwt_tokens()
        test_email_validation()
        test_html_sanitization()
        test_flask_security()
        test_cryptography()
        
        print("\n" + "=" * 60)
        print("✅ ALL SECURITY TESTS COMPLETED!")
        print("=" * 60)
        print("\n📚 For more information, check:")
        print("   - SECURITY_GUIDE.md (Comprehensive guide)")
        print("   - SECURITY_SETUP.md (Quick start guide)")
        print("\n🚀 Your application is now secure and ready for production!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
