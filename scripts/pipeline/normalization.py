import pandas as pd



def normalize(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Normalize the DataFrame by dividing each value by the maximum value in its column.
    
    Args:
        df (pd.DataFrame): The DataFrame to normalize.
        columns (list): The list of columns to normalize.
    
    Returns:
        pd.DataFrame: The normalized DataFrame.
    """
    # Create a copy of the DataFrame to avoid modifying the original
    df_normalized = df.copy()

    # Normalize the specified columns
    for column in columns:
        if column in df_normalized.columns:
            max_value = df_normalized[column].max()
            if max_value != 0:  # Avoid division by zero
                df_normalized[column] = df_normalized[column] / max_value

    return df_normalized


if __name__ == "__main__":
    datasets = [
        {
            "path": "tmp/spotify_2000_tops.csv",
            "columns": ["bpm", "energy", "danceability", "loudness", "speechiness", "acousticness", "liveness", "valence", "length", "popularity"]
        },
        {
            "path": "tmp/spotify_music_dataset.csv",
            "columns": ["popularity", "danceability", "energy", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
        },
        {
            "path": "tmp/spotify_song_attributes.csv",
            "columns": ["danceability", "energy", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
        },
        {
            "path": "tmp/mxmh_survey_results.csv",
            "columns": ["anxiety", "depression", "insomnia", "ocd"]
        },
    ]

    for dataset in datasets:
        print(f"Normalizing dataset: {dataset['path']}")
        
        # read the dataset
        df = pd.read_csv(dataset["path"])

        # normalize the dataset
        ndf = normalize(df, dataset["columns"])

        # save the normalized dataset
        ndf.to_csv(dataset["path"], index=False)
