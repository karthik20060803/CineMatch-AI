
import pickle
import pandas as pd
import requests

# Load the processed movie dataframe
movie = pickle.load(open('movie.pkl', 'rb'))

# Load the similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))
API_KEY = '7cef7832'
def fetch_movie_details(title):

    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"

    response = requests.get(url)

    data = response.json()

    return {
        "title": data.get("Title", title),
        "poster": data.get("Poster"),
        "rating": data.get("imdbRating", "N/A"),
        "year": data.get("Year", "N/A"),
        "genre": data.get("Genre", "N/A")
    }
def recommend(movie_title):

    try:
        movie_index = movie[movie['title'] == movie_title].index[0]

    except IndexError:
        return []

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []

    for i in distances[1:6]:

        movie_name = movie.iloc[i[0]].title

        details = fetch_movie_details(movie_name)

        recommendations.append(details)

    return recommendations