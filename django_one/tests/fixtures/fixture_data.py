import datetime

import pytest
from movies.models import Category, Actor, Genre, MovieShots, Movie


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='Tester',
        first_name='',
        last_name='',
        email='test.user@fake.mail',
        password='12345Qq',
    )


@pytest.fixture
def category1():
    return Category.objects.create(name='Фильмы', description='Разные фильмы', url='movies')


@pytest.fixture
def category2():
    return Category.objects.create(name='Сериалы', description='Разные сериалы', url='series')


@pytest.fixture
def actor1():
    return Actor.objects.create(name='ДиКаприо',
                                birthday=datetime.date(1962, 8, 28),
                                description='О персоне\r\n\r\nКарьера\r\nРежиссер, Продюсер, Актер',
                                image='actors/fff.jpeg')


@pytest.fixture
def genre1():
    return Genre.objects.create(name='Комедия', description='Жанр комедий', url='comedy')


@pytest.fixture
def movie1(actor1, genre1, category1):
    return Movie.objects.create(
        title="Бойцовский клуб",
        tagline="«Интриги. Хаос. Мыло»",
        mpaa_rating="NOT RATED",
        description='<p>Терзаемый хронической бессонницей и отчаянно пытающийся вырваться из мучительно скучной'
                    ' жизни клерк встречает некоего Тайлера Дардена, харизматического торговца мылом с извращенной'
                    ' философией. Тайлер уверен, что самосовершенствование &mdash; удел слабых, а саморазрушение '
                    '&mdash; единственное, ради чего стоит жить.</p>\r\n\r\n<p><iframe frameborder="0" height="360"'
                    ' src="https://www.youtube.com/embed/oqHJp_ZZdU4?rel=0" width="640"></iframe></p>',
        poster="movies/p.jpeg",
        year=1999,
        country="США",
        world_premiere=datetime.date(1999, 9, 10),
        budget=63000000,
        fees_in_usa=37030102,
        fess_in_world=100853753,
        category=category1,
        url="fight_club",
        draft=False
    )


@pytest.fixture
def movie_shots1(movie1):
    return MovieShots.objects.create(title="k1", description="Кадр с осколком тарелки",
                                     image="movie_shots/x504.jpeg", movie=movie1)
