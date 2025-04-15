import pandas as pd
from difflib import get_close_matches
import random



def get_genre(df):
    """
    Get the genre of the survey results.
    """
    return df['genre'].unique()

def convert_genres(path: str, genre_list: list):
    """
    Convert the genres in the dataset to the closest existing value in the genre list.

    Args:
        path (str): The path to the dataset.
        genre_list (list): The list of existing genres.
    """
    # load the dataset
    df = pd.read_csv(path)

    # create a mapping of genres to the closest existing value in the genre list
    def find_closest_genre(genre):
        if pd.isna(genre):  # check if the genre is NaN
            return genre  # keep NaN as is
        matches = get_close_matches(str(genre), genre_list, n=1, cutoff=0.6)
        return matches[0] if matches else random.choice(genre_list)  # use the closest match or a random genre
        return matches[0] if matches else genre  # use the closest match or keep the original genre

    # replace the genres in the dataset with the closest existing value
    df['genre'] = df['genre'].apply(find_closest_genre)

    # save the updated dataset
    df.to_csv(path, index=False)


if __name__ == "__main__":
    # load the base dataset
    df = pd.read_csv('tmp/mxmh_survey_results.csv')

    # get the genre of the survey results
    genre = get_genre(df)

    # list of existing sources
    datasets = ['tmp/apple_music_dataset.csv', 'tmp/spotify_2000_tops.csv', 'tmp/spotify_music_dataset.csv', 'tmp/spotify_song_attributes.csv']

    for dataset in datasets:
        print(f"Converting genres in {dataset} to the closest existing value in the genre list...")

        # convert the genres in the dataset to the closest existing value in the genre list
        convert_genres(dataset, genre)
