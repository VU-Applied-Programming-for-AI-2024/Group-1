import sys
from tmdbv3api import TMDb, Movie, TV, Genre
from flask import Flask
app = Flask(__name__)


tmdb = TMDb()
tmdb.api_key = '46cbbac59c440a0b0490ad2adad2b849'
my_movie = Movie()
my_tv = TV()
def search(query, filter_typ, genre_id, sort_opt):
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


    return results


def search_results(results, typ):
    results_lst = [] 
    
    lst = ['title','overview','rating','poster_path','release_date','popularity']

    for result in results:
        results_dct = {}
        for l in lst:
            if l == "title":
                if hasattr(result,'title'):
                    results_dct[l] = result.title
                elif hasattr(result,'name'):
                    results_dct[l] = result.name    
            
            if l == "overview":
                if hasattr(result,'overview'):
                    results_dct[l] = result.overview
                else:
                    results_dct[l] = 'Overview not available'
            
            if l == "rating":
                if hasattr(result,'vote_average'):
                    results_dct[l] = result.vote_average
                else:
                    results_dct[l] = "Rating not available"

            if l == "poster_path":
                if hasattr(result, 'poster_path'):
                    results_dct[l] = result.poster_path
                else:
                    results_dct[l] = 'Poster not available'
            if l == "release_date":
                if hasattr(result,'release_date'):
                    results_dct[l] = result.release_date
                else:
                    results_dct[l] = 'Release date not available'
            if l == "popularity":
                if hasattr(result,'popularity'):
                    results_dct[l] = result.popularity
                else:
                    results_dct[l] = 'Popularity not available'
        results_dct["type"] = typ
        results_lst.append(results_dct)
    return results_lst
def filter_genre(results, genre_id):
    filtered_lst = []
    for result in results:
        if hasattr(result,'genre_ids'):
            if genre_id == result.genre_ids:
                filtered_lst.append(result)
    return filtered_lst
def sorting_it(results, sort_by):
    if sort_by == 'popularity':
        results.sort(key=lambda x: x['popularity'], reverse=True)
    elif sort_by == 'vote_average':
        results.sort(key=lambda x: x['vote_average'], reverse=True)
    elif sort_by == 'release_date':
        results.sort(key=lambda x: x['release_date'])
    return results

