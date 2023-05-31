from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.generic import View, ListView, DetailView
from django.db.models import Q, Count, Sum, F
from .models import Movie, Actor, Category, Rating
from .forms import ReviewForm, RatingForm
from django.http import HttpResponse

User = get_user_model()


class MovieMixin:
    queryset = Movie.published.annotate(avg_rating=Sum(F('ratings__star')) / Count(F('ratings'))).all()


class MovieView(MovieMixin, ListView):
    model = Movie
    paginate_by = 8

    def get_queryset(self):
        return self.queryset.only("title", "poster", "url").order_by('-id')


class MovieDetailView(MovieMixin, DetailView):
    model = Movie
    slug_field = "url"

    def get_queryset(self):
        return self.queryset.defer("category_id", "draft", "url")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class AddReview(View):

    def post(self, request, pk):  # noqa

        # запрос закидываем в форму
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        user = User.objects.get(email=request.user.email)

        if form.is_valid():
            form = form.save(commit=False)
            # ключ parent - имя поля в input type="hidden"
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.user = user
            form.name = user.username
            form.email = user.email
            form.save()

        return redirect(movie.get_absolute_url())


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def post(self, request):  # noqa
        form = RatingForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            Rating.objects.update_or_create(
                ip=request.user.email,
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class ActorDetailView(DetailView):
    model = Actor
    slug_field = "name"


class FilterMoviesView(MovieMixin, ListView):
    paginate_by = 8

    def get_queryset(self):
        year = self.request.GET.get("year", "1970,2023")
        genre = self.request.GET.getlist("genre")
        mpaa = self.request.GET.getlist("mpaa")

        queryset = self.queryset.only("title", "poster", "url")

        try:
            year_start, year_end = year.split(",")
            queryset = self.queryset.only("title", "poster", "url").filter(year__range=(year_start, year_end))
        except ValueError as e:
            print(e)

        if mpaa and genre:
            return queryset.filter(genres__name__in=genre,
                                   mpaa_rating__in=mpaa).distinct().order_by("id")
        elif mpaa:
            return queryset.filter(mpaa_rating__in=mpaa).distinct().order_by("id")
        elif genre:
            return queryset.filter(genres__name__in=genre).distinct().order_by("id")
        else:
            return queryset.all().order_by("id")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = "year=%s&" % self.request.GET.get("year")
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        context["mpaa"] = ''.join([f"mpaa={x}&" for x in self.request.GET.getlist("mpaa")])
        return context

    class Meta:
        ordering = ["title"]


class Search(MovieMixin, ListView):
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get("search", '')
        return self.queryset.filter(Q(title__icontains=query) |
                                    Q(title__icontains=query.capitalize())
                                    ).only("title", "poster", "url").order_by('title')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search"] = f'search={self.request.GET.get("search")}&'
        return context

    class Meta:
        ordering = ["title"]


class CategoryMovies(MovieMixin, ListView):
    paginate_by = 8
    template_name = 'movies/category.html'

    def get_queryset(self):
        category_movies = self.queryset.only("title", "poster", "url").filter(
            category__url=self.kwargs['cat_name']).order_by('id')
        return category_movies

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryMovies, self).get_context_data(**kwargs)
        context["movies"] = context["object_list"]
        context["category"] = Category.objects.get(url=self.kwargs['cat_name'])
        return context

    class Meta:
        ordering = 'id'


def get_movies_rating(request):
    return render(request, "movies/include/movie_rating.html")


def index(request):
    return redirect("movies/")
