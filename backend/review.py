import sys
from tmdbv3api import TMDb, Movie, TV, Genre
from flask import Flask
app = Flask(__name__)


tmdb = TMDb()
tmdb.api_key = '46cbbac59c440a0b0490ad2adad2b849'
my_movie = Movie()