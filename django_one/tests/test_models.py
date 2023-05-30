import datetime
import pytest
from movies.models import Category, Actor, Genre, MovieShots, Movie
from django.db import IntegrityError


MODEL_FIELDS = [
    [
        Category,
        [
            'name',
            'description',
            'url',
        ],
    ],
    [
        Actor,
        [
            'name',
            'birthday',
            'description',
            'image',
        ]
    ],
    [
        Genre,
        [
            'name',
            'description',
            'url',
        ],
    ],
    [
        MovieShots,
        [
            'title',
            'description',
            'image',
            'movie_id',
        ],
    ],
]


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestModels:
    @pytest.mark.parametrize(
        argnames=['model_name', 'expected_fields'], argvalues=MODEL_FIELDS
    )
    def test_model_fields(self, model_name, expected_fields):
        """Test user model specific fields"""
        model_fields = model_name._meta.fields
        for test_field in expected_fields:
            field = search_field(model_fields, test_field)
            assert (
                    field is not None
            ), f'Поле {test_field} не найдено в модели {model_name}'


@pytest.mark.django_db
class TestCategoryModel:
    """Тесты модели Category"""

    def test_category_count(self):
        assert Category.objects.count() == 0

    def test_category_constraints(self, category1):
        """Тест ограничений модели"""
        with pytest.raises(IntegrityError):
            Category.objects.create(name='Фильмы', description='Разные фильмы', url='movies')

    def test_get_category(self, category1):
        """Тест получения категории"""
        category = Category.objects.first()
        assert isinstance(category, Category)
        assert Category.objects.count() == 1

    def test_check_values(self, category1, category2):
        """Тест проверки значений"""
        assert category1.name == 'Фильмы'
        assert category1.url == 'movies'
        assert category2.name == 'Сериалы'
        assert category2.url == 'series'

    def test_model_team_str(self, category1, category2):
        """Тест метода __str__"""
        model_name = category1.__str__()
        series = category2.__str__()
        assert model_name == 'Фильмы'
        assert series == 'Сериалы'


@pytest.mark.django_db
class TestActorModel:
    """Тесты модели Actor"""

    def test_actor_count(self):
        assert Actor.objects.count() == 0

    def test_get_actor(self, actor1):
        """Тест получения категории"""
        actor = Actor.objects.first()
        assert isinstance(actor, Actor)
        assert Actor.objects.count() == 1

    def test_check_values(self, actor1):
        """Тест проверки значений"""
        assert actor1.name == 'ДиКаприо'
        assert actor1.birthday == datetime.date(1962, 8, 28)
        assert actor1.image == 'actors/fff.jpeg'

    def test_model_team_str(self, actor1):
        """Тест метода __str__"""
        model_name = actor1.__str__()
        assert model_name == 'ДиКаприо', 'Не правильный вывод метода __str__'


@pytest.mark.django_db
class TestGenreModel:
    """Тесты модели Genre"""

    def test_genre_count(self):
        assert Genre.objects.count() == 0

    def test_genre_constraints(self, genre1):
        """Тест ограничений модели"""
        with pytest.raises(IntegrityError):
            Genre.objects.create(name='Комедия', description='Жанр комедий', url='comedy')

    def test_get_genre(self, genre1):
        """Тест получения объекта"""
        genre = Genre.objects.first()
        assert isinstance(genre, Genre)
        assert Genre.objects.count() == 1, 'должен быть 1 объект'

    def test_check_values(self, genre1):
        """Тест проверки значений"""
        assert genre1.name == 'Комедия'
        assert genre1.url == 'comedy'

    def test_model_team_str(self, genre1):
        """Тест метода __str__"""
        model_name = genre1.__str__()
        assert model_name == 'Комедия'


@pytest.mark.django_db
class TestMovieShotsModel:
    """Тесты модели MovieShots"""

    def test_movie_shots_count(self):
        assert MovieShots.objects.count() == 0

    def test_get_movie_shots(self, movie_shots1):
        """Тест получения объекта"""
        movie_shots = MovieShots.objects.first()
        assert isinstance(movie_shots, MovieShots)
        assert MovieShots.objects.count() == 1, 'должен быть 1 объект'

    def test_check_values(self, movie_shots1, movie1):
        """Тест проверки значений"""
        assert movie_shots1.title == "k1"
        assert movie_shots1.description == "Кадр с осколком тарелки"
        assert movie_shots1.image == "movie_shots/x504.jpeg"
        assert movie_shots1.movie == movie1

    def test_model_team_str(self, movie_shots1):
        """Тест метода __str__"""
        model_name = movie_shots1.__str__()
        assert model_name == 'k1'


@pytest.mark.django_db
class TestMovieModel:
    """Тесты модели Movie"""
    def test_movie_shots_count(self):
        assert Movie.objects.count() == 0

    def test_get_movie(self, movie1):
        """Тест получения объекта"""
        movie = Movie.objects.first()
        assert isinstance(movie, Movie)
        assert Movie.objects.count() == 1, 'должен быть 1 объект'

    def test_check_values(self, movie1, category1):
        """Тест проверки значений"""
        assert movie1.title == "Бойцовский клуб"
        assert movie1.tagline == "«Интриги. Хаос. Мыло»"
        assert movie1.mpaa_rating == "NOT RATED"
        assert movie1.poster == "movies/p.jpeg"
        assert movie1.year == 1999
        assert movie1.country == "США"
        assert movie1.world_premiere == datetime.date(1999, 9, 10)
        assert movie1.budget == 63000000
        assert movie1.fees_in_usa == 37030102
        assert movie1.fess_in_world == 100853753
        assert movie1.category_id == category1.id
        assert movie1.url == "fight_club"
        assert movie1.draft is False

    def test_model_str(self, movie1):
        """Тест метода __str__"""
        model_name = movie1.__str__()
        assert model_name == 'Бойцовский клуб'

