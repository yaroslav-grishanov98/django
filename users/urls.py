from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserRegisterView, UserLoginView, UserProfileView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:index'), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
