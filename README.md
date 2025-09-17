# Build model

This repository contains a small script to build and pickle the city recommender artifacts.

Usage (from the project root where `City.csv` and `Places.csv` live):

1. Create a Python environment and install requirements:

   pip install -r requirements.txt

2. Run the builder:

   python build_model.py

This writes `model.pkl` containing a dict with keys: `vectorizer`, `sim_matrix`, `city_df`, `city_col`, `dur_col`, `time_col`, `city_to_idx`.

Load it with `pickle.load(open('model.pkl','rb'))` for deployment.
