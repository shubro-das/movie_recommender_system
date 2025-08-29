import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))

df = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Select a movie:', df['title'].values)

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d5806c043d075a25394aa8a5114acf67')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    
    movie_index = df[df['title']==movie].index[0]
    distances = similarity[movie_index]
    recommended = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:6]

    recommendations = []
    posters = []
    for i in recommended:
        movieId = df.iloc[i[0]]['movie_id']
        # fetch poster from api
        recommendations.append(df.iloc[i[0]]['title'])
        posters.append(fetch_poster(movieId))
    return recommendations, posters



if st.button('Recommend'):
    # st.write('You selected:', selected_movie)
    # # Here you would add the recommendation logic
    st.write('Top 5 recommendations for', selected_movie, ':')
    movie_name, poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(poster[4])

    # # Dummy recommendations for illustration
    # recommendations = movies['title'].sample(5).values
    # for rec in recommendations:
    #     # st.write(rec)