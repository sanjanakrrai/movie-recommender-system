import streamlit as st
import pickle
import pandas as pd
import requests

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
img {
    border-radius: 10px;
}
img:hover {
    transform: scale(1.05);
    transition: 0.3s;
}
.stButton>button {
    background-color: #e50914;
    color: white;
    border-radius: 8px;
    height: 50px;
    width: 250px;
    font-size: 18px;
}
h1 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOAD MODEL --------------------
@st.cache_resource
def load_model():
    import requests

    url = "https://dl.dropboxusercontent.com/scl/fi/jhbykfrusg79wiwxxnrn0/model.pkl?rlkey=kdjh7v440mg6v4q57sz4vsuwd"

    response = requests.get(url)

    with open("model.pkl", "wb") as f:
        f.write(response.content)

    model = pickle.load(open("model.pkl", "rb"))
    return model

similarity = load_model()

# Load movie data
movies = pickle.load(open('movie_list.pkl', 'rb'))

# -------------------- TMDB POSTER --------------------
def fetch_poster(movie_id):
    api_key = "e6f7d68e57c1fcfca8a61d9938d29a4a"  
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# -------------------- RECOMMEND FUNCTION --------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# -------------------- UI --------------------
st.title('🎬 Movie Recommender')

selected_movie = st.selectbox(
    "Choose a movie",
    movies['title'].values
)

if st.button('Recommend Movies'):
    with st.spinner('Finding best movies for you...'):
        names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.caption(names[0])

    with col2:
        st.image(posters[1])
        st.caption(names[1])

    with col3:
        st.image(posters[2])
        st.caption(names[2])

    with col4:
        st.image(posters[3])
        st.caption(names[3])

    with col5:
        st.image(posters[4])
        st.caption(names[4])

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("Made with ❤️ by Sanjana")