import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Function to fetch the poster of a movie
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"  # Placeholder image
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

# Function to recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        st.error("Movie not found in the database.")
        return [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        try:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        except Exception as e:
            st.error(f"Error in recommendation: {e}")
    
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI setup
st.set_page_config("Recommender", layout="wide", page_icon="icon.png")
st.header('Movie Recommender System')

# Load movie data and similarity matrix
try:
    movies = pd.read_csv("movie_list.csv")
    similarity = pd.read_csv("similarity.csv").values  # Load similarity as a numpy array
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
except Exception as e:
    st.error(f"Error loading data: {e}")

# Dropdown to select a movie
if 'movies' in locals():
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or Select a movie from the Dropdown",
        movie_list,
        placeholder="Avatar"
    )

    # Display recommendations when the button is clicked
    if st.button('Show Recommendation'):
        if selected_movie:
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            if recommended_movie_names:
                cols = st.columns(5)
                for idx, col in enumerate(cols):
                    if idx < len(recommended_movie_names):
                        with col:
                            st.text(recommended_movie_names[idx])
                            st.image(recommended_movie_posters[idx])
        else:
            st.error("Please select a movie.")

        









