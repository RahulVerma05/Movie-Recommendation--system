# Modules used for data sorting and cleaning
import pandas as pd
import numpy as np
import ast
import pickle

# Input the required data file
credits = pd.read_csv("tmdb_5000_credits.csv")
movie = pd.read_csv("tmdb_5000_movies.csv")

movie.head(2)
credits.head(2)

# Merging both files into one
movies = movie.merge(credits, on='title')

# Removing null rows if any
movies.isnull().sum()
movies.dropna(inplace=True)

# Takes only those coulmn which required for our model
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# Function for takes out the value according to column
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

# Function for takes out the director name 
def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

movies['crew'] = movies['crew'].apply(fetch_director)
movies.head()

# Due to so many names in cast we takes only four
def reduce_cast(text):
    L =[]
    c = 0
    for i in ast.literal_eval(text):
        if c < 4:
            L.append(i['name'])
            c += 1
    return L

movies['cast'] = movies['cast'].apply(reduce_cast)

# Removing the Unnessary empty spaces
def space(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

movies['cast'] = movies['cast'].apply(space)
movies['crew'] = movies['crew'].apply(space)
movies['keywords'] = movies['keywords'].apply(space)
movies['genres'] = movies['genres'].apply(space)

# Creating a new column 
movies['tages'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies_df = movies[['movie_id','title','tages']]

movies_df['tages'] = movies_df['tages'].apply(lambda x: " ".join(x))
movies_df['tages'] = movies_df['tages'].apply(lambda x: x.lower())

print(movies_df.head())

# Importing modules for crating a model for Movie
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ignoring all common words of english('a','the','an'...)
tf_vectoriztion = TfidfVectorizer(stop_words='english')
# Creating a metrix for all words in tages by their frequency
tf_matrix = tf_vectoriztion.fit_transform(movies_df['tages'].values.astype('U'))

# Using cosin similarity creating scores for word
cosin_sim = cosine_similarity(tf_matrix,tf_matrix)

# Function which used the input movie name and according to cosin score print most related movies
def get_recommand(title, cosin_sim = cosin_sim):
    idx = movies_df[movies_df['title'] == title].index[0]
    sim_score = list(enumerate(cosin_sim[idx]))
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse= True)
    sim_score = sim_score[1:11]
    movie_indicate = [i[0] for i in sim_score]
    return movies_df['title'].iloc[movie_indicate]

film = 'Avatar'
print('film recommended ')
print(get_recommand(film))