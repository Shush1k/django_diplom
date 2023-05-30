from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'movies'

urlpatterns = [
    path("", views.index),
    path("movies/", views.MovieView.as_view(), name="movies"),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name="search"),
    path("movies-top/", views.get_movies_rating, name="movies_top"),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("category/<str:cat_name>/", views.CategoryMovies.as_view(), name="catt"),
    # путь выше имеет атрибут name="catt", который может использоваться в модели, как get_absolute_url
    # или же вместо этого используя тэг {% 'url' %} в шаблонах
    path("movie/<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    # cache_page(180)
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorDetailView.as_view(), name="actor_detail"),
]
