import pandas as pd
from scipy.spatial.distance import cdist

mental_health_df = pd.read_csv('../assets/datasets/all_platforms_merged.csv')
spotify_df = pd.read_csv('../assets/datasets/universal_top_spotify_songs.csv')

# === Step 1: Clean & Aggregate Spotify Data ===
spotify_df = spotify_df[['country', 'tempo', 'danceability', 'energy', 'valence']]
spotify_df = spotify_df.dropna(subset=['country', 'tempo'])

# Aggregate features per country
country_agg = spotify_df.groupby('country').agg({
    'tempo': 'mean',
    'danceability': 'mean',
    'energy': 'mean',
    'valence': 'mean'
}).reset_index()

# Rename columns for consistency
country_agg.columns = ['country', 'bpm', 'danceability', 'energy', 'valence']

# === Step 2: Prepare Mental Health Data ===
mental_health_df = mental_health_df.rename(columns={'BPM': 'bpm'})
mental_health_df['bpm'] = pd.to_numeric(mental_health_df['bpm'], errors='coerce')
mental_health_df = mental_health_df.dropna(subset=['bpm'])

# === Step 3: Match Users to Closest Country ===
# Create feature vectors
resp_vec = mental_health_df[['bpm', 'danceability', 'energy', 'valence']].values
country_vec = country_agg[['bpm', 'danceability', 'energy', 'valence']].values

# Calculate distances
distances = cdist(resp_vec, country_vec, metric='euclidean')
closest_country_idx = distances.argmin(axis=1)

# Assign best-match country to each respondent
mental_health_df['country'] = country_agg.loc[closest_country_idx, 'country'].values

# === Step 4: Save the result ===
mental_health_df.to_csv('mental_health_with_country.csv', index=False)
print("Merged dataset saved as 'mental_health_with_country.csv'")


# Check how many unique countries
unique_countries = mental_health_df['country'].nunique()
print(f"Number of unique countries in the result: {unique_countries}\n")

# Count how many rows (users) per country
country_counts = mental_health_df['country'].value_counts()

print("Number of respondents matched to each country:\n")
print(country_counts)

