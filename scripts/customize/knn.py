import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler



# load the datasets
spotify_data = pd.read_csv('tmp/universal_top_spotify_songs.csv')
mental_health_data = pd.read_csv('tmp/merged_attributes_and_mental_health.csv')

# select common features for merging
common_features = ['danceability', 'energy', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

# drop rows with missing values in the common features
spotify_data = spotify_data.dropna(subset=common_features + ['country'])
mental_health_data = mental_health_data.dropna(subset=common_features)

# normalize the features
scaler = StandardScaler()
spotify_data[common_features] = scaler.fit_transform(spotify_data[common_features])
mental_health_data[common_features] = scaler.transform(mental_health_data[common_features])

# train a k-NN model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(spotify_data[common_features], spotify_data['country'])

# predict the country for the mental health dataset
mental_health_data['predicted_country'] = knn.predict(mental_health_data[common_features])

# save the updated dataset
mental_health_data.to_csv('tmp/merged_attributes_and_mental_health_with_country.csv', index=False)
print("updated dataset saved with predicted country column.")
