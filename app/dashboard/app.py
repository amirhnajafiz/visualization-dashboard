import os
from flask import Flask, jsonify, render_template, request
import pandas as pd
import geojson
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from livereload import Server
import prince
import copy
import pycountry


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Load data
DATA_PATH = os.path.join("data", "dataset.csv")
GEO_JSON_PATH = os.path.join("data", "countries.geo.json")


# Read and preprocess
raw_data = pd.read_csv(DATA_PATH)
raw_data = raw_data.dropna(subset=['country'])
raw_data.fillna(raw_data.mean(numeric_only=True), inplace=True)
iso2_to_iso3 = {country.alpha_2: country.alpha_3 for country in pycountry.countries}
raw_data['country'] = raw_data['country'].map(iso2_to_iso3)

# Define features for clustering and regression
cluster_features = ['bpm', 'danceability', 'energy', 'valence', 'anxiety', 'depression', 'insomnia', 'ocd']
audio_features = ['bpm', 'danceability', 'energy', 'valence']

# Standardize
scaler = StandardScaler()
scaled = scaler.fit_transform(raw_data[cluster_features])

# PCA and KMeans
pca = PCA(n_components=2)
raw_data[['pca1', 'pca2']] = pca.fit_transform(scaler.transform(raw_data[cluster_features]))
kmeans = KMeans(n_clusters=5, random_state=42).fit(raw_data[['pca1', 'pca2']])
raw_data['cluster'] = kmeans.labels_

# Train Regressor
kreg = KNeighborsRegressor(n_neighbors=5).fit(raw_data[audio_features], raw_data['anxiety'])

# Group for choropleth
country_summary = raw_data.groupby("country").agg({
    'anxiety': 'mean', 'depression': 'mean', 'insomnia': 'mean', 'ocd': 'mean',
    'valence': 'mean', 'danceability': 'mean', 'energy': 'mean', 'bpm': 'mean'
}).reset_index()

# Load geojson
with open(GEO_JSON_PATH) as f:
    gj = geojson.load(f)
    gj['features'] = [f for f in gj['features'] if f['properties']['name'] != 'Antarctica']
    for f in gj['features']:
        iso = f['id']
        if iso in country_summary['country'].values:
            row = country_summary[country_summary['country'] == iso].iloc[0]
            for col in country_summary.columns[1:]:
                f[col] = row[col]

@app.route("/api/country", methods=['POST'])
def get_country_map_data():
    selected_metric = request.get_json().get("metric", "anxiety")

    local_gj = copy.deepcopy(gj)

    for f in local_gj["features"]:
        iso3 = f['id']

        if iso3:
            values = raw_data[raw_data['country'] == iso3][selected_metric]
            values = values[values.notna()]
            val = values.mean() if not values.empty else 0
            f[selected_metric] = float(val)
        else:
            f[selected_metric] = 0

    return jsonify(local_gj)

@app.route("/api/summary", methods=['POST'])
def get_country_summary():
    filters = request.get_json()
    df = raw_data.copy()
    if 'country' in filters:
        df = df[df['country'] == filters['country']]
    if 'cluster' in filters:
        df = df[df['cluster'] == int(filters['cluster'])]
    return jsonify(df.to_dict(orient='records'))

@app.route("/api/pcp", methods=['POST'])
def get_pcp_data():
    filters = request.get_json()
    df = raw_data.copy()
    if 'country' in filters:
        df = df[df['country'] == filters['country']]
    if 'cluster' in filters:
        df = df[df['cluster'] == int(filters['cluster'])]
    return jsonify(df[cluster_features + ['country', 'cluster']].to_dict(orient='records'))

@app.route("/api/wordcloud", methods=['POST'])
def get_wordcloud_data():
    filters = request.get_json()
    print(filters)
    df = raw_data.copy()
    if 'country' in filters:
        df = df[df['country'] == filters['country']]
    top_genres = df['genre'].value_counts().head(20).reset_index()
    top_genres.columns = ['genre', 'count']
    return jsonify(top_genres.to_dict(orient='records'))

@app.route("/api/cluster", methods=['POST'])
def get_cluster_summary():
    filters = request.get_json()
    df = raw_data.copy()
    if 'country' in filters:
        df = df[df['country'] == filters['country']]
    summary = df.groupby('cluster').agg({
        'anxiety': 'mean', 'depression': 'mean', 'energy': 'mean', 'valence': 'mean', 'bpm': 'mean'
    }).reset_index()
    return jsonify(summary.to_dict(orient='records'))

@app.route("/api/predict/anxiety", methods=['POST'])
def predict_anxiety():
    input_data = request.get_json()
    X_input = pd.DataFrame([input_data])
    prediction = kreg.predict(X_input)[0]
    return jsonify({"predicted_anxiety": float(prediction)})

@app.route("/api/mca", methods=['POST'])
def get_mca():
    categorical_cols = [
        'while working', 'exploratory', 'foreign', 'effects',
        'frequency [classical]', 'frequency [country]', 'frequency [edm]',
        'frequency [folk]', 'frequency [gospel]', 'frequency [hip hop]',
        'frequency [jazz]', 'frequency [k pop]', 'frequency [latin]',
        'frequency [lofi]', 'frequency [metal]', 'frequency [pop]',
        'frequency [r&b]', 'frequency [rap]', 'frequency [rock]',
        'frequency [video game music]'
    ]
    df_categorical = raw_data[categorical_cols].fillna("Unknown")
    mca = prince.MCA(n_components=2, random_state=42)
    coords = mca.fit_transform(df_categorical)
    coords.columns = ['mca1', 'mca2']
    coords['effects'] = raw_data['effects'].values
    coords['country'] = raw_data['country'].values
    coords['cluster'] = raw_data['cluster'].values
    return jsonify(coords.to_dict(orient='records'))

@app.route("/")
def home():
    return render_template("index.html")


if(__name__ == "__main__"):
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    server = Server(app.wsgi_app)
    server.watch('templates/')
    server.watch('static/')
    server.serve(port=5000, debug=True)