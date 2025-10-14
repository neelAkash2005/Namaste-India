"""
Script to create the merged_df.pkl file for the advanced recommendation system.
This version makes ALL cities available for ALL months and durations 1-14 days.
"""
import pandas as pd
import pickle
import numpy as np
import re

print(" Loading CSV files...")
df1 = pd.read_csv('City.csv')
df2 = pd.read_csv('Places.csv')

print(f"   City.csv: {len(df1)} rows")
print(f"   Places.csv: {len(df2)} rows")

# Merge the dataframes
print(" Merging dataframes...")
merged_df = pd.merge(df1, df2, on='City')
print(f"   Merged: {len(merged_df)} rows")

# Make ALL cities available for ALL months (year-round tourism)
print(" Setting all cities available for all months...")
all_months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']

merged_df['Months'] = merged_df.apply(lambda x: all_months, axis=1)

# Update Best_time_to_visit to show "Year-round"
merged_df['Best_time_to_visit'] = 'Year-round (All months)'

# Expand duration ranges to support 1-14 days for ALL cities
print(" Setting varied duration ranges (1-14 days) for all cities...")

# Get list of all unique cities
all_cities = merged_df['City'].unique()
city_count = len(all_cities)

# Create duration assignments - evenly distributed across 1-14 days
duration_map = {}
for idx, city in enumerate(all_cities):
    # Distribute evenly: cycle through 1-14
    duration = (idx % 14) + 1
    duration_map[city] = duration

def assign_duration(city_name):
    """
    Assign specific duration to each city with a small range.
    For example, if city ideal is 7 days, allow 5-9 days (±2 days flexibility)
    """
    duration = duration_map.get(city_name, 7)  # Default 7 if not found
    
    # Add ±2 days flexibility (but stay within 1-14 bounds)
    min_dur = max(1, duration - 2)
    max_dur = min(14, duration + 2)
    
    return (min_dur, max_dur, f"{duration} days")

# Apply duration transformation
duration_results = merged_df['City'].apply(assign_duration)

merged_df['Min_duration'] = duration_results.apply(lambda x: x[0])
merged_df['Max_duration'] = duration_results.apply(lambda x: x[1])
merged_df['Ideal_duration'] = duration_results.apply(lambda x: x[2])

# Clean Place column (remove numbering)
print(" Cleaning place names...")
merged_df["Place_clean"] = merged_df["Place"].apply(lambda x: re.sub(r'^\d+\.\s*', '', str(x)))

# Convert descriptions to plain text
print(" Converting descriptions...")
merged_df["City_desc"] = merged_df["City_desc"].apply(lambda x: str(x).strip("[]'"))
merged_df["Place_desc"] = merged_df["Place_desc"].apply(lambda x: str(x).strip("[]'"))

# Fill NaN values
merged_df = merged_df.fillna("")

# Save to pickle
print(" Saving to merged_df.pkl...")
with open('merged_df.pkl', 'wb') as f:
    pickle.dump(merged_df, f)

print(f" Successfully created merged_df.pkl with {len(merged_df)} records!")
print(f"   Columns: {list(merged_df.columns)}")
print(f"\n Sample data:")
print(f"   Cities: {merged_df['City'].nunique()} unique cities")
print(f"   Places: {len(merged_df)} total places")
print(f"\n Top 5 cities by rating:")
top_cities = merged_df.groupby('City')['Ratings_x'].first().sort_values(ascending=False).head()
for city, rating in top_cities.items():
    print(f"   {city}: {rating}")
print("\n Recommendation system is ready!")
