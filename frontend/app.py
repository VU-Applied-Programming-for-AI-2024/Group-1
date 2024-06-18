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

@app.route("/info")
def info():
    return render_template("review_page.html")


if __name__ == "__main__":
    app.run()