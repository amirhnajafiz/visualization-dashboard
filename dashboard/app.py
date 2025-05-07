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
import warnings



warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_country_name(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code).name
    except Exception:
        print(f"❗ No match found for ISO3 code: {iso3_code}")
        return None

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
    filters = request.get_json()
    selected_metric = filters.get("metric", "anxiety")
    selected_countries = filters.get('countries', None)

    local_gj = copy.deepcopy(gj)

    for f in local_gj["features"]:
        country = f['id']

        if selected_countries and country not in selected_countries:
            f[selected_metric] = 0 # grey out unselected countries
        else:
            val = raw_data[raw_data['country'] == country][selected_metric].mean()
            f[selected_metric] = float(val) if not np.isnan(val) else 0

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

    if filters.get('countries'):
        df = df[df['country'].isin(filters['countries'])]

    pcp_columns = [
        'country',
        'anxiety',
        'depression',
        'insomnia',
        'ocd',
        'bpm',
        'valence',
        'energy',
        'hours',
        'age'
    ]

    # Aggregate: group by country, take MEAN of features
    grouped = df[pcp_columns].groupby('country').mean().reset_index()

    grouped["id"] = grouped["country"]
    grouped["location"] = grouped["country"].map(get_country_name)

    final_cols = ['id', 'location', 'anxiety', 'depression', 'insomnia', 'ocd', 'bpm', 'valence', 'energy', 'hours', 'age']
    return jsonify(grouped[final_cols].to_dict(orient="records"))


@app.route("/api/wordcloud", methods=['POST'])
def get_wordcloud_data():
    filters = request.get_json()
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

@app.route("/api/correlation", methods=['POST'])
def get_correlation_data():
    filters = request.get_json()
    df = raw_data.copy()

    if filters.get('countries'):
        df = df[df['country'].isin(filters['countries'])]

    corr = df[['age', 'hours', 'bpm', 'anxiety', 'depression', 'insomnia', 'ocd']].corr()
    corr_reset = corr.reset_index()
    corr_reset.rename(columns={"index": ""}, inplace=True)

    result = []
    for col in corr_reset.columns[1:]:
        for idx, row in corr_reset.iterrows():
            result.append({
                "x": row[""],
                "y": col,
                "value": row[col]
            })
    return jsonify(result)

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

@app.route("/api/stackedbar", methods=["POST"])
def get_stackedbar_data():
    payload = request.get_json()
    metric = payload.get("mental_health_metric", "anxiety")
    countries = payload.get("countries", [])

    df = raw_data.copy()

    # Filter if countries are selected
    if countries:
        df = df[df['country'].isin(countries)]

    # Bin mental health metric into Low, Moderate, High
    bins = [0, 0.33, 0.66, 1.0]
    labels = ['Low', 'Moderate', 'High']
    df['health_bucket'] = pd.cut(df[metric], bins=bins, labels=labels, include_lowest=True)

    # Count genres within each health bucket
    grouped = df.groupby(['health_bucket', 'genre'], observed=True).size().reset_index(name='count')

    # Pivot to wide format for stacked bar
    pivot = grouped.pivot(index='health_bucket', columns='genre', values='count')
    pivot = pivot.reset_index()

    return pivot.to_json(orient='records')

@app.route("/api/tsne", methods=["POST"])
def get_tsne():
    payload = request.get_json()
    features = payload.get("features", ["valence", "energy", "danceability", "tempo", "acousticness", "liveness"])
    countries = payload.get("countries", [])
    sample_size = int(payload.get("sample_size", 300))

    df = raw_data.copy()

    if countries:
        df = df[df['country'].isin(countries)]

    # Stratified sampling by genre
    grouped = df.groupby("genre")
    df_sampled = grouped.apply(lambda x: x.sample(min(len(x), max(1, sample_size // len(grouped))))).reset_index(drop=True)

    X = StandardScaler().fit_transform(df_sampled[features])

    # Add normalized features back to DataFrame for frontend t-SNE
    for i, feature in enumerate(features):
        df_sampled[f"norm_{feature}"] = X[:, i]

    # Return original metadata and normalized features
    response_data = df_sampled[["genre", "country"] + [f"norm_{f}" for f in features]].to_dict(orient="records")

    return jsonify(response_data)

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
