from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, FormView
from django.contrib import messages

from .models import ContactLink, About
from .forms import ContactForm


class ContactView(FormView):
    form_class = ContactForm
    success_url = "/"
    template_name = 'contact/contact.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            obj = form.save(commit=False)
            obj.email = self.request.user.email
            obj.save()
            messages.success(self.request, 'Спасибо за отзыв. Мы ответим Вам в ближайшее время.')
        else:
            messages.error(self.request, "Комментарии могут оставлять только зарегистрированные пользователи")
            return redirect('/users/login')
        return super().form_valid(form)


class CreateContact(CreateView):
    form_class = ContactForm
    success_url = "/"


class AboutView(View):

    @staticmethod
    def get(request):
        about = About.objects.all()
        return render(request, 'contact/about.html', {"about": about})

