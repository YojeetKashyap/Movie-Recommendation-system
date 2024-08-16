
import random
import numpy as np
import pandas as pd
import pickle
import nltk
import ast
credits_df = pd.read_csv("credits.csv")
movies_df = pd.read_csv("movies.csv")
movies_df = movies_df.merge(credits_df,on = "title")
movies_df.shape
movies_df = movies_df[['movie_id','title','overview','genres','keywords','cast','crew']]
movies_df.isnull().sum()
movies_df.dropna(inplace = True)

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L
movies_df['genres'] = movies_df['genres'].apply(convert)
movies_df['keywords'] = movies_df['keywords'].apply(convert)

def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i["name"])
            counter += 1
        else :
            break
        return L
    
    
movies_df['cast'] =  movies_df['cast'].apply(convert3)  

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i["job"] == "Director" :
            L.append(i["name"])
    return L
movies_df['crew'] = movies_df['crew'].apply(fetch_director)

movies_df["overview"] = movies_df['overview'].apply(lambda x:x.split())


def process_list(lst):
    if lst is not None:
        return [i.replace(" ", "") for i in lst]
    else:
        return None

movies_df["genres"] = movies_df["genres"].apply(process_list)
movies_df["keywords"] = movies_df["keywords"].apply(process_list)
movies_df["cast"] = movies_df["cast"].apply(process_list)
movies_df["crew"] = movies_df["crew"].apply(process_list)

movies_df['tags'] =  movies_df['overview'] + movies_df['genres'] + movies_df["keywords"] + movies_df["cast"] + movies_df["crew"]
new_df = movies_df[["movie_id","title","tags"]]

new_df['tags'] = new_df['tags'].apply(lambda x: ' '.join(x) if isinstance(x, (list, tuple)) else '')
new_df['tags'] =  new_df['tags'].apply(lambda x:x.lower())

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 5000 , stop_words = 'english')
cv.fit_transform(new_df['tags']).toarray().shape
vectors = cv.fit_transform(new_df["tags"]).toarray()

from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

from  sklearn.metrics.pairwise import cosine_similarity
cosine_similarity(vectors)
similarity = cosine_similarity(vectors)
sorted(list(enumerate(similarity[0])),reverse=True,key = lambda x:x[1:6])

#   ----==============================--=++++++++++++++++++++++++++++++++++++++++=

def recommend(movie):
        movie_index = new_df[new_df['title']==movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:5]
        a=[]
        for i in movies_list:
            a.append(new_df.iloc[i[0]].title)
            #print(type(a))
            
        return a


pickle.dump(new_df,open('movie_list.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))

