from django import forms
from .models import Rating, RatingStar, Reviews


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews

        # поля модели в форме
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):

    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect, empty_label=None)

    class Meta:
        model = Rating
        
        fields = ("star", )