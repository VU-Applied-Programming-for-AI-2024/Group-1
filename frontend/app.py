from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
class User(db.Model, UserMixin):
    """
    columns for table of users in database
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False) # Note: 80 max length here and 20 in registration form because database takes in
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
        
        if user and bcrypt.check_password_hash(user.password, password.data) == False:
            flash("Your password is incorrect")
            raise ValidationError("Invalid Password")
        

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/genre")
def genre():
    return render_template("genre.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
     
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
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