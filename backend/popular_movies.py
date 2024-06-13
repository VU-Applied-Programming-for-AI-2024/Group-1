from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tmdbv3api import TMDb, Movie
from typing import Dict, Any


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

tmdb = TMDb()
tmdb.api_key = '46cbbac59c440a0b0490ad2adad2b849' 

movie_api = Movie()

class MovieModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    overview = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.String(20), nullable=True)
    poster_path = db.Column(db.String(200), nullable=True)
    vote_average = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Movie {self.title}>'
    
popular_movie_dict: Dict[str, Dict[str, Any]] = {}

with app.app_context():
    db.create_all()
    popular_movies = movie_api.popular()
    for movie in popular_movies:
        popular_movie_dict[movie.title] = {"ID": movie.id, "Overview": movie.overview, "Release Date": movie.release_date,
                                           "Poster Path": movie.poster_path, "Vote Average": f"{movie.vote_average}\n"}
        print(f"{movie.title}: {popular_movie_dict[movie.title]}, \n")
        existing_movie = MovieModel.query.filter_by(id=movie.id).first()
        if not existing_movie:
            new_movie = MovieModel(
                id=movie.id,
                title=movie.title,
                overview=movie.overview,
                release_date=movie.release_date,
                poster_path=movie.poster_path,
                vote_average=movie.vote_average
            )
            db.session.commit()
