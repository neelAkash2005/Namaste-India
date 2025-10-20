"""
Machine Learning Models for Tourism Recommendation System
This script trains multiple ML models including:
- Random Forest Classifier
- Gradient Boosting Classifier
- XGBoost Classifier
- K-Nearest Neighbors
- Neural Network (MLPClassifier)
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️ XGBoost not installed. Install with: pip install xgboost")

print("=" * 60)
print("🤖 MACHINE LEARNING MODEL TRAINING")
print("=" * 60)

# Load the data
print("\n📂 Loading data...")
with open('merged_df.pkl', 'rb') as f:
    merged_df = pickle.load(f)

print(f"✅ Loaded {len(merged_df)} records with {merged_df['City'].nunique()} unique cities")

# Prepare features for ML
print("\n🔧 Preparing features for machine learning...")

# Clean Distance column - extract numeric values
def extract_distance(dist_str):
    """Extract numeric distance from string like '5 km from city center'"""
    if pd.isna(dist_str) or dist_str == '':
        return 0
    try:
        # Extract first number from string
        import re
        numbers = re.findall(r'\d+', str(dist_str))
        if numbers:
            return float(numbers[0])
        return 0
    except:
        return 0

merged_df['Distance_Numeric'] = merged_df['Distance'].apply(extract_distance)

# Clean ratings - ensure numeric
def clean_rating(rating):
    try:
        return float(rating)
    except:
        return 0.0

merged_df['Ratings_y_clean'] = merged_df['Ratings_y'].apply(clean_rating)
merged_df['Ratings_x_clean'] = merged_df['Ratings_x'].apply(clean_rating)

# Get city-level aggregated data
city_features = merged_df.groupby('City').agg({
    'Ratings_x_clean': 'first',
    'Min_duration': 'first',
    'Max_duration': 'first',
    'Distance_Numeric': 'mean',
    'Ratings_y_clean': 'mean',
    'Place': 'count'  # Number of attractions
}).reset_index()

city_features.columns = ['City', 'City_Rating', 'Min_Duration', 'Max_Duration', 
                         'Avg_Distance', 'Avg_Place_Rating', 'Num_Attractions']

# Calculate ideal duration as midpoint
city_features['Ideal_Duration'] = ((city_features['Min_Duration'] + city_features['Max_Duration']) / 2).astype(int)

# Create duration categories for classification (Short, Medium, Long trips)
def categorize_duration(days):
    if days <= 3:
        return 'Short'
    elif days <= 7:
        return 'Medium'
    else:
        return 'Long'

city_features['Duration_Category'] = city_features['Ideal_Duration'].apply(categorize_duration)

# Create rating categories (Excellent, Good, Average)
def categorize_rating(rating):
    if rating >= 4.5:
        return 'Excellent'
    elif rating >= 4.0:
        return 'Good'
    else:
        return 'Average'

city_features['Rating_Category'] = city_features['City_Rating'].apply(categorize_rating)

print(f"📊 Feature engineering complete!")
print(f"   - {len(city_features)} cities")
print(f"   - Duration categories: {city_features['Duration_Category'].value_counts().to_dict()}")
print(f"   - Rating categories: {city_features['Rating_Category'].value_counts().to_dict()}")

# Prepare features (X) and target (y) for classification
print("\n🎯 Preparing training data...")

# Features for prediction
feature_columns = ['City_Rating', 'Min_Duration', 'Max_Duration', 'Ideal_Duration',
                   'Avg_Distance', 'Avg_Place_Rating', 'Num_Attractions']

X = city_features[feature_columns].values
y_duration = city_features['Duration_Category'].values
y_rating = city_features['Rating_Category'].values

# Encode target variables
le_duration = LabelEncoder()
le_rating = LabelEncoder()
y_duration_encoded = le_duration.fit_transform(y_duration)
y_rating_encoded = le_rating.fit_transform(y_rating)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_dur_train, y_dur_test = train_test_split(
    X_scaled, y_duration_encoded, test_size=0.2, random_state=42
)
_, _, y_rat_train, y_rat_test = train_test_split(
    X_scaled, y_rating_encoded, test_size=0.2, random_state=42
)

print(f"✅ Training set: {len(X_train)} samples")
print(f"✅ Test set: {len(X_test)} samples")

# ========================================
# TRAIN MULTIPLE ML MODELS
# ========================================

models_results = {}

print("\n" + "=" * 60)
print("🚀 TRAINING MACHINE LEARNING MODELS")
print("=" * 60)

# 1. Random Forest Classifier
print("\n1️⃣ Training Random Forest Classifier...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_dur_train)
rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_dur_test, rf_pred)
rf_cv_score = cross_val_score(rf_model, X_scaled, y_duration_encoded, cv=5).mean()

models_results['Random Forest'] = {
    'model': rf_model,
    'accuracy': rf_accuracy,
    'cv_score': rf_cv_score
}

print(f"   ✅ Random Forest Accuracy: {rf_accuracy:.4f}")
print(f"   ✅ Cross-validation Score: {rf_cv_score:.4f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)
print(f"   📊 Top 3 Important Features:")
for idx, row in feature_importance.head(3).iterrows():
    print(f"      - {row['feature']}: {row['importance']:.4f}")

# 2. Gradient Boosting Classifier
print("\n2️⃣ Training Gradient Boosting Classifier...")
gb_model = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
gb_model.fit(X_train, y_dur_train)
gb_pred = gb_model.predict(X_test)
gb_accuracy = accuracy_score(y_dur_test, gb_pred)
gb_cv_score = cross_val_score(gb_model, X_scaled, y_duration_encoded, cv=5).mean()

models_results['Gradient Boosting'] = {
    'model': gb_model,
    'accuracy': gb_accuracy,
    'cv_score': gb_cv_score
}

print(f"   ✅ Gradient Boosting Accuracy: {gb_accuracy:.4f}")
print(f"   ✅ Cross-validation Score: {gb_cv_score:.4f}")

# 3. XGBoost Classifier (if available)
if XGBOOST_AVAILABLE:
    print("\n3️⃣ Training XGBoost Classifier...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    xgb_model.fit(X_train, y_dur_train)
    xgb_pred = xgb_model.predict(X_test)
    xgb_accuracy = accuracy_score(y_dur_test, xgb_pred)
    xgb_cv_score = cross_val_score(xgb_model, X_scaled, y_duration_encoded, cv=5).mean()
    
    models_results['XGBoost'] = {
        'model': xgb_model,
        'accuracy': xgb_accuracy,
        'cv_score': xgb_cv_score
    }
    
    print(f"   ✅ XGBoost Accuracy: {xgb_accuracy:.4f}")
    print(f"   ✅ Cross-validation Score: {xgb_cv_score:.4f}")

# 4. K-Nearest Neighbors
print("\n4️⃣ Training K-Nearest Neighbors...")
knn_model = KNeighborsClassifier(
    n_neighbors=5,
    weights='distance',
    metric='euclidean'
)
knn_model.fit(X_train, y_dur_train)
knn_pred = knn_model.predict(X_test)
knn_accuracy = accuracy_score(y_dur_test, knn_pred)
knn_cv_score = cross_val_score(knn_model, X_scaled, y_duration_encoded, cv=5).mean()

models_results['KNN'] = {
    'model': knn_model,
    'accuracy': knn_accuracy,
    'cv_score': knn_cv_score
}

print(f"   ✅ KNN Accuracy: {knn_accuracy:.4f}")
print(f"   ✅ Cross-validation Score: {knn_cv_score:.4f}")

# 5. Neural Network (MLP)
print("\n5️⃣ Training Neural Network (MLP)...")
mlp_model = MLPClassifier(
    hidden_layer_sizes=(100, 50),
    activation='relu',
    solver='adam',
    max_iter=500,
    random_state=42
)
mlp_model.fit(X_train, y_dur_train)
mlp_pred = mlp_model.predict(X_test)
mlp_accuracy = accuracy_score(y_dur_test, mlp_pred)
mlp_cv_score = cross_val_score(mlp_model, X_scaled, y_duration_encoded, cv=5).mean()

models_results['Neural Network'] = {
    'model': mlp_model,
    'accuracy': mlp_accuracy,
    'cv_score': mlp_cv_score
}

print(f"   ✅ Neural Network Accuracy: {mlp_accuracy:.4f}")
print(f"   ✅ Cross-validation Score: {mlp_cv_score:.4f}")

# ========================================
# MODEL COMPARISON
# ========================================

print("\n" + "=" * 60)
print("📊 MODEL COMPARISON RESULTS")
print("=" * 60)

comparison_df = pd.DataFrame([
    {
        'Model': name,
        'Accuracy': results['accuracy'],
        'CV Score': results['cv_score']
    }
    for name, results in models_results.items()
]).sort_values('Accuracy', ascending=False)

print("\n" + comparison_df.to_string(index=False))

# Find best model
best_model_name = comparison_df.iloc[0]['Model']
best_model = models_results[best_model_name]['model']

print(f"\n🏆 BEST MODEL: {best_model_name}")
print(f"   Accuracy: {models_results[best_model_name]['accuracy']:.4f}")
print(f"   CV Score: {models_results[best_model_name]['cv_score']:.4f}")

# ========================================
# SAVE ALL MODELS
# ========================================

print("\n💾 Saving models and preprocessors...")

ml_package = {
    'models': models_results,
    'best_model_name': best_model_name,
    'scaler': scaler,
    'label_encoder_duration': le_duration,
    'label_encoder_rating': le_rating,
    'feature_columns': feature_columns,
    'city_features': city_features,
    'comparison_df': comparison_df
}

with open('ml_models.pkl', 'wb') as f:
    pickle.dump(ml_package, f)

print("✅ All models saved to 'ml_models.pkl'")

# ========================================
# DETAILED EVALUATION OF BEST MODEL
# ========================================

print("\n" + "=" * 60)
print(f"🔍 DETAILED EVALUATION - {best_model_name}")
print("=" * 60)

# Confusion Matrix
cm = confusion_matrix(y_dur_test, 
                     best_model.predict(X_test))
print("\n📊 Confusion Matrix:")
print(cm)

# Classification Report
print("\n📋 Classification Report:")
print(classification_report(y_dur_test, 
                          best_model.predict(X_test),
                          target_names=le_duration.classes_))

# ========================================
# PREDICTION EXAMPLES
# ========================================

print("\n" + "=" * 60)
print("🎯 SAMPLE PREDICTIONS")
print("=" * 60)

# Select a few cities for demonstration
sample_cities = city_features.sample(5)

for idx, city in sample_cities.iterrows():
    city_name = city['City']
    features = city[feature_columns].values.reshape(1, -1)
    features_scaled = scaler.transform(features)
    
    # Predict using best model
    prediction = best_model.predict(features_scaled)[0]
    predicted_category = le_duration.inverse_transform([prediction])[0]
    actual_category = city['Duration_Category']
    
    print(f"\n🏙️ {city_name}")
    print(f"   Rating: ⭐ {city['City_Rating']:.1f}")
    print(f"   Attractions: {city['Num_Attractions']}")
    print(f"   Actual Duration: {actual_category}")
    print(f"   Predicted Duration: {predicted_category}")
    print(f"   {'✅ Correct!' if predicted_category == actual_category else '❌ Wrong'}")

print("\n" + "=" * 60)
print("✨ TRAINING COMPLETE!")
print("=" * 60)
print(f"\n✅ Trained {len(models_results)} machine learning models")
print(f"✅ Best model: {best_model_name} (Accuracy: {models_results[best_model_name]['accuracy']:.4f})")
print(f"✅ Models saved to: ml_models.pkl")
print(f"\n💡 You can now use these models for intelligent recommendations!")
print("=" * 60)
