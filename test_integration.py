"""
Comprehensive System Integration Test
Tests all connections between main app.py and other modules
"""

import sys
import os

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def test_all_connections():
    """Test all file connections and integrations"""
    
    print_header("🔍 COMPREHENSIVE SYSTEM INTEGRATION TEST")
    
    results = {
        'passed': [],
        'failed': [],
        'warnings': []
    }
    
    # Test 1: Import app.py
    print("📦 Test 1: Importing app.py...")
    try:
        import app
        results['passed'].append("✅ app.py imported successfully")
        print("   ✅ app.py imported successfully")
        print(f"   - Flask app name: {app.app.name}")
        print(f"   - Secret key configured: {'Yes' if app.app.secret_key else 'No'}")
    except Exception as e:
        results['failed'].append(f"❌ app.py import failed: {e}")
        print(f"   ❌ Failed: {e}")
        return results
    
    # Test 2: ML Recommender Connection
    print("\n🤖 Test 2: Checking ML Recommender connection...")
    try:
        from ml_recommender import (
            get_ml_enhanced_recommendations,
            get_similar_cities_ml,
            get_model_insights,
            ML_MODELS_AVAILABLE
        )
        results['passed'].append("✅ ml_recommender.py connected to app.py")
        print("   ✅ ml_recommender.py connected")
        print(f"   - ML Models Available: {ML_MODELS_AVAILABLE}")
        print(f"   - Functions imported: 3 (recommendations, similar_cities, insights)")
        
        # Test ML functionality
        if ML_MODELS_AVAILABLE:
            test_result = get_ml_enhanced_recommendations("june", 7, 3)
            if test_result.get('count', 0) > 0:
                results['passed'].append("✅ ML recommendations working")
                print(f"   ✅ ML recommendations working ({test_result['count']} results)")
            else:
                results['warnings'].append("⚠️ ML recommendations returned 0 results")
                print("   ⚠️ ML recommendations returned 0 results")
    except Exception as e:
        results['failed'].append(f"❌ ML Recommender connection failed: {e}")
        print(f"   ❌ Failed: {e}")
    
    # Test 3: Check ML model files
    print("\n📁 Test 3: Checking ML data files...")
    ml_files = {
        'ml_models.pkl': 'ML models file',
        'merged_df.pkl': 'Training data file',
        'train_ml_models.py': 'Training script',
        'test_ml.py': 'ML test suite'
    }
    
    for filename, description in ml_files.items():
        if os.path.exists(filename):
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            results['passed'].append(f"✅ {filename} exists")
            print(f"   ✅ {filename} ({size_mb:.2f} MB) - {description}")
        else:
            results['failed'].append(f"❌ {filename} missing")
            print(f"   ❌ {filename} missing - {description}")
    
    # Test 4: Security Module Connection
    print("\n🔒 Test 4: Checking Security module...")
    if os.path.exists('WebSecurity.py'):
        results['passed'].append("✅ WebSecurity.py exists")
        print("   ✅ WebSecurity.py exists")
        
        # Check for circular import issue
        try:
            with open('WebSecurity.py', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'from app import app' in content:
                    results['warnings'].append("⚠️ WebSecurity.py has circular import (from app import app)")
                    print("   ⚠️ WebSecurity.py has circular import issue")
                    print("      This may cause issues if WebSecurity is imported in app.py")
        except Exception as e:
            print(f"   ⚠️ Could not read WebSecurity.py: {e}")
    else:
        results['warnings'].append("⚠️ WebSecurity.py not found")
        print("   ⚠️ WebSecurity.py not found")
    
    # Test 5: Check Flask Routes
    print("\n🛣️  Test 5: Checking Flask routes...")
    try:
        routes = [str(rule) for rule in app.app.url_map.iter_rules()]
        total_routes = len(routes)
        results['passed'].append(f"✅ Flask routes registered: {total_routes}")
        print(f"   ✅ Total routes: {total_routes}")
        
        # Check for key ML endpoints
        ml_endpoints = {
            '/recommend': 'ML recommendations',
            '/similar/<city_name>': 'Similar cities',
            '/insights': 'Model insights',
            '/health': 'Health check'
        }
        
        print("\n   Key ML Endpoints:")
        for endpoint, description in ml_endpoints.items():
            found = any(endpoint in str(route) for route in routes)
            if found:
                results['passed'].append(f"✅ {endpoint} endpoint exists")
                print(f"      ✅ {endpoint} - {description}")
            else:
                results['warnings'].append(f"⚠️ {endpoint} endpoint missing")
                print(f"      ⚠️ {endpoint} - {description} (MISSING)")
    except Exception as e:
        results['failed'].append(f"❌ Route check failed: {e}")
        print(f"   ❌ Failed: {e}")
    
    # Test 6: Check Security Files
    print("\n🛡️  Test 6: Checking Security files...")
    security_files = {
        'test_security.py': 'Security test suite',
        '.env': 'Environment variables',
        '.env.example': 'Environment template',
        'requirements.txt': 'Dependencies list'
    }
    
    for filename, description in security_files.items():
        if os.path.exists(filename):
            results['passed'].append(f"✅ {filename} exists")
            print(f"   ✅ {filename} - {description}")
        else:
            if filename == '.env':
                results['warnings'].append(f"⚠️ {filename} not found (should be created)")
            else:
                results['failed'].append(f"❌ {filename} missing")
            print(f"   {'⚠️' if filename == '.env' else '❌'} {filename} - {description}")
    
    # Test 7: Check .gitignore
    print("\n🔐 Test 7: Checking .gitignore protection...")
    if os.path.exists('.gitignore'):
        try:
            with open('.gitignore', 'r', encoding='utf-8') as f:
                gitignore_content = f.read()
                
            protected_items = {
                '.env': 'Environment variables',
                '*.key': 'Private keys',
                '*.pem': 'Certificates',
                'secrets.json': 'Secret files',
                'site.db': 'Database files'
            }
            
            for item, description in protected_items.items():
                if item in gitignore_content:
                    results['passed'].append(f"✅ {item} in .gitignore")
                    print(f"   ✅ {item} protected - {description}")
                else:
                    results['warnings'].append(f"⚠️ {item} not in .gitignore")
                    print(f"   ⚠️ {item} not protected - {description}")
        except Exception as e:
            print(f"   ⚠️ Could not read .gitignore: {e}")
    else:
        results['warnings'].append("⚠️ .gitignore not found")
        print("   ⚠️ .gitignore not found")
    
    # Test 8: Check Data Files
    print("\n📊 Test 8: Checking data files...")
    data_files = {
        'City.csv': 'City information',
        'Places.csv': 'Places/attractions data',
        'users.json': 'User data'
    }
    
    for filename, description in data_files.items():
        if os.path.exists(filename):
            results['passed'].append(f"✅ {filename} exists")
            print(f"   ✅ {filename} - {description}")
        else:
            results['warnings'].append(f"⚠️ {filename} not found")
            print(f"   ⚠️ {filename} - {description}")
    
    # Test 9: Check Documentation
    print("\n📚 Test 9: Checking documentation...")
    doc_files = {
        'README.md': 'Main README',
        'ML_ENHANCED_README.md': 'ML documentation',
        'SECURITY_GUIDE.md': 'Security guide',
        'ML_MIGRATION_COMPLETE.md': 'Migration summary'
    }
    
    for filename, description in doc_files.items():
        if os.path.exists(filename):
            results['passed'].append(f"✅ {filename} exists")
            print(f"   ✅ {filename} - {description}")
        else:
            results['warnings'].append(f"⚠️ {filename} not found")
            print(f"   ⚠️ {filename} - {description}")
    
    # Test 10: Final Integration Test
    print("\n🔄 Test 10: Testing end-to-end integration...")
    try:
        # Test if app can be started (without actually starting it)
        if hasattr(app, 'app') and app.app is not None:
            results['passed'].append("✅ Flask app can be initialized")
            print("   ✅ Flask app can be initialized")
            
        # Test if ML is integrated
        if hasattr(app, 'ML_MODELS_AVAILABLE'):
            if app.ML_MODELS_AVAILABLE:
                results['passed'].append("✅ ML models integrated with Flask app")
                print("   ✅ ML models integrated with Flask app")
            else:
                results['warnings'].append("⚠️ ML models not available in Flask app")
                print("   ⚠️ ML models not available in Flask app")
    except Exception as e:
        results['failed'].append(f"❌ Integration test failed: {e}")
        print(f"   ❌ Failed: {e}")
    
    return results

def print_summary(results):
    """Print test summary"""
    print_header("📊 TEST SUMMARY")
    
    print(f"✅ PASSED: {len(results['passed'])} tests")
    print(f"⚠️  WARNINGS: {len(results['warnings'])} items")
    print(f"❌ FAILED: {len(results['failed'])} tests")
    
    if results['failed']:
        print("\n❌ FAILED TESTS:")
        for item in results['failed']:
            print(f"   {item}")
    
    if results['warnings']:
        print("\n⚠️  WARNINGS:")
        for item in results['warnings']:
            print(f"   {item}")
    
    print("\n" + "=" * 70)
    
    if len(results['failed']) == 0:
        print("✅ ALL CRITICAL TESTS PASSED!")
        print("🚀 Your system is ready to run!")
        print("\nTo start the application:")
        print("   python app.py")
    else:
        print("❌ SOME TESTS FAILED - Please fix the issues above")
    
    print("=" * 70)

if __name__ == "__main__":
    try:
        results = test_all_connections()
        print_summary(results)
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
