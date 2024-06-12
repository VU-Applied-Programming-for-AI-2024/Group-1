from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tmdbv3api import TMDb, Movie


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

tmdb = TMDb()
tmdb.api_key = '1a674da5bbed27d22ed3a066a5899ca1' # replace with your API key 

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

with app.app_context():
    db.create_all()

    popular_movies = movie_api.popular()
    for movie in popular_movies:
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
            db.session.add(new_movie)
            db.session.commit()
