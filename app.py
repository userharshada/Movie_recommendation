import pickle
import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    posters = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        posters.append(fetch_poster(movie_id))
    
    return recommended_movies, posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styles
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
        color: #333333;
        font-family: Arial, sans-serif;
    }
    .stButton button {
        background-color: #3366ff;
        color: white;
    }
    .stSelectbox select {
        background-color: #f0f0f0;
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Movie Recommendation System')

option = st.selectbox('How would you like to be contacted?', ('Email', 'Contact'))

selected_movie = st.selectbox('Select a movie', movies['title'])

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0])
        else:
            st.text("Poster not available")
    with col2:
        st.text(names[1])
        if posters[1]:
            st.image(posters[1])
        else:
            st.text("Poster not available")
    with col3:
        st.text(names[2])
        if posters[2]:
            st.image(posters[2])
        else:
            st.text("Poster not available")
    with col4:
        st.text(names[3])
        if posters[3]:
            st.image(posters[3])
        else:
            st.text("Poster not available")
    with col5:
        st.text(names[4])
        if posters[4]:
            st.image(posters[4])
        else:
            st.text("Poster not available")
