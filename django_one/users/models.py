from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('Email'), unique=True)

    email_verify = models.BooleanField(_('Email верифицирован'), default=False,
                                       help_text="Указывает, что пользователь подтвердил электронную почту.")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
