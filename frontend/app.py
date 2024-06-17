from flask import Flask, render_template
from dotenv import load_dotenv
import json
import requests
import os


app = Flask(__name__)

load_dotenv()
api_key = os.environ['API_KEY']
base_url = f'https://api.themoviedb.org/3'

@app.route("/")
def home():
    response = f'{base_url}/trending/movie/day?api_key={api_key}'
    trending_movies = requests.get(response).json()
    return render_template("index.html", data=trending_movies['results'])


@app.route("/genre")
def genre():
    return render_template("genre.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/info/<movie_id>")
def info(movie_id):
    response = f'{base_url}/movie/{movie_id}?api_key={api_key}'
    results = requests.get(response).json()
    reponse2 = f'{base_url}/movie/{movie_id}/credits?api_key={api_key}'
    results2 = requests.get(reponse2).json()
    movie_info = {
        'movie_title' : results.get('original_title'),
        'plot' : results.get('overview'),
        'poster_path' : f'https://image.tmdb.org/t/p/w500/{results.get("poster_path")}',
        'release_date' : results.get('release_date'),
        'score' : results.get('vote_average')
    }
    director_name = 'Not Available'
    for person in results2.get('crew'):
        if person['job'] == 'Director':
            director_name = person['name']
    movie_info['director'] = director_name
    return render_template("review_page.html", data=movie_info)


if __name__ == "__main__":
    app.run()