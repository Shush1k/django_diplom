from django.contrib import admin
from django.db import models
from django.urls import reverse
from datetime import date, datetime
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "5. Категории"

    def get_absolute_url(self):
        return reverse('movies:catt', kwargs={"cat_name": self.url})


class Actor(models.Model):
    """Актеры и режиссеры"""
    name = models.CharField("Имя", max_length=100)
    birthday = models.DateField("Дата рождения")
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:actor_detail', kwargs={"slug": self.name})

    @admin.display(description='Участие в')
    def movies_list(self):
        return ", ".join(list(self.film_actor.all().values_list('title', flat=True)))

    def age(self):
        if self.birthday:
            return int((datetime.now().date() - self.birthday).days / 365.25)
        return None

    age.short_description = "Возраст"
    age_property = property(age)

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "4. Актеры и режиссеры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "3. Жанры"


class PublishedMovieManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(draft=False)


class Movie(models.Model):
    """Фильм"""
    class MPAA(models.TextChoices):
        G = 'G', 'G'
        PG = 'PG', 'PG'
        PG_13 = 'PG-13', 'PG-13'
        R = 'R', 'R'
        NC_17 = 'NC-17', 'NC-17'
        NOT_RATED = 'NOT RATED', 'NOT RATED'
        UNRATED = 'UNRATED', 'UNRATED'

    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    mpaa_rating = models.CharField("MPAA", choices=MPAA.choices, max_length=10, default=MPAA.NOT_RATED)
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/", null=True, blank=True,
                               default="movies/no_movie_image.png")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2022)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(
        Actor, verbose_name="режиссеры", related_name="film_director")
    actors = models.ManyToManyField(
        Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0,
                                         help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True, db_index=True, verbose_name="URL")
    draft = models.BooleanField("Черновик", default=False)

    objects = models.Manager()  # default менеджер
    published = PublishedMovieManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # передаем из urls: name и параметры, т.е. slug
        return reverse("movies:movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.prefetch_related("user").filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "1. Фильмы"
        indexes = [
            models.Index(fields=['title']),
        ]


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание", null=True)
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "2. Кадры из фильма"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    text = models.TextField("Сообщение", max_length=150)
    created = models.DateTimeField("Дата", auto_now_add=True)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.movie}"

    def children(self):
        return Reviews.objects.select_related("user").filter(parent=self)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "6. Отзывы"

        ordering = ['-created']
