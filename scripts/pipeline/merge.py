import pandas as pd



def merge_songs_and_genres():
    """
    Merge the songs and genres datasets from Apple Music and Spotify.
    """
    # read the CSV files
    apple_music_df = pd.read_csv('datasets/apple_music_dataset.csv')
    spotify_df = pd.read_csv('datasets/spotify_music_dataset.csv')

    # merge the datasets
    combined_df = pd.concat([spotify_df, apple_music_df]).drop_duplicates(subset=['song', 'genre'], keep='first')

    # reindex to ensure all columns are present and fill missing values with NaN
    combined_df = combined_df.reindex(columns=spotify_df.columns.union(apple_music_df.columns, sort=False))
    combined_df = combined_df.reset_index(drop=True)

    # remove the missing values
    combined_df = combined_df.dropna()
    # remove duplicates
    combined_df = combined_df.drop_duplicates()

    # save the merged dataset if needed
    combined_df.to_csv('datasets/merged_music_dataset.csv', index=False)

def merge_songs_and_attributes():
    """
    Merge the songs and attributes datasets from all sources.
    """
    # read the CSV files
    merged_songs_df = pd.read_csv('datasets/merged_music_dataset.csv')
    spotify_2000_df = pd.read_csv('datasets/spotify_2000_tops.csv')
    songs_attributes = pd.read_csv('datasets/spotify_song_attributes.csv')

    # merge the datasets
    combined_df = pd.concat([merged_songs_df, spotify_2000_df, songs_attributes], axis=0, ignore_index=True)

    # reindex to ensure all columns are present and fill missing values with NaN
    combined_df = combined_df.reindex(columns=merged_songs_df.columns.union(spotify_2000_df.columns).union(songs_attributes.columns, sort=False))
    combined_df = combined_df.reset_index(drop=True)

    # fill missing values using linear interpolation
    combined_df = combined_df.interpolate(method='linear', limit_direction='both')

    # save the merged dataset if needed
    combined_df.to_csv('datasets/merged_attributes_dataset.csv', index=False)

def merge_attributes_and_mental_health():
    """
    Merge the songs attributes and mental health datasets.
    """
    # read the CSV files
    songs_attributes = pd.read_csv('datasets/merged_attributes_dataset.csv')
    mental_health_df = pd.read_csv('datasets/mxmh_survey_results.csv')

    # drop the 'song' column from songs_attributes
    songs_attributes = songs_attributes.drop(columns=['song'], errors='ignore')

    # merge the datasets using the 'genre' column
    combined_df = pd.merge(songs_attributes, mental_health_df, on='genre', how='inner')
    # reindex to ensure all columns are present and fill missing values with NaN
    combined_df = combined_df.reindex(columns=songs_attributes.columns.union(mental_health_df.columns, sort=False))
    combined_df = combined_df.reset_index(drop=True)

    # fill missing values using linear interpolation
    combined_df = combined_df.interpolate(method='linear', limit_direction='both')
    # remove duplicates
    combined_df = combined_df.drop_duplicates()
    # remove the missing values
    combined_df = combined_df.dropna()

    # save the merged dataset
    combined_df.to_csv('datasets/merged_attributes_and_mental_health.csv', index=False)


if __name__ == "__main__":
    merge_songs_and_genres()
    merge_songs_and_attributes()
    merge_attributes_and_mental_health()
