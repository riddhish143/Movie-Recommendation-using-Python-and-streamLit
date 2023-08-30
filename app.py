import streamlit as st
import pickle
import pandas as pd
import requests

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
    for i in distances[1:10]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

with open('movie_dict.pkl', 'rb') as file:
    movie_dict = pickle.load(file)

with open('similarity.pkl' , 'rb') as file:
    similarity = pickle.load(file)

movies = pd.DataFrame(movie_dict)
st.title("Movie Recommendation System")
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    num_columns = 3  # Number of columns in each row
    num_rows = -(-len(recommended_movie_names) // num_columns)  # Calculate the number of rows needed

    rows = st.columns(num_rows)  # Create a list of columns for rows

    for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
        row_idx = i // num_columns  # Calculate the current row index
        col_idx = i % num_columns  # Calculate the current column index

        with rows[row_idx]:
            st.text(name)
            st.image(poster, width=200)  # Adjust the width as needed

