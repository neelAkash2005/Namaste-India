"""
ML-Enhanced Recommendation System
Integrates trained ML models with the existing recommendation system
"""

import pickle
import pandas as pd
import numpy as np
from flask import jsonify

# Load ML models
try:
    with open('ml_models.pkl', 'rb') as f:
        ml_package = pickle.load(f)
    
    ML_MODELS_AVAILABLE = True
    print("✅ ML Models loaded successfully!")
    print(f"   Best model: {ml_package['best_model_name']}")
    print(f"   Accuracy: {ml_package['models'][ml_package['best_model_name']]['accuracy']:.4f}")
except FileNotFoundError:
    ML_MODELS_AVAILABLE = False
    print("⚠️ ML models not found. Run train_ml_models.py first.")
except Exception as e:
    ML_MODELS_AVAILABLE = False
    print(f"⚠️ Error loading ML models: {e}")


def get_ml_enhanced_recommendations(month, duration=None, topn=10, user_preferences=None):
    """
    Get recommendations using ML models for intelligent ranking
    
    Parameters:
    - month: Travel month
    - duration: Trip duration in days
    - topn: Number of results to return
    - user_preferences: Dict with user preferences like {'prefer_rating': True, 'prefer_attractions': False}
    
    Returns:
    - Dictionary with recommendations and ML insights
    """
    
    if not ML_MODELS_AVAILABLE:
        return {
            'error': 'ML models not available. Please train models first.',
            'results': []
        }
    
    # Load the main data
    with open('merged_df.pkl', 'rb') as f:
        merged_df = pickle.load(f)
    
    # Get city features from ML package
    city_features = ml_package['city_features'].copy()
    scaler = ml_package['scaler']
    best_model = ml_package['models'][ml_package['best_model_name']]['model']
    le_duration = ml_package['label_encoder_duration']
    feature_columns = ml_package['feature_columns']
    
    # Normalize month
    month = month.capitalize()
    
    # Validate month
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                    'july', 'august', 'september', 'october', 'november', 'december']
    month_lower = month.lower()
    is_valid_month = any(month_lower[:3] in valid_month or valid_month[:3] in month_lower 
                         for valid_month in valid_months)
    
    if not is_valid_month:
        return {
            'query': {'month': month},
            'count': 0,
            'results': [],
            'error': f'Invalid month: "{month}". Please enter a valid month name.'
        }
    
    # Filter cities based on month (all cities available year-round in this dataset)
    available_cities = city_features['City'].tolist()
    
    # Filter by duration if provided
    if duration is not None:
        duration = int(duration)
        # Use ML model to find cities with matching duration profiles
        city_features_filtered = city_features[
            (city_features['Min_Duration'] <= duration) & 
            (city_features['Max_Duration'] >= duration)
        ].copy()
    else:
        city_features_filtered = city_features.copy()
    
    if len(city_features_filtered) == 0:
        return {
            'query': {'month': month, 'duration': duration},
            'count': 0,
            'results': [],
            'message': 'No cities found matching your criteria.'
        }
    
    # ========================================
    # ML-ENHANCED SCORING
    # ========================================
    
    # Prepare features for ML prediction
    X_features = city_features_filtered[feature_columns].values
    X_scaled = scaler.transform(X_features)
    
    # Get ML predictions and probabilities
    ml_predictions = best_model.predict(X_scaled)
    
    # For probabilistic models, get confidence scores
    if hasattr(best_model, 'predict_proba'):
        ml_confidence = best_model.predict_proba(X_scaled).max(axis=1)
    else:
        ml_confidence = np.ones(len(X_scaled))  # Default confidence = 1
    
    # Calculate composite score
    city_features_filtered['ML_Confidence'] = ml_confidence
    
    # Scoring weights (can be customized based on user preferences)
    weights = {
        'rating': 0.3,
        'attractions': 0.2,
        'ml_confidence': 0.3,
        'duration_match': 0.2
    }
    
    # Apply user preferences if provided
    if user_preferences:
        if user_preferences.get('prefer_rating'):
            weights['rating'] = 0.4
            weights['ml_confidence'] = 0.25
        if user_preferences.get('prefer_attractions'):
            weights['attractions'] = 0.3
            weights['rating'] = 0.25
    
    # Normalize scores to 0-1 range
    city_features_filtered['Rating_Score'] = city_features_filtered['City_Rating'] / 5.0
    city_features_filtered['Attraction_Score'] = (
        city_features_filtered['Num_Attractions'] / 
        city_features_filtered['Num_Attractions'].max()
    )
    
    # Duration match score
    if duration is not None:
        city_features_filtered['Duration_Match_Score'] = city_features_filtered.apply(
            lambda row: 1.0 - abs(row['Ideal_Duration'] - duration) / 14.0,
            axis=1
        )
    else:
        city_features_filtered['Duration_Match_Score'] = 0.5  # Neutral score
    
    # Calculate final ML-enhanced score
    city_features_filtered['ML_Score'] = (
        weights['rating'] * city_features_filtered['Rating_Score'] +
        weights['attractions'] * city_features_filtered['Attraction_Score'] +
        weights['ml_confidence'] * city_features_filtered['ML_Confidence'] +
        weights['duration_match'] * city_features_filtered['Duration_Match_Score']
    )
    
    # Sort by ML score
    city_features_filtered = city_features_filtered.sort_values('ML_Score', ascending=False)
    
    # Reset index to avoid indexing issues
    city_features_filtered = city_features_filtered.reset_index(drop=True)
    
    # Prepare results
    results = []
    for idx, row in city_features_filtered.head(topn).iterrows():
        city_name = row['City']
        
        # Get city description from merged_df
        city_info = merged_df[merged_df['City'] == city_name].iloc[0]
        
        # Get original index for ml_predictions
        original_idx = city_features_filtered.index.get_loc(idx)
        
        results.append({
            'city': city_name,
            'rating': float(row['City_Rating']),
            'ideal_duration': f"{int(row['Ideal_Duration'])} days",
            'best_time': 'Year-round (All months)',
            'description': str(city_info.get('City_desc', ''))[:200] + '...',
            'num_attractions': int(row['Num_Attractions']),
            'ml_score': float(row['ML_Score']),
            'ml_confidence': float(row['ML_Confidence']),
            'predicted_category': le_duration.inverse_transform([ml_predictions[original_idx]])[0]
        })
    
    return {
        'query': {'month': month, 'duration': duration},
        'count': len(results),
        'results': results,
        'ml_info': {
            'model_used': ml_package['best_model_name'],
            'model_accuracy': float(ml_package['models'][ml_package['best_model_name']]['accuracy']),
            'scoring_weights': weights
        }
    }


def get_similar_cities_ml(city_name, topn=5):
    """
    Find similar cities using ML features
    """
    
    if not ML_MODELS_AVAILABLE:
        return {'error': 'ML models not available'}
    
    city_features = ml_package['city_features']
    feature_columns = ml_package['feature_columns']
    scaler = ml_package['scaler']
    
    # Find the target city
    target_city = city_features[city_features['City'] == city_name]
    
    if len(target_city) == 0:
        return {'error': f'City "{city_name}" not found'}
    
    # Get features of target city
    target_features = target_city[feature_columns].values
    target_scaled = scaler.transform(target_features)
    
    # Calculate similarity with all other cities (using Euclidean distance)
    all_features = city_features[feature_columns].values
    all_scaled = scaler.transform(all_features)
    
    # Compute distances
    distances = np.linalg.norm(all_scaled - target_scaled, axis=1)
    city_features['Similarity_Distance'] = distances
    
    # Sort by similarity (smaller distance = more similar)
    similar_cities = city_features[city_features['City'] != city_name].sort_values(
        'Similarity_Distance'
    ).head(topn)
    
    results = []
    for idx, row in similar_cities.iterrows():
        results.append({
            'city': row['City'],
            'rating': float(row['City_Rating']),
            'ideal_duration': f"{int(row['Ideal_Duration'])} days",
            'num_attractions': int(row['Num_Attractions']),
            'similarity_score': float(1 / (1 + row['Similarity_Distance']))  # Convert distance to score
        })
    
    return {
        'source_city': city_name,
        'similar_cities': results
    }


def get_model_insights():
    """
    Return ML model performance metrics and insights
    """
    
    if not ML_MODELS_AVAILABLE:
        return {'error': 'ML models not available'}
    
    comparison_df = ml_package['comparison_df']
    
    return {
        'models_trained': len(ml_package['models']),
        'best_model': ml_package['best_model_name'],
        'model_comparison': comparison_df.to_dict('records'),
        'feature_columns': ml_package['feature_columns'],
        'total_cities': len(ml_package['city_features'])
    }
