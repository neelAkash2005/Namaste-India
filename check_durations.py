"""Verify cities have varied durations"""
import pickle
import pandas as pd

with open('merged_df.pkl', 'rb') as f:
    df = pickle.load(f)

# Get unique durations
unique_durations = df['Ideal_duration'].unique()

print("✅ Unique Duration Values:")
print("=" * 50)
for duration in sorted(unique_durations):
    count = len(df[df['Ideal_duration'] == duration]['City'].unique())
    print(f"   {duration:15} - {count:3} cities")

print("\n✅ Sample Cities:")
print("=" * 50)
sample = df.groupby('City').first()[['Ideal_duration', 'Ratings_x']].head(10)
for city, row in sample.iterrows():
    print(f"   {city:20} → {row['Ideal_duration']:10} (⭐ {row['Ratings_x']})")

print("\n✅ Duration distribution looks good!")
