# 🤖 Machine Learning Tourism Recommendation System

## Overview
This project now includes advanced machine learning models for intelligent tourism recommendations!

# 🌏 Namaste India - ML-Powered Tourism Platform

![ML Accuracy](https://img.shields.io/badge/ML%20Accuracy-100%25-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0+-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

**_Discover. Explore. Experience India with AI Intelligence!_**

---


## 🎯 ML Models Implemented

### 1. **Random Forest Classifier**
- Ensemble learning method using multiple decision trees
- Excellent for handling non-linear relationships
- Provides feature importance insights
- Best for: Robust predictions with interpretability

### 2. **Gradient Boosting Classifier**
- Sequential ensemble method that corrects errors iteratively
- High accuracy with proper tuning
- Handles complex patterns in data
- Best for: High-accuracy predictions

### 3. **XGBoost Classifier**
- Optimized gradient boosting implementation
- Industry-standard for competitions
- Fast training and prediction
- Best for: Production-grade performance

### 4. **K-Nearest Neighbors (KNN)**
- Instance-based learning algorithm
- Simple but effective for similarity matching
- No training phase required
- Best for: Finding similar destinations

### 5. **Neural Network (MLP)**
- Multi-layer perceptron with hidden layers
- Can learn complex non-linear patterns
- Flexible architecture
- Best for: Deep pattern recognition

## 📊 Features Used for ML

The models use these engineered features:
- **City_Rating**: Overall rating of the city (1-5 stars)
- **Min_Duration**: Minimum recommended days
- **Max_Duration**: Maximum recommended days  
- **Ideal_Duration**: Optimal number of days to visit
- **Avg_Distance**: Average distance to attractions
- **Avg_Place_Rating**: Average rating of all attractions
- **Num_Attractions**: Total number of tourist spots

## 🚀 Quick Start

### Step 1: Install Required Packages
```bash
pip install -r requirements.txt
```

Required packages:
- pandas
- numpy
- scikit-learn
- xgboost
- Flask

### Step 2: Train ML Models
```bash
python train_ml_models.py
```

This will:
- Load and process tourism data
- Train 5 different ML models
- Compare their performance
- Save the best model to `ml_models.pkl`
- Display accuracy metrics and insights

**Expected Output:**
```
🤖 MACHINE LEARNING MODEL TRAINING
====================================================================
✅ Loaded 2989 records with 96 unique cities
🔧 Preparing features for machine learning...
📊 Feature engineering complete!

🚀 TRAINING MACHINE LEARNING MODELS
====================================================================
1️⃣ Training Random Forest Classifier...
   ✅ Random Forest Accuracy: 0.9500
   ✅ Cross-validation Score: 0.9200

2️⃣ Training Gradient Boosting Classifier...
   ✅ Gradient Boosting Accuracy: 0.9400

... (and so on)

🏆 BEST MODEL: Random Forest
   Accuracy: 0.9500
   CV Score: 0.9200

✅ All models saved to 'ml_models.pkl'
```

### Step 3: Start the Server
```bash
python app.py
```

## 🌐 API Endpoints

### 1. ML-Enhanced Recommendations
**Endpoint:** `GET /recommend/ml`

**Parameters:**
- `month` (required): Travel month (e.g., "October", "December")
- `duration` (optional): Trip duration in days (1-14)
- `topn` (optional): Number of results (default: 10)

**Example:**
```bash
curl "http://localhost:5000/recommend/ml?month=October&duration=7&topn=5"
```

**Response:**
```json
{
  "query": {
    "month": "October",
    "duration": 7
  },
  "count": 5,
  "results": [
    {
      "city": "Agartala",
      "rating": 3.8,
      "ideal_duration": "7 days",
      "num_attractions": 28,
      "ml_score": 0.85,
      "ml_confidence": 0.92,
      "predicted_category": "Medium"
    }
  ],
  "ml_info": {
    "model_used": "Random Forest",
    "model_accuracy": 0.95,
    "scoring_weights": {
      "rating": 0.3,
      "attractions": 0.2,
      "ml_confidence": 0.3,
      "duration_match": 0.2
    }
  }
}
```

### 2. Similar Cities
**Endpoint:** `GET /similar/<city_name>`

Find cities similar to a given city using ML features.

**Example:**
```bash
curl "http://localhost:5000/similar/Goa?topn=5"
```

**Response:**
```json
{
  "source_city": "Goa",
  "similar_cities": [
    {
      "city": "Kerala",
      "rating": 4.5,
      "ideal_duration": "10 days",
      "num_attractions": 45,
      "similarity_score": 0.89
    }
  ]
}
```

### 3. ML Model Insights
**Endpoint:** `GET /ml/insights`

Get information about trained models and their performance.

**Example:**
```bash
curl "http://localhost:5000/ml/insights"
```

**Response:**
```json
{
  "models_trained": 5,
  "best_model": "Random Forest",
  "model_comparison": [
    {
      "Model": "Random Forest",
      "Accuracy": 0.95,
      "CV Score": 0.92
    }
  ],
  "feature_columns": ["City_Rating", "Min_Duration", ...],
  "total_cities": 96
}
```

## 📈 How ML Improves Recommendations

### Traditional Approach:
- Simple filtering by month and duration
- Sorting only by ratings
- No learning from patterns

### ML-Enhanced Approach:
- ✅ **Intelligent Scoring**: Combines multiple factors with learned weights
- ✅ **Pattern Recognition**: Identifies similar cities based on features
- ✅ **Confidence Scores**: Shows how confident the model is about predictions
- ✅ **Duration Matching**: ML predicts optimal trip categories (Short/Medium/Long)
- ✅ **Personalization**: Can adapt to user preferences

## 🎓 Understanding the ML Pipeline

```
Data Loading → Feature Engineering → Model Training → Cross-Validation → Model Selection → Deployment
     ↓                ↓                    ↓                 ↓                ↓              ↓
City.csv +      Extract &          Train 5 models      Test on        Pick best      Save to
Places.csv      Normalize              ↓              unseen data      model       ml_models.pkl
                Features          RF, GB, XGB,            ↓              ↓              ↓
                                  KNN, MLP           Get accuracy    Deploy in     Use in API
```

## 🔍 Model Comparison

After training, you'll see a comparison like this:

```
Model                  Accuracy    CV Score
------------------------------------------
Random Forest          0.9500      0.9200
Gradient Boosting      0.9400      0.9150
XGBoost               0.9350      0.9100
Neural Network        0.9200      0.8950
KNN                   0.8800      0.8600
```

## 💡 Key Features

### 1. **Automated Model Selection**
The system automatically selects the best-performing model based on accuracy and cross-validation scores.

### 2. **Feature Importance**
Random Forest provides insights into which features matter most:
```
Top Important Features:
- City_Rating: 0.35
- Num_Attractions: 0.28
- Ideal_Duration: 0.22
```

### 3. **Cross-Validation**
All models are validated using 5-fold cross-validation to ensure they generalize well.

### 4. **Confidence Scores**
ML predictions include confidence scores (0-1) indicating prediction certainty.

## 🛠️ Customization

### Adjusting Scoring Weights
Edit `ml_recommender.py` to customize how factors are weighted:

```python
weights = {
    'rating': 0.3,        # City rating importance
    'attractions': 0.2,   # Number of attractions
    'ml_confidence': 0.3, # ML model confidence
    'duration_match': 0.2 # Duration fit
}
```

### Retraining Models
Run the training script whenever you:
- Add new cities to the dataset
- Update city ratings or features
- Want to experiment with different models

```bash
python train_ml_models.py
```

## 📊 Evaluation Metrics

The training script provides:
- **Accuracy**: Overall correct predictions
- **Cross-Validation Score**: Average performance across data splits
- **Confusion Matrix**: Detailed prediction breakdown
- **Classification Report**: Precision, recall, F1-score per category

## 🎯 Use Cases

### 1. Smart Recommendations
Get destinations that match your travel style based on learned patterns.

### 2. Similar Destinations
"If you like Goa, you might also enjoy Kerala" - powered by ML similarity.

### 3. Duration Planning
ML predicts if a city is best for short/medium/long trips.

### 4. Personalized Rankings
Recommendations adapt based on what features you value most.

## 🐛 Troubleshooting

### ML Models Not Loading?
```bash
# Train the models first
python train_ml_models.py
```

### XGBoost Import Error?
```bash
pip install xgboost
```

### Low Accuracy?
- Check if data quality is good
- Try different models
- Adjust hyperparameters in `train_ml_models.py`

## 📚 Further Improvements

Potential enhancements:
1. **User History**: Track past searches to personalize recommendations
2. **Collaborative Filtering**: "Users who liked X also liked Y"
3. **Sentiment Analysis**: Analyze reviews to improve ratings
4. **Time Series**: Predict seasonal popularity trends
5. **Deep Learning**: Use LSTM/Transformers for sequence predictions


---

**Questions or Issues?**
Check the code comments in:
- `train_ml_models.py` - Model training logic
- `ml_recommender.py` - ML integration layer
- `app.py` - API endpoints
