import pandas as pd
import numpy as np
import ast
import pickle

credits = pd.read_csv("tmdb_5000_credits.csv")
movie = pd.read_csv("tmdb_5000_movies.csv")

movie.head(2)
credits.head(2)

movies = movie.merge(credits, on='title')
movies.isnull().sum()
movies.dropna(inplace=True)

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies.head()

movies['keywords'] = movies['keywords'].apply(convert)
movies.head()

movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.head()


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

movies['crew'] = movies['crew'].apply(fetch_director)
movies.head()

def reduce_cast(text):
    L =[]
    c = 0
    for i in ast.literal_eval(text):
        if c < 4:
            L.append(i['name'])
            c += 1
    return L

movies['cast'] = movies['cast'].apply(reduce_cast)