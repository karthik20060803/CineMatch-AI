import pandas as pd
import ast
import pickle

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load datasets
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# Merge
movies = movies.merge(credits, on="title")

# Keep useful columns
movies = movies[
    ["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]
]

# Remove missing values
movies.dropna(inplace=True)


def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L


def convert3(obj):
    L = []
    counter = 0

    for i in ast.literal_eval(obj):

        if counter != 3:
            L.append(i["name"])
            counter += 1
        else:
            break

    return L


def fetch_director(obj):

    L = []

    for i in ast.literal_eval(obj):

        if i["job"] == "Director":

            L.append(i["name"])

            break

    return L


movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert3)
movies["crew"] = movies["crew"].apply(fetch_director)

movies["overview"] = movies["overview"].apply(lambda x: x.split())

for feature in ["genres", "keywords", "cast", "crew"]:
    movies[feature] = movies[feature].apply(
        lambda x: [i.replace(" ", "") for i in x]
    )

movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

new_df = movies[["movie_id", "title", "tags"]].copy()

new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))

new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())

ps = PorterStemmer()


def stem(text):
    return " ".join(ps.stem(word) for word in text.split())


new_df["tags"] = new_df["tags"].apply(stem)

cv = CountVectorizer(max_features=5000, stop_words="english")

vectors = cv.fit_transform(new_df["tags"]).toarray()

similarity = cosine_similarity(vectors)

pickle.dump(new_df, open("movie.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("Done!")
print("movie.pkl created")
print("similarity.pkl created")