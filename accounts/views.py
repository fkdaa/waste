from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from . import forms
from django.utils import timezone

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

from django.views.generic import TemplateView,CreateView # 追記
from django.contrib.auth.forms import UserCreationForm  # 追記
from django.urls import reverse_lazy # 追記

from app.models import User
from app.models import UserLog


class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"


@receiver(user_logged_in)
#ログイン時に呼び出し
def user_logged_in_callback(sender, request, user, **kwargs):
    UserLog.objects.create(target=user,timestamp=timezone.datetime.now(),label="login")



class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"

@receiver(user_logged_out)
#ログアウト時に呼び出し
def user_logged_out_callback(sender, request, user, **kwargs):
    UserLog.objects.create(target=user,timestamp=timezone.datetime.now(),label="logout")


class IndexView(TemplateView):
    template_name = "app/index.html"

# 追記
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/create.html"
    success_url = reverse_lazy("login")