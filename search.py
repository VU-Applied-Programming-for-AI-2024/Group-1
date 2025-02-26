import sys
from tmdbv3api import TMDb, Movie, TV
from typing import List, Dict, Any

tmdb = TMDb()
tmdb.api_key = '46cbbac59c440a0b0490ad2adad2b849'
my_movie = Movie()
my_tv = TV()
def search(query, filter_typ, sort_opt) -> List[Dict[str,Any]]:
    """
    param: query : A string which would be name of a movie or tv show that the user wants to search for 
    param: filter_typ : A string through which the user can filter if they want to see only movies or only tv shows
    param: sort_opt : A string through which the user can sort the search results based on rating, popularity, and realease date
    reutrn: The function returns a list that contains a dictionary and with the dictionary conytaining details about the search
    """
    sys.stdout.reconfigure(encoding='utf-8')
    results: List[Dict[str,Any]] = []
    if filter_typ in ['movie', 'all']:
        movie_results: List = my_movie.search(query)
        results.extend(search_results(movie_results, filter_typ))
    if filter_typ in ['tv', 'all']:
        tv_results: List = my_tv.search(query)
        results.extend(search_results(tv_results, filter_typ))
    if sort_opt:
        results: List = sorting_it(results, sort_opt)


    return results  


def media_type(id) -> str:
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

def get_cast(id) -> List[str]:
    cast_list: List[str] = []
    if media_type(id) == 'movie':
        try:
            movie_credit: Dict[str, List[Any]] = my_movie.credits(id)
            for member in movie_credit['cast']:
                cast_list.append(member.name)
        except:
            cast_list.append('Cast not available')
    elif media_type(id) == "tv":
        try:
            tv_credit = my_tv.credits(id)
            for member in tv_credit['cast']:
                cast_list.append(member.name)
        except:
            cast_list.append('Cast not available')
    return cast_list

def director_name(id) -> str:
    if media_type(id) == 'movie':
        try: 
            movie_cred: Dict[str,] = my_movie.credits(id)
            for member in movie_cred['crew']:
                if member['job'] == 'Director':
                    return member['name']
        except:
            return 'Director name not available'
    elif media_type(id) == 'tv':
        try:
            tv_cred = my_tv.credits(id)
            for member in tv_cred['crew']:
                if member['job'] == 'Director':
                    return member['name']
        except:
            return 'Director name not available'
def search_results(results, typ) -> List[Dict[str,Any]] :
    results_lst: List[Dict[str,Any]] = [] 
    
    lst: List[str] = ['title','overview','rating','poster_path','release_date','popularity', 'id','review','author','cast','director']
    id_lst: List[int] = []
    for result in results:
        results_dct: Dict = {}
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
                    results_dct[l] = 0.0

            if l == "poster_path":
                if hasattr(result, 'poster_path'):
                    results_dct[l] = result.poster_path
                else:
                    results_dct[l] = 'Poster not available'
            if l == "release_date":
                if hasattr(result,'release_date'):
                    results_dct[l] = result.release_date
                else:
                    results_dct[l] = '0000-00-00'
            if l == "popularity":
                if hasattr(result,'popularity'):
                    results_dct[l] = result.popularity
                else:
                    results_dct[l] = 0.0
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
        results_dct["type"] = typ
        results_lst.append(results_dct)
    return results_lst
    
def sorting_it(results, sort_by) -> List[Dict[str, Any]]:
    if sort_by == 'popularity':
        results.sort(key=lambda x: x['popularity'], reverse=True)
    elif sort_by == 'vote_average':
        results.sort(key=lambda x: x['rating'], reverse=True)
    elif sort_by == 'release_date':
        results.sort(key=lambda x: x['release_date'])
    return results