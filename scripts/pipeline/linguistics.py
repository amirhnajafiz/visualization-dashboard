import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def get_genre(df):
    """
    Get the genre of the survey results.
    """
    return df['genre'].unique()

def convert_genres(path: str, nlp: any, main_vectors: any, genre_list: str):
    """
    Convert the genres in the dataset to the closest existing value in the genre list.

    Args:
        path (str): The path to the dataset.
        nlp (any): The nlp model used for vectorization.
        main_vectors (any): The vectors of the main dataset.
        genre_list (str): The list of existing genres.
    """
    # load the dataset
    df = pd.read_csv(path)

    # create a mapping of genres to the closest existing value in the genre list
    def find_closest_genre(genre):
        if pd.isna(genre):  # check if the genre is NaN
            return genre  # keep NaN as is
        vec = nlp.transform([genre])
        similarity = cosine_similarity(vec, main_vectors)[0]
        closest_index = similarity.argmax()
        return genre_list[closest_index]

    # replace the genres in the dataset with the closest existing value
    df['genre'] = df['genre'].apply(find_closest_genre)

    # save the updated dataset
    df.to_csv(path, index=False)


if __name__ == "__main__":
    # load the base dataset
    df = pd.read_csv('tmp/mxmh_survey_results.csv')

    # get the genres of the survey results
    genres = get_genre(df)

    # vectorize the genres
    vectorizer = TfidfVectorizer().fit(genres)
    main_vectors = vectorizer.transform(genres)

    # list of existing sources
    datasets = ['tmp/apple_music_dataset.csv', 'tmp/spotify_2000_tops.csv', 'tmp/spotify_music_dataset.csv', 'tmp/spotify_song_attributes.csv']

    for dataset in datasets:
        print(f"Converting genres in {dataset} to the closest existing value in the genre list...")

        # convert the genres in the dataset to the closest existing value in the genre list
        convert_genres(dataset, vectorizer, main_vectors, genres)
