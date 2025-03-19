from django.urls import path
from .views import (HomePageView, AboutView, RegisterView, LoginView, LogoutView, ProfileView)

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('about', AboutView.as_view(), name="about"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/', ProfileView.as_view(), name="profile"),
]