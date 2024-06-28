# Movie Matrix
![The landing page](/readme-assets/Screenshot%202024-06-28%20at%2018.15.28.png)
The <a href="https://group1112-c247f6969d92.herokuapp.com/">link</a> to the project.

## Brief description of the project
The aim of the project is to provide a simple, minimalistic web application to allow users to explore movies and tv shows and provide information about(plot, release date, director, etc)them along with opinions of what other people who have watched them think about it and to add to them by adding their own reviews to the titles of their choice. This website is for everyone, from people who are looking for suggestions for their next movie marathon or people who simply want to share their opinion about what they have watched. 

## Frontend 
![Wireframe](/readme-assets/New%20Wireframe%201.png)
![Home page](/readme-assets/Screenshot%202024-06-28%20at%2018.15.28.png)
![Movie info](/readme-assets/Screenshot%202024-06-28%20at%2022.50.24.png)
![reviews](/readme-assets/Screenshot%202024-06-28%20at%2022.50.28.png)
![reviews-user](/readme-assets/Screenshot%202024-06-28%20at%2022.51.00.png)



## Colour pallete
![Colour Pallete](/readme-assets/Screenshot%202024-06-28%20at%2021.38.35.png)


<hr>

## Team members
- Kartik Patil
- Jacob Raphael
- Yash Tyagi
## Installation details
The project was deployed using Heroku and the PostgreSQL database is from ElephantSQL (The [link](https://group1112-c247f6969d92.herokuapp.com/) to the project if you want to just try it.) Unfortunately, ElephantSQL will be out of service next year and is not open to new users so we recommend using other services like AWS (We have access to the server till next year so we decided to use it). The steps are similar. 

### Requirements(general)
Follow these guidelines based on deployment.
1. Install all the dependencies. These are listed in the file `requirements.txt`. You can install them using `pip install -r requirements.txt`.
2. Install dotenv to import environment variables into app.py. The command `pip install python-dotenv`. To import variables from the .env file, simply use the command `os.getenv('VAR_NAME')`
3. Get an API_KEY from [TMDB](https://developer.themoviedb.org/docs/getting-started).
4. On your database hosting service, create a new database instance and get the URL of the database. Add it to the .env file.
5. Create a SECRET_KEY for the flask app. Store it in the .env file and import it into the app.py file. Add it to the .env file. 

### Local
- Clone the repository using `git clone https://github.com/VU-Applied-Programming-for-AI-2024/Group-1.git`. 
- To run it locally, fulfil the requiremets. 
- The app.py file contains the essential code. To run the app, use the `python3 app.py` command to run the application.

To deploy your own Heroku app using this repository. 
### Database hosting(ElephantSQL) 
- Signup for a database hosting service. 
- Create an instance for the database that will be used in this project. 
- Get the URL of this database and add it to the .env file and import it into app.py. 

### Heroku
- Create a Procfile in your root branch with the command: `web: gunicorn app:app` where the first app is the name of the flask file you are using. This file has to be in the root of the directory. 
- Have a `runtime.txt ` with your desired python version. 
- Make sure the files mentioned aboved(app.py, requirements.txt, runtime.txt, Procfile, and .env) are in the same folder.
- Push these changes to Github. 
- Signup for a Heroku account. 
- On your Heroku dashaboard, click on `New` and then `Create new app`. 
- Once you have given it a name and selected your region, go to settings and add your environment variables from above as `config vars`(the key and value are not to be in quotes).
- Make sure there is a build pack present. 
- Go to `Deploy` and deploy using `Github` or `Heroku Git`. (For this project we deployed using Heroku Git but using Github is a reliable option).
- Follow the instructions provided by the options. For `Heroku Git ` use the command `git push Heroku master` if your primary branch is called master. 


## Architecture
![The architecture](/readme-assets/Untitled%20Diagram.drawio-2.png)

### Limitations
- The tv title information does not work well. You might get information about movies instead.
- Search results when provided with random words will provide cards with titles that have title of a string object. 

### Future implementation
- Like/Watchlist feature for registred users.
- User dashboard with lists of their reviews and their likes/watchlist items.
