from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, ValidationError, EqualTo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False) # Note: 80 max length here and 20 in registration form because database takes in
                                                        # hashed version of password which is usually longer
    
class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    email = StringField('Email', validators=[InputRequired(), Email()],
                        render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    
    submit = SubmitField("Register")
    
    def validate_username(self, username):
        existing_username = User.query.filter_by(
            username=username.data).first()

        if existing_username:
            raise ValidationError(
                "This username already exists."
            )
            
    def validate_email(self, email):
        existing_email = User.query.filter_by(
            email=email.data).first()
        
        if existing_email:
            raise ValidationError(
                "This email is already registered."
            )
            
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "password"})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/genre")
def genre():
    return render_template("genre.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
     
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created, you are now able to login.')
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route("/info")
def info():
    return render_template("review_page.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)