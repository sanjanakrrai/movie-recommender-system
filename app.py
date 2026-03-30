import streamlit as st
import pickle
import requests

# -------------------------------
# CONFIG (IMPORTANT)
# -------------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# -------------------------------
# LOAD DATA
# -------------------------------
movies = pickle.load(open('movie_list.pkl', 'rb'))

import requests
import pickle

def load_model():
    url = "https://drive.google.com/uc?export=download&id=1GAC5wkLzheXAwC535ICNzRKzaHrycors"

    response = requests.get(url, stream=True)

    with open("model.pkl", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    return model

similarity = load_model()
# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.title {
    font-size: 50px;
    font-weight: bold;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

.movie-container {
    text-align: center;
}

.movie-container img {
    border-radius: 12px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.movie-container img:hover {
    transform: scale(1.08);
    box-shadow: 0px 10px 30px rgba(255,0,0,0.6);
}

.movie-title {
    font-size: 16px;
    color: white;
    margin-top: 8px;
}

.stButton>button {
    background-color: #e50914;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 220px;
    font-size: 16px;
    font-weight: bold;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# FETCH POSTER
# -------------------------------
@st.cache_data
def fetch_poster(title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key=e6f7d68e57c1fcfca8a61d9938d29a4a&query={title}"
        data = requests.get(url).json()

        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"

        return "https://via.placeholder.com/500x750?text=No+Poster"

    except:
        return "https://via.placeholder.com/500x750?text=Error"

# -------------------------------
# RECOMMEND FUNCTION
# -------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        names.append(title)
        posters.append(fetch_poster(title))

    return names, posters

# -------------------------------
# UI HEADER
# -------------------------------
st.markdown('<div class="title">🎬 Movie Recommender</div>', unsafe_allow_html=True)

# -------------------------------
# SELECT BOX
# -------------------------------
selected_movie = st.selectbox(
    "Choose a movie",
    movies['title'].values
)

# -------------------------------
# BUTTON
# -------------------------------
if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown("<div class='movie-container'>", unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)