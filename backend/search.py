import sys
from tmdbv3api import TMDb, Movie, TV 
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

tmdb = TMDb()
tmdb.api_key = '46cbbac59c440a0b0490ad2adad2b849'
my_movie = Movie()
my_tv = TV()
sys.stdout.reconfigure(encoding='utf-8')
class SearchLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(255), nullable=False)
    search_type = db.Column(db.String(50), nullable=False)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(200), nullable=False)
    results = db.Column(db.JSON, nullable=False)

    def __repr__(self) -> str:
        return  f"<SearchHistory(query='{self.query}', results='{self.results}')>"

with app.app_context():
    db.create_all()

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    filter_typ = request.args.get('filter')
    genre_id = request.args.get('genre')
    sort_opt = request.args.get('sort_by')

    results = []
    sys.stdout.reconfigure(encoding='utf-8')
    results = []
    if filter_typ == "movie" or filter_typ == "all":
        movie_results = my_movie.search(query)
        results.extend(search_results(movie_results,filter_typ))
    if filter_typ == "tv" or filter_typ == "all":
        tv_results = my_tv.search(query)
        results.extend(search_results(tv_results,filter_typ))
    if genre_id:
        results = filter_genre(results, genre_id)  
    if sort_opt:
        results = sorting_it(results, sort_opt)  

    search_entry = SearchHistory(query=query, results=results)
    db.session.add(search_entry)
    db.session.commit()

    return jsonify(results)


def search_results(results, typ):
    results_lst = [] 
    
    lst = ['title','overview','rating','poster_path']

    for result in results:
        results_dct = {}
        for l in lst:
            if l == "title":
                if typ == "movie":
                    results_dct[l] = result.title
                else:
                    results_dct[l] = result.name
            if l == "overview":
                results_dct[l] = result.overview
            if l == "rating":
                results_dct[l] == result.vote_average
            if l == "poster_path":
                results_dct[l] = result.poster_path
        results_dct["type"] = typ
        results_lst.append(results_dct)
    return results_lst
def filter_genre(results, genre_id):
    filtered_lst = []
    for result in results:
        if genre_id == result.genre_ids:
            filtered_lst.append(result)
    return filtered_lst
def sorting_it(results, sort_by):
    if sort_by == 'date':
        return sorted(results, key=lambda x: x['release_date'], reverse=True)
    elif sort_by == 'rating':
        return sorted(results, key=lambda x: x['rating'], reverse=True)
    return results

