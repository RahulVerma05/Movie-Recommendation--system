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

def space(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

movies['cast'] = movies['cast'].apply(space)
movies['crew'] = movies['crew'].apply(space)
movies['keywords'] = movies['keywords'].apply(space)
movies['genres'] = movies['genres'].apply(space)

movies['tages'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies_df = movies[['movie_id','title','tages']]