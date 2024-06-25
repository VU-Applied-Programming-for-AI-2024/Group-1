import sys
from tmdbv3api import TMDb, Movie, TV, Genre, Discover
from flask import Flask
from search import media_type, get_cast, director_name, sorting_it
app = Flask(__name__)


my_genre = Genre()
my_discover = Discover()
tmdb = TMDb()
tmdb.api_key = '46cbbac59c440a0b0490ad2adad2b849'
my_movie = Movie()
my_tv = TV()
def genre(filter_typ, genre_name, sort_opt):
    sys.stdout.reconfigure(encoding='utf-8')
    movie_genre = my_genre.movie_list()
    tv_genre = my_genre.tv_list()
    results = []
    if filter_typ == 'movie':
        for movie in movie_genre:
            if movie.name == genre_name:
                genre_id = movie.id       
                movie_results = my_discover.discover_movies({'with_genre':genre_id})
                results.extend(filter_genre(movie_results))
    elif filter_typ == 'tv':
         for tv in tv_genre:
            if tv.name == genre_name:
                genre_id = tv.id       
                tv_results = my_discover.discover_tv_shows({'with_genre':genre_id})
                results.extend(filter_genre(tv_results))
    if sort_opt:
        results = sorting_it(results, sort_opt)
    print(results)
    return results
def filter_genre(results):
    results_lst = [] 
    
    lst = ['title','overview','rating','poster_path','release_date','popularity', 'id','review','author','cast','director']
    id_lst = []
    for result in results:
        results_dct = {}
        if hasattr(result,"id"):
            id_lst.append(result.id)
        else:
            id_lst.append("does not have ID")
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
                elif hasattr(result, "first_air_date"):
                    results_dct[l] = result.first_air_date
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
                    
            if l == "author":
                for id in id_lst:
                    if media_type(id) == "movie" and hasattr(my_movie,'reviews'):
                        movie_review = my_movie.reviews(id)
                        for review in movie_review['results']:
                            for key, value in review.items():
                                if key == 'author':
                                    results_dct[l] = value
                    elif media_type(id) == "tv" and hasattr(my_tv,'reviews'):
                        tv_review = my_tv.reviews(id)
                        for review in tv_review['results']:
                            for key, value in review.items():
                                if key == 'author':
                                    results_dct[l] = value
                    else:
                        results_dct[l] = "Some Author"                    

            if l == "cast":
                for id in id_lst:
                    cast = get_cast(id)
                    results_dct[l] = cast
            if l == 'director':
                for id in id_lst:
                    direct = director_name(id)
                    results_dct[l] = direct
        results_lst.append(results_dct)
    return results_lst

