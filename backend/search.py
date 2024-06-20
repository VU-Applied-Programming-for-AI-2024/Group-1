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

def media_type(id):
    try:

        my_movie.details(id)
        return "movie"
    
    except:
        pass
    try:

        my_tv.details(id)
        return "tv"
    
    except:
        pass
    
    return "unknown"
def search_results(results, typ):
    results_lst = [] 
    
    lst = ['title','overview','rating','poster_path','release_date','popularity', 'id','review']
    id_lst = []
    for result in results:
        results_dct = {}
        id_lst.append(result.id)
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
            if l == 'id':
                if hasattr(result,'id'):
                    results_dct[l] = result.id
                else:
                    results_dct[l] = 'Id not avalaible'
            if l == 'review':
                for id in id_lst:
                    if media_type(id) == "movie" and hasattr(my_movie,'reviews'):
                        movie_review = my_movie.reviews(id)
                        for review in movie_review['results']:
                            for key, value in review.items():
                                if key == 'content':
                                    results_dct[l] = value
                    elif media_type(id) == "tv" and hasattr(my_tv,'reviews'):
                        tv_review = my_tv.reviews(id)
                        for review in tv_review['results']:
                            for key, value in review.items():
                                if key == 'content':
                                    results_dct[l] = value

                    else:
                        results_dct[l] = 'review not available'
        
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

