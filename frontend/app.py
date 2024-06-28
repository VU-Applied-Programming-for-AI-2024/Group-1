# Import all the libraries required. 
from flask import Flask, render_template, redirect, request, url_for, flash
import sys
import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
import search 
import genre_x
from tmdbv3api import TV, Movie 
import json
import psycopg2



load_dotenv()


app = Flask(__name__)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
api_key = os.getenv('API_KEY')
base_url = 'https://api.themoviedb.org/3'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
# "sqlite:///database.db"
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


my_movie = Movie()
my_tv = TV()
@app.context_processor
def utility_processor():
    return dict(json=json)

class User(db.Model, UserMixin):
    """
    columns for table of users in database
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False) # Note: 80 max length here and 20 in registration form because database takes in
                                                        # hashed version of password which is usually longer
                                        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 
class RegistrationForm(FlaskForm):
    """
    defines attributes of each input field under the signup page
    """
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    
    submit = SubmitField("Register")
    
    def validate_username(self, username):
        """
        validates that each username is unique
        param: username: what users enter under the input field 'username'
        raises: ValidationError: if the username that a user enters is already in the database
        """
        existing_username = User.query.filter_by(
            username=username.data).first()

        if existing_username:
            raise ValidationError(
                "This username already exists."
            )
            
class LoginForm(FlaskForm):
    """
    defines the attributes of each input field in the login page
    """
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "password"})
    
    submit = SubmitField('Login')
    
    def validate_user(self, username):
        """
        validates that users enter a username that already exists
        param: username: what the user enters in the username input field
        raises: ValidationError: if the user enters a username that isn't in the database
        """
        user = User.query.filter_by(username=username.data).first()
        
        if not user:
            flash("Please enter a valid username")
            raise ValidationError("Invalid Username")
        
    def validate_password(self, password):
        """
        validates that users enter the correct password
        param: password: what the user enters in the password input field
        :raises: ValidationError: if the user enters an incorrect password
        """
        user = User.query.filter_by(username=self.username.data).first()
        
        if user and not bcrypt.check_password_hash(user.password, password.data):
          flash("Your password is incorrect")
          raise ValidationError("Invalid Password")

        
# Review model
class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='reviews')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review = db.Column(db.String(700), nullable=False)

# Flask form (flask_wtf)
class Review_form(FlaskForm):
    review = TextAreaField('Review', validators=[InputRequired()])
    submit = SubmitField('Submit Review')


@app.route("/")
def home():
    response = f'{base_url}/trending/movie/day?api_key={api_key}'
    trending_movies = requests.get(response).json()
    return render_template("index.html", data = trending_movies['results'])

@app.route("/genre", methods = ['GET'])
def genre():
    genre_name = request.args.get('genre_name')
    filter_typ = request.args.get('filter_typ')
    sort_opt = request.args.get("sort_opt", 'popularity')
    results = genre_x.genre(filter_typ, genre_name, sort_opt)
    return render_template("genre.html", results=results, genre_name=genre_name, filter_typ=filter_typ, sort_opt=sort_opt)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'You were successfully logged in. Welcome {user.username}!')
            return redirect(url_for('home'))
    return render_template("login.html", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
     
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created, you are now able to login.')
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash(f'You were successfully logged out.')
    return redirect(url_for('home'))

@app.route("/info/<movie_id>")
def info(movie_id):
    response = f'{base_url}/movie/{movie_id}?api_key={api_key}'
    results = requests.get(response).json()
    reponse2 = f'{base_url}/movie/{movie_id}/credits?api_key={api_key}'
    results2 = requests.get(reponse2).json()
    response3 = f'{base_url}/movie/{movie_id}/reviews?api_key={api_key}'
    results3 = requests.get(response3).json()
    movie_info = {
        'movie_id' : movie_id,
        'movie_title' : results.get('title'),
        'plot' : results.get('overview'),
        'poster_path' : f'https://image.tmdb.org/t/p/w500/{results.get("poster_path")}',
        'release_date' : results.get('release_date'),
        'score' : results.get('vote_average'),
    }
    director_name = 'Not Available'
    for person in results2.get('crew'):
        if person['job'] == 'Director':
            director_name = person['name']
    movie_info['director'] = director_name

    cast = []
    for person in results2.get('cast'):
        if person['known_for_department'] == 'Acting':
            cast.append(person['name'])
    movie_info['cast'] = cast


    if results3['results'] != [ ]:
        first_review = results3['results'][0]
        movie_info['user_name'] = first_review['author']
        movie_info['user_review'] = first_review['content']
    else:
        first_review = None


    form = Review_form()
    if form.validate_on_submit():
        review = Review(movie_id=movie_id, user_id=current_user.id, review=form.review.data)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('info', movie_id=movie_id))

    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return render_template("review_page.html", data=movie_info, reviews=reviews, form=form, first_review=first_review)

@app.route('/add_review/<movie_id>', methods=['POST'])
@login_required
def add_review(movie_id):
    form = Review_form()
    if form.validate_on_submit():
        review = Review(movie_id=movie_id, user_id=current_user.id, review=form.review.data)
        db.session.add(review)
        db.session.commit()
        flash('Your review was added successfully!')
        return redirect(url_for('info', movie_id=movie_id))
    return render_template("review_page.html", form=form)


@app.route('/update_review/<review_id>', methods=['GET','POST'])
@login_required
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        return redirect(url_for('info', movie_id=review.movie_id))
    
    form = Review_form()
    if form.validate_on_submit():
        review.review = form.review.data
        db.session.commit()
        flash('You review was updated!')
        return redirect(url_for('info', movie_id=review.movie_id))
    else:
        form.review.data = review.review
    return render_template('update_review.html', form=form, review=review)

@app.route('/delete_review/<review_id>')
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        return redirect(url_for('info', movie_id=review.movie_id))

    db.session.delete(review)
    db.session.commit()
    flash('Your review has been deleted. ')
    return redirect(url_for('info', movie_id=review.movie_id))

@app.route('/search_route', methods=['GET','POST'])
def search_route():
    query = request.form.get('query') or request.args.get('query')
    filter_typ = request.args.get('filter_typ', "all")
    genre_id = request.args.get('genre')
    sort_opt = request.args.get('sort_opt')
    results = search.search(query, filter_typ, genre_id, sort_opt)
    return render_template('search.html', query=query, results=results)

@app.route("/details/<media_type>")
def details(media_type):
    title = request.args.get("title")
    overview = request.args.get("overview")
    rating = float(request.args.get("vote_average"))
    poster_path = request.args.get("poster_path")
    id = request.args.get("id")
    release_date = request.args.get("release_date")
    review = request.args.get("review")
    author = request.args.get("author")
    director = request.args.get("director")
    cast_json = request.args.get("cast")

    cast = json.loads(cast_json) if cast_json else []

    result = {
        'id': id,
        'title': title,
        'overview': overview,
        'rating': rating,
        'poster_path': poster_path,
        'release_date': release_date,
        'review': review,
        'author': author,
        'cast' : cast,
        'director': director,
        'type': media_type
    }
    print(result)
    return render_template('details.html', result=result, media_type=media_type)
# TV 
# @app.route('/add_review/<movie_id>', methods=['POST'])
# @login_required
# def add_review(movie_id):
#     form = Review_form()
#     if form.validate_on_submit():
#         review = Review(movie_id=movie_id, user_id=current_user.id, review=form.review.data)
#         db.session.add(review)
#         db.session.commit()
#         flash('Your review was added successfully!')
#         return redirect(url_for('info', movie_id=movie_id))
#     return render_template("review_page.html", form=form)


# @app.route('/update_review/<review_id>', methods=['GET','POST'])
# @login_required
# def update_review(review_id):
#     review = Review.query.get_or_404(review_id)
#     if review.user_id != current_user.id:
#         return redirect(url_for('info', movie_id=review.movie_id))
    
#     form = Review_form()
#     if form.validate_on_submit():
#         review.review = form.review.data
#         db.session.commit()
#         flash('You review was updated!')
#         return redirect(url_for('info', movie_id=review.movie_id))
#     else:
#         form.review.data = review.review
#     return render_template('update_review.html', form=form, review=review)

# @app.route('/delete_review/<review_id>')
# @login_required
# def delete_review(review_id):
#     review = Review.query.get_or_404(review_id)
#     if review.user_id != current_user.id:
#         return redirect(url_for('info', movie_id=review.movie_id))

#     db.session.delete(review)
#     db.session.commit()
#     flash('Your review has been deleted. ')
#     return redirect(url_for('info', movie_id=review.movie_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()