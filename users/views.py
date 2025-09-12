from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import User


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        user = form.save()

        login(self.request, user)

        send_mail(
            'Регистрация прошла успешно',
            f'Добро пожаловать, {user.email}! Ваш аккаунт успешно создан.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        messages.success(self.request, 'Вы успешно зарегистрированы!')

        return redirect(self.success_url)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        messages.success(self.request, 'Вы успешно вошли!')
        return reverse_lazy('catalog:index')


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)
