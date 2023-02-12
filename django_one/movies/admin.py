from django.utils.safestring import mark_safe
from django import forms
from django.contrib import admin
from .models import Movie, Category, Genre, Actor, MovieShots, Rating, RatingStar, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("name",)}
    list_display = ("name", "url",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "movie", "ip")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description",)
    list_display_links = ("name",)


class ReviewInline(admin.StackedInline):
    model = Reviews
    readonly_fields = ("name", "email", "parent")
    extra = 1


class ReviewTabular(admin.TabularInline):
    model = Reviews
    readonly_fields = ("name", "email", "parent")
    extra = 1

    # fieldsets = (
    #     (None, {
    #         "classes": ("collapse",),
    #         "fields": (("text", "name", "email", "parent"),)
    #     }),
    # )


class MovieShotsTabular(admin.TabularInline):
    model = MovieShots
    fields = ("title", "image")
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "draft")
    list_display_links = ("title",)

    search_fields = ("title", "category__name", "description")
    list_filter = ("category__name", "draft")

    # inlines = [ReviewTabular] # отзывы
    inlines = [MovieShotsTabular]
    save_on_top = True

    form = MovieAdminForm

    list_editable = ("draft",)
    prepopulated_fields = {"url": ("title",)}

    autocomplete_fields = ("actors", "directors")

    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email", "parent", "movie")

    list_display_links = ("name", )


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "get_shot_image", "image")

    search_fields = ("name",)

    list_display_links = ("name", "get_shot_image")

    fields = ("name", "birthday", "description", "image", "get_shot_image")
    readonly_fields = ("get_shot_image",)

    def get_shot_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=150 height=200>")

    get_shot_image.short_description = "Фото"


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "get_shot_image", "image")
    list_display_links = ("title", "get_shot_image")

    fields = ("title", "description", "image", "get_shot_image", "movie",)
    readonly_fields = ("get_shot_image",)

    list_filter = ("movie__title",)
    search_fields = ("movie__title",)

    autocomplete_fields = ("movie",)

    def get_shot_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=150 height=90>")

    get_shot_image.short_description = "Кадр"


# оставил чтобы помнить что так тоже можно
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Rating)
admin.site.register(RatingStar)

admin.AdminSite.site_header = "Администрирование Movies"
admin.AdminSite.index_title = "Панель администрирования"