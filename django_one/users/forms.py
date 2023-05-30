from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (UserCreationForm as DjUserCreationForm,
                                       AuthenticationForm as DjAuthenticationForm, UsernameField)
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.utils import send_email

User = get_user_model()


class AuthenticationForm(DjAuthenticationForm):
    username = UsernameField(label=_("Email"),
                             widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control col-sm-3',
                                                           "placeholder": "example@gmail.com"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form-control col-sm-3',
                                          "placeholder": "Password"}),
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

            if not self.user_cache.email_verify:
                send_email(self.request, self.user_cache)
                raise ValidationError(
                    "Email не верифицирован, проверьте почту!",
                    code="invalid_login",
                )

        return self.cleaned_data


class UserCreationForm(DjUserCreationForm):
    username = forms.CharField(label="Имя пользователя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control col-sm-3'}))

    email = forms.EmailField(label=_("Email"),
                             max_length=254,
                             widget=forms.EmailInput(attrs={
                                 'autocomplete': 'email',
                                 'class': 'form-control col-sm-3'
                             }))

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-control col-sm-3'}),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-control col-sm-3'}),
    )

    class Meta(DjUserCreationForm.Meta):
        model = User
        fields = ('username', "email",)
