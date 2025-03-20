from django.urls import path
from .views import (HomePageView, AboutView, RegisterView, LoginView, LogoutView, ProfileView,
                   ProductIndexView, ProductView, ProductCreateView, ProductEditView, ProductDeleteView)

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('about', AboutView.as_view(), name="about"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/', ProfileView.as_view(), name="profile"),
    
    # Rutas de productos
    path('products/', ProductIndexView.as_view(), name="product_index"),
    path('products/create/', ProductCreateView.as_view(), name="product_create"),
    path('products/<slug:slug>/', ProductView.as_view(), name="product_detail"),
    path('products/<slug:slug>/edit/', ProductEditView.as_view(), name="product_edit"),
    path('products/<slug:slug>/delete/', ProductDeleteView.as_view(), name="product_delete"),
]