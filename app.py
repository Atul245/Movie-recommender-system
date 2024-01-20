import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=39a413bff97dc75b46e54fe50eb767f0&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()

    poster_path = data['poster_path']
    rating = data['vote_average']
    overview = data['overview']
    imdb_id = data['imdb_id']

    
    genres_list = data.get('genres', [])
    genres = [genre.get('name', 'Unknown') for genre in genres_list]

    full_path = "https://image.tmdb.org/t/p/w500" + poster_path

    return full_path, rating, overview, genres, imdb_id

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    recommended_movies_rating = []
    recommended_movies_overview= []
    recommended_movies_genres = []
    recommended_movies_imdbid = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        full_path, rating, overview, genres, imdb_id = fetch_poster(movie_id)
        recommended_movies_poster.append(full_path)
        recommended_movies_name.append(movies.iloc[i[0]].title)
        recommended_movies_rating.append(rating)
        recommended_movies_overview.append(overview)
        recommended_movies_genres.append(genres)
        recommended_movies_imdbid.append(imdb_id)

    return (
        recommended_movies_name,
        recommended_movies_poster,
        recommended_movies_rating,
        recommended_movies_overview,
        recommended_movies_genres,
        recommended_movies_imdbid,
    )


st.header("Movie Recommendation System")
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movies_list = movies['title'].values
selected_movie = st.selectbox(
    'Search Movie for Recommendation',
    movies_list
)

if st.button('Show Recommendation'):
    recommended_movies_name, recommended_movies_poster, recommended_movies_rating, recommended_movies_overview, recommended_movies_genres, recommended_movies_imdbid = recommend(selected_movie)


    for i in range(5):
        container = st.container(border=True)

        # Split the container into two columns
        col1, col2 = container.columns([0.4, 0.6])

        # Part 1: Image
        col1.image(recommended_movies_poster[i], width=900, use_column_width=True)

        # Part 2: Overview, Genres, Rating, IMDb_id, and Title
        with col2:
            genres_line = " ".join([f"<div style='border: 2px solid black; border-radius: 5px; padding: 5px; margin: 5px; display: inline-block;'>{genre}</div>" for genre in recommended_movies_genres[i]])
            st.markdown(genres_line, unsafe_allow_html=True)

            st.header(recommended_movies_name[i])
            st.write(recommended_movies_overview[i])

            st.markdown(
                f"<span style='border: 1px solid white; border-radius: 5px; padding: 5px; margin: 2px; display: inline-block; color: white;'>IMDb ID : <span style='color:#FFEF00'>{recommended_movies_imdbid[i]}</span></span>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<span style='color:gold; font-size: 1.2em;'>&#9733;</span> Rating: <span style='color:green'>{recommended_movies_rating[i]}</span><span style='color:white'>/10</span>",
                unsafe_allow_html=True
            )











