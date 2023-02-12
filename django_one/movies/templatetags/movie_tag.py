from django import template

from movies.models import Category, Genre, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_genres():
    return Genre.objects.all()


@register.simple_tag()
def get_years():
    return Movie.objects.filter(draft=False).values("year").distinct()
