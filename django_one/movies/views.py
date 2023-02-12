from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View, ListView, DetailView
from django.db.models import Q
from .models import Movie, Actor, Genre, Category
from .forms import ReviewForm, RatingForm


class MovieMixin:
    queryset = Movie.objects.filter(draft=False)

    # @staticmethod
    # def get_published_movies():
    #     return Movie.objects.filter(draft=False)


class MovieView(MovieMixin, ListView):
    model = Movie
    paginate_by = 3

    def get_queryset(self):
        return self.queryset.order_by('-id')


class MovieDetailView(MovieMixin, DetailView):
    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context

    def __str__(self):
        return '%s ___ %s' % (self.title, self.tagline)


class AddReview(View):

    def post(self, request, pk):

        # запрос закидываем в форму
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)

        if form.is_valid():
            form = form.save(commit=False)
            # ключ parent - имя поля в input type="hidden"
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()

        return redirect(movie.get_absolute_url())


class ActorDetailView(DetailView):
    model = Actor
    slug_field = "name"


class FilterMoviesView(MovieMixin, ListView):
    paginate_by = 3

    def get_queryset(self):
        if self.request.GET.getlist("year") and self.request.GET.getlist("genre"):
            return self.queryset.filter(year__in=self.request.GET.getlist("year"),
                                        genres__name__in=self.request.GET.getlist("genre")).distinct().order_by("id")
        elif self.request.GET.getlist("year"):
            return self.queryset.filter(year__in=self.request.GET.getlist("year")).distinct().order_by("id")
        elif self.request.GET.getlist("genre"):
            return self.queryset.filter(genres__name__in=self.request.GET.getlist("genre")).distinct().order_by("id")
        else:
            return self.queryset.all().order_by("id")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context

    class Meta:
        ordering = ["title"]


class Search(MovieMixin, ListView):
    paginate_by = 4

    def get_queryset(self):
        # icontains - проблемы с русскими символами в Sqlite
        return self.queryset.filter(Q(title__icontains=self.request.GET.get("search")) |
                                    Q(title__startswith=self.request.GET.get("search").capitalize()) |
                                    Q(title__startswith=self.request.GET.get("search")) |
                                    Q(title__icontains=self.request.GET.get("search").upper())).order_by("id")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search"] = f'search={self.request.GET.get("search")}&'
        return context

    class Meta:
        ordering = ["title"]


def get_category_movies(request, cat_name):
    cat_movies = Movie.objects.filter(category__url=cat_name, draft=False)
    cat_n = Category.objects.get(url=cat_name)
    # точно можно сделать как-то по-другому через select related и уменьшить кол-во запросов

    return render(request, "movies/category.html", {"category_movies": cat_movies, "category": cat_n})


def index(request):
    return redirect("movies/")
