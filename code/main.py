import pandas as pd
import numpy as np
import ast
import pickle

credits = pd.read_csv("tmdb_5000_credits.csv")
movie = pd.read_csv("tmdb_5000_movies.csv")

<<<<<<< HEAD:main.py
movie.head(2)
credits.head(2)

movies = movie.merge(credits, on='title')
movies.head()
=======
print(df_2)
>>>>>>> 877dc5823ab59ecde1e9ac3bdb8c65f33aa52959:code/main.py
