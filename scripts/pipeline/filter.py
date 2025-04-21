import pandas as pd



def filter_attribute(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Filters the DataFrame based on a specific columns.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (list): The column names to filter by.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    # check if the specified column exists in the DataFrame
    if not all(col in df.columns for col in columns):
        raise ValueError(f"One or more columns {columns} do not exist in the DataFrame.")

    # filter the DataFrame based on the specified column and value
    filtered_df = df[columns]

    return filtered_df

def save_filtered_data(df: pd.DataFrame, columns: list, output_path: str) -> None:
    """
    Saves the filtered DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        columns (list): The column names to save.
        output_path (str): The path to save the CSV file.
    """
    # save the df to a CSV file replacing the existing columns with new columns
    df.columns = columns

    # save the DataFrame to a CSV file
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    datasets = [
        {
            "path": "assets/archive/apple_music_dataset.csv",
            "output_path": "tmp/apple_music_dataset.csv",
            "columns": ["trackCensoredName", "primaryGenreName"],
            "new_columns": ["song", "genre"]
        },
        {
            "path": "assets/archive/spotify_2000_tops.csv",
            "output_path": "tmp/spotify_2000_tops.csv",
            "columns": ["Title", "Top Genre", "Beats Per Minute (BPM)", "Energy", "Danceability", "Loudness (dB)", "Speechiness", "Acousticness", "Liveness", "Valence", "Popularity"],
            "new_columns": ["song", "genre", "bpm", "energy", "danceability", "loudness", "speechiness", "acousticness", "liveness", "valence", "popularity"]
        },
        {
            "path": "assets/archive/spotify_music_dataset.csv",
            "output_path": "tmp/spotify_music_dataset.csv",
            "columns": ["song", "genre", "popularity", "danceability", "energy", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"],
            "new_columns": ["song", "genre", "popularity", "danceability", "energy", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
        },
        {
            "path": "assets/archive/spotify_song_attributes.csv",
            "output_path": "tmp/spotify_song_attributes.csv",
            "columns": ["trackName", "genre", "danceability", "energy", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"],
            "new_columns": ["song", "genre", "danceability", "energy", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
        },
        {
            "path": "assets/archive/mxmh_survey_results.csv",
            "output_path": "tmp/mxmh_survey_results.csv",
            "columns": ["Age", "Hours per day", "While working", "Fav genre", "Exploratory", "Foreign languages", "Anxiety", "Depression", "Insomnia", "OCD", "Music effects", "Frequency [Classical]", "Frequency [Country]", "Frequency [EDM]", "Frequency [Folk]", "Frequency [Gospel]", "Frequency [Hip hop]", "Frequency [Jazz]", "Frequency [K pop]", "Frequency [Latin]", "Frequency [Lofi]", "Frequency [Metal]", "Frequency [Pop]", "Frequency [R&B]", "Frequency [Rap]", "Frequency [Rock]", "Frequency [Video game music]"],
            "new_columns": ["age", "hours", "while working", "genre", "exploratory", "foreign", "anxiety", "depression", "insomnia", "ocd", "effects", "frequency [classical]", "frequency [country]", "frequency [edm]", "frequency [folk]", "frequency [gospel]", "frequency [hip hop]", "frequency [jazz]", "frequency [k pop]", "frequency [latin]", "frequency [lofi]", "frequency [metal]", "frequency [pop]", "frequency [r&b]", "frequency [rap]", "frequency [rock]", "frequency [video game music]"]
        },
    ]

    for dataset in datasets:
        print(f"\tfiltering {dataset['path']} with columns {dataset['columns']} and saving to {dataset['output_path']}")
        print(f"\tnumber of columns: {len(dataset['columns'])}")

        # read the dataset
        df = pd.read_csv(dataset["path"])

        # filter the dataset
        filtered_df = filter_attribute(df, dataset["columns"])

        # save the filtered dataset
        save_filtered_data(filtered_df, dataset["new_columns"], dataset["output_path"])
