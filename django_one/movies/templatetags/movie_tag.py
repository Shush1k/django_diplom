from django import template
from django.db.models import Avg
from django.shortcuts import render

from movies.models import Category, Genre, Movie, Rating


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_genres():
    return Genre.objects.all()


@register.simple_tag()
def get_years():
    return Movie.published.values("year").distinct()


@register.simple_tag()
def get_rating(max_=10):
    return Rating.objects.values('movie__title', 'movie__url', 'movie__poster').annotate(avg=Avg('star')).order_by('-avg')[:max_]


@register.simple_tag()
def get_mpaa():
    return Movie.MPAA.choices


@register.simple_tag()
def get_user_vote_rating(ip, movie_id):
    return Rating.objects.filter(ip=ip, movie__id=movie_id).values_list('star_id', flat=True)


@register.filter()
def is_numeric(value):
    return isinstance(value, (int, float))
