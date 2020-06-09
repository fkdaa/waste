from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from . import forms

from django.views.generic import TemplateView,CreateView # 追記
from django.contrib.auth.forms import UserCreationForm  # 追記
from django.urls import reverse_lazy # 追記

class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "logout.html"

class IndexView(TemplateView):
    template_name = "index.html"

# 追記
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "create.html"
    success_url = reverse_lazy("login")