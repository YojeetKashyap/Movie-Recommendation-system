import pickle
import streamlit as st
from  bs4 import BeautifulSoup
import pandas as pd
import requests
import webbrowser

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.set_page_config("Recommender",layout="wide",page_icon="icon.png")
st.header('Movie Recommender System')
movies = pd.read_csv("movie_list.csv")
    
similarity = pd.read_csv("similarity.csv")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or Select a movie from the Dropdown",
    movie_list,placeholder="Avatar"
)

def download( name ):
    page = requests.get(f"https://mkvcinemas.cat/?s={name}")
    soup = BeautifulSoup(page.content,"html.parser")
    row = soup.find("div",class_=["movies-list","movies-list-full"])
    col = row.find_all("div",class_="ml-item")
    handle = True
    if len(col) == 0 :
        return (f"https://www.imdb.com/find/?q={name}")
        handle=False
        
    anchor = col[0].find("a")
    if handle :
        return anchor["href"]
    
def Call(value) :
    webbrowser.open_new_tab(value)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        links = download(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.link_button("Download",url=links)
    with col2:
        st.text(recommended_movie_names[1])
        links = download(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.link_button("Download",url=links)

    with col3:
        st.text(recommended_movie_names[2])
        links = download(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.link_button("Download",url=links)
        
    with col4:
        st.text(recommended_movie_names[3])
        links = download(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.link_button("Download",url=links)
    with col5:
        st.text(recommended_movie_names[4])
        links = download(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.link_button("Download",url=links)









