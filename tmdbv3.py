from tmdbv3api import TMDb, Movie, Genre

tmdb = TMDb()
tmdb.api_key = '1a674da5bbed27d22ed3a066a5899ca1'
tmdb.debug = True

movie = Movie()
popular = movie.popular()
popular_list = []

recommendations = movie.recommendations(movie_id=112)

#for recommendation in recommendations:
   # print(recommendation.title)
   # print(recommendation.overview)
    
for p in popular:
    popular_list.append(p)
    print(p)
    
#genre = Genre()
#genres = genre.movie_list()

#for g in genres:
   # print(g.id)
   # print(g.name)