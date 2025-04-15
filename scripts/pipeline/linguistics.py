import pandas as pd
import spacy
from sklearn.metrics.pairwise import cosine_similarity



def get_genre(df):
    """
    Get the genre of the survey results.
    """
    return df['genre'].unique()

def convert_genres(path: str, nlp: any, genre_list: any):
    """
    Convert the genres in the dataset to the closest existing value in the genre list.

    Args:
        path (str): The path to the dataset.
        nlp (any): The spaCy model used for vectorization.
        genre_list (any): The list of existing genres.
    """
    # load the dataset
    df = pd.read_csv(path)

    # create a mapping of genres to the closest existing value in the genre list
    def find_closest_genre(genre):
        if pd.isna(genre):  # check if the genre is NaN
            return genre  # keep NaN as is
        other_vec = nlp(genre).vector
        similarities = cosine_similarity([other_vec], main_vectors)[0]
        best_match_index = similarities.argmax()
        best_match = genre_list[best_match_index]
        return best_match

    # replace the genres in the dataset with the closest existing value
    df['genre'] = df['genre'].apply(find_closest_genre)

    # save the updated dataset
    df.to_csv(path, index=False)


if __name__ == "__main__":
    # load the base dataset
    df = pd.read_csv('tmp/mxmh_survey_results.csv')

    # load the spacy model
    nlp = spacy.load("en_core_web_md")

    # get the genres of the survey results
    genres = get_genre(df)

    # convert genres to spaCy vectors
    main_vectors = [nlp(genre).vector for genre in genres]

    # list of existing sources
    datasets = ['tmp/apple_music_dataset.csv', 'tmp/spotify_2000_tops.csv', 'tmp/spotify_music_dataset.csv', 'tmp/spotify_song_attributes.csv']

    for dataset in datasets:
        print(f"Converting genres in {dataset} to the closest existing value in the genre list...")

        # convert the genres in the dataset to the closest existing value in the genre list
        convert_genres(dataset, nlp, main_vectors)
