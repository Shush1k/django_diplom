from ckeditor.fields import RichTextField
from django.db import models


class Contact(models.Model):
    """ Класс модели обратной связи"""
    timestamp = models.DateTimeField(auto_now_add=True)
    topic = models.CharField("Заголовок", max_length=100)
    email = models.EmailField("Email", max_length=130)
    message = models.TextField("Сообщение", max_length=5000)

    def __str__(self):
        return f"{self.topic[:30]} - {self.email}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class ContactLink(models.Model):
    """ Класс модели контактов """
    icon = models.FileField(upload_to="icons/")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class About(models.Model):
    author_name = models.CharField(max_length=100)
    # TODO продумать, что должна отражать страница об авторе
    # TODO и как использовать это все в админке
    text = RichTextField()
    mini_text = RichTextField()
