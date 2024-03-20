import pandas as pd
import numpy as np
import ast
import pickle

credits = pd.read_csv("tmdb_5000_credits.csv")
movie = pd.read_csv("tmdb_5000_movies.csv")

movie.head(2)
credits.head(2)

movies = movie.merge(credits, on='title')
movies.dropna(inplace=True)

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies.head()

movies['keywords'] = movies['keywords'].apply(convert)
movies.head()