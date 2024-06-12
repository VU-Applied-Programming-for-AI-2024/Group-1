import sys
from tmdbv3api import TMDb, Movie
def movies_search(movie_name:str):
    tmdb = TMDb()
    tmdb.api_key = '46cbbac59c440a0b0490ad2adad2b849'
    my_movie = Movie()
    results = my_movie.search(movie_name)
    sys.stdout.reconfigure(encoding='utf-8')
    for i in results:
    #     results_dict = results.__dict__
    #     for key, value in results_dict.items():
    #         if key == "_json":
    #             for akey, avalue in value.items():
    #                 if type(avalue) == list:
    #                     for j in avalue:
    #                         for key1, value1 in j.items():
    #                             return ''
        print(i.title, i.realsea)
movies_search('Godzilla')