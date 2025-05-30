import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt



def sample_dataset(file_path, output_path, n_samples=5000, n_clusters=25):
    """
    Sample the dataset using PCA and K-means clustering.

    Args:
        file_path (str): Path to the input dataset.
        output_path (str): Path to save the sampled dataset.
        n_samples (int): Number of samples to select.
        n_clusters (int): Number of clusters for K-means.
    """
    # load the dataset
    df = pd.read_csv(file_path)

    # drop non-numeric columns for PCA and clustering
    numeric_df = df.select_dtypes(include=[np.number]).dropna()

    # apply PCA to reduce dimensions to 2 for visualization
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(numeric_df)
    numeric_df['pca_1'] = pca_result[:, 0]
    numeric_df['pca_2'] = pca_result[:, 1]

    # perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    numeric_df['cluster'] = kmeans.fit_predict(numeric_df)

    # sample data points from each cluster proportionally
    sampled_indices = []
    cluster_sizes = []
    for cluster in range(n_clusters):
        cluster_indices = numeric_df[numeric_df['cluster'] == cluster].index
        cluster_size = len(cluster_indices)
        cluster_sizes.append(cluster_size)
        n_cluster_samples = max(1, int((cluster_size / len(numeric_df)) * n_samples))
        sampled_indices.extend(np.random.choice(cluster_indices, n_cluster_samples, replace=False))

    sampled_df = df.loc[sampled_indices]

    # save the sampled dataset
    sampled_df.to_csv(output_path, index=False)

    # plot PCA results
    plt.figure(figsize=(16, 8))

    # PCA with K-means Clusters
    plt.subplot(2, 2, 1)
    plt.scatter(numeric_df['pca_1'], numeric_df['pca_2'], c=numeric_df['cluster'], cmap='viridis', s=10)
    plt.title('PCA with K-means Clusters')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')

    # Sampled Data Points
    plt.subplot(2, 2, 2)
    sampled_pca = numeric_df.loc[sampled_indices]
    plt.scatter(sampled_pca['pca_1'], sampled_pca['pca_2'], c=sampled_pca['cluster'], cmap='viridis', s=10)
    plt.title('Sampled Data Points')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')

    # Histogram of Cluster Sizes
    plt.subplot(2, 2, 3)
    plt.bar(range(n_clusters), cluster_sizes, color='skyblue')
    plt.title('Cluster Sizes')
    plt.xlabel('Cluster')
    plt.ylabel('Number of Points')

    # Proportion of Samples per Cluster
    plt.subplot(2, 2, 4)
    sampled_cluster_sizes = sampled_pca['cluster'].value_counts().sort_index()
    plt.bar(range(n_clusters), sampled_cluster_sizes, color='orange')
    plt.title('Sampled Points per Cluster')
    plt.xlabel('Cluster')
    plt.ylabel('Number of Samples')

    plt.tight_layout()
    plt.show()

# example usage
file_path = 'tmp/merged_attributes_and_mental_health_with_country.csv'
output_path = 'dashboard/data/dataset.csv'
sample_dataset(file_path, output_path)
