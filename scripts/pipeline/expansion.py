import pandas as pd



def expand_spotify_music():
    """
    Expands the Spotify music dataset by splitting the genre column into multiple rows.
    """
    # read the CSV file
    spotify_df = pd.read_csv('tmp/spotify_music_dataset.csv')

    # split rows with multiple genres into separate rows
    spotify_df = spotify_df.assign(genre=spotify_df['genre'].str.split(',')).explode('genre').reset_index(drop=True)

    # save the dataset into a CSV file
    spotify_df.to_csv('tmp/spotify_music_dataset.csv', index=False)

def expand_apple_music():
    """
    Expands the Apple music dataset by splitting the genre column into multiple rows.
    """
    # read the CSV file
    apple_df = pd.read_csv('tmp/apple_music_dataset.csv')

    # split rows with multiple genres into separate rows
    apple_df = apple_df.assign(genre=apple_df['genre'].str.split('/')).explode('genre').reset_index(drop=True)

    # save the dataset into a CSV file
    apple_df.to_csv('tmp/apple_music_dataset.csv', index=False)


if __name__ == "__main__":
    expand_spotify_music()
    expand_apple_music()
