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

    # statistics tracking
    total_changes = 0
    genre_changes = {}
    similarity_scores = []

    # create a mapping of genres to the closest existing value in the genre list
    def find_closest_genre(genre):
        nonlocal total_changes
        if pd.isna(genre):  # check if the genre is NaN
            return genre  # keep NaN as is
        vec = nlp.transform([genre])
        similarity = cosine_similarity(vec, main_vectors)[0]
        closest_index = similarity.argmax()
        best_score = similarity[closest_index]
        similarity_scores.append(best_score)

        closest_genre = genre_list[closest_index]
        if genre != closest_genre:
            total_changes += 1
            genre_changes[genre] = genre_changes.get(genre, 0) + 1
        return closest_genre

    # replace the genres in the dataset with the closest existing value
    df['genre'] = df['genre'].apply(find_closest_genre)

    # save the updated dataset
    df.to_csv(path, index=False)

    # calculate statistics
    average_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0
    print(f"\tstatistics for {path}:")
    print(f"\t\ttotal changes: {total_changes}")
    print(f"\t\taverage best similarity score: {average_similarity:.4f}")
    print(f"\t\tchanges per genre: {genre_changes}")


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
        print(f"\tconverting genres in {dataset}")

        # convert the genres in the dataset to the closest existing value in the genre list
        convert_genres(dataset, vectorizer, main_vectors, genres)
