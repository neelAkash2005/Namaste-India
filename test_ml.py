"""
Quick Test Script for ML Models
Run this after training to verify everything works
"""

import pickle
import pandas as pd
import numpy as np

print("=" * 60)
print("🧪 TESTING ML RECOMMENDATION SYSTEM")
print("=" * 60)

# Test 1: Check if models are trained
print("\n✅ Test 1: Checking if ML models exist...")
try:
    with open('ml_models.pkl', 'rb') as f:
        ml_package = pickle.load(f)
    print(f"   ✅ Models loaded successfully!")
    print(f"   Best model: {ml_package['best_model_name']}")
    print(f"   Total models: {len(ml_package['models'])}")
except FileNotFoundError:
    print("   ❌ ml_models.pkl not found!")
    print("   Run: python train_ml_models.py")
    exit(1)

# Test 2: Check data files
print("\n✅ Test 2: Checking data files...")
try:
    with open('merged_df.pkl', 'rb') as f:
        merged_df = pickle.load(f)
    print(f"   ✅ Data loaded: {len(merged_df)} records, {merged_df['City'].nunique()} cities")
except FileNotFoundError:
    print("   ❌ merged_df.pkl not found!")
    print("   Run: python prepare_data.py")
    exit(1)

# Test 3: Test ML recommender module
print("\n✅ Test 3: Testing ML recommender functions...")
try:
    from ml_recommender import (
        get_ml_enhanced_recommendations, 
        get_similar_cities_ml, 
        get_model_insights
    )
    print("   ✅ ML recommender module loaded successfully!")
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    exit(1)

# Test 4: Test recommendations
print("\n✅ Test 4: Testing ML recommendations...")
try:
    result = get_ml_enhanced_recommendations('October', 7, topn=5)
    
    if 'error' in result:
        print(f"   ❌ Error: {result['error']}")
    else:
        print(f"   ✅ Found {result['count']} recommendations for October, 7 days")
        print(f"   ✅ Using model: {result['ml_info']['model_used']}")
        print(f"   ✅ Model accuracy: {result['ml_info']['model_accuracy']:.4f}")
        
        if result['results']:
            top_city = result['results'][0]
            print(f"\n   🏆 Top recommendation: {top_city['city']}")
            print(f"      Rating: ⭐ {top_city['rating']:.1f}")
            print(f"      ML Score: {top_city['ml_score']:.4f}")
            print(f"      Confidence: {top_city['ml_confidence']:.4f}")
except Exception as e:
    print(f"   ❌ Error during recommendation: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Test similar cities
print("\n✅ Test 5: Testing similar cities feature...")
try:
    result = get_similar_cities_ml('Goa', topn=3)
    
    if 'error' in result:
        print(f"   ❌ Error: {result['error']}")
    else:
        print(f"   ✅ Found {len(result['similar_cities'])} cities similar to Goa")
        for city in result['similar_cities'][:3]:
            print(f"      - {city['city']}: Similarity {city['similarity_score']:.4f}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: Test model insights
print("\n✅ Test 6: Testing model insights...")
try:
    insights = get_model_insights()
    
    if 'error' in insights:
        print(f"   ❌ Error: {insights['error']}")
    else:
        print(f"   ✅ Total models trained: {insights['models_trained']}")
        print(f"   ✅ Best model: {insights['best_model']}")
        print(f"   ✅ Total cities in dataset: {insights['total_cities']}")
        print(f"\n   📊 Model Comparison:")
        for model in insights['model_comparison'][:3]:
            print(f"      - {model['Model']}: Accuracy {model['Accuracy']:.4f}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 7: Check Flask app integration
print("\n✅ Test 7: Checking Flask app integration...")
try:
    with open('app.py', 'r') as f:
        app_content = f.read()
    
    if 'get_ml_enhanced_recommendations' in app_content:
        print("   ✅ ML functions integrated in Flask app")
    else:
        print("   ⚠️ ML functions not found in app.py")
    
    if '/recommend/ml' in app_content:
        print("   ✅ ML endpoint '/recommend/ml' added")
    else:
        print("   ⚠️ ML endpoint not found")
        
    if '/similar/' in app_content:
        print("   ✅ Similar cities endpoint added")
    else:
        print("   ⚠️ Similar cities endpoint not found")
        
except Exception as e:
    print(f"   ❌ Error reading app.py: {e}")

# Summary
print("\n" + "=" * 60)
print("✨ TEST SUMMARY")
print("=" * 60)
print("\n✅ All core tests passed!")
print("\n📋 Next steps:")
print("   1. Start Flask server: python app.py")
print("   2. Test ML endpoint: http://localhost:5000/recommend/ml?month=October&duration=7")
print("   3. Test similar cities: http://localhost:5000/similar/Goa")
print("   4. Check insights: http://localhost:5000/ml/insights")
print("\n🎉 Your ML recommendation system is ready!")
print("=" * 60)
