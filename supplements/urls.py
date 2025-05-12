from django.urls import path
from .views import (
    HomePageView, AboutView,
    RegisterView, LoginView, LogoutView, ProfileView,
    ProductIndexView, ProductCreateView, ProductView,
    ProductEditView, ProductDeleteView, LatestSupplementsView,
    TopSellersView, add_to_cart, CartView
)

# NO hace falta app_name aquí si no vas a usar namespace
urlpatterns = [
    # ——— PÁGINAS ESTÁTICAS ———
    path('', HomePageView.as_view(), name="home"),
    path('about/', AboutView.as_view(), name="about"),

    # ——— AUTENTICACIÓN ———
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/', ProfileView.as_view(), name="profile"),

    # ——— PRODUCTOS ———
    path('products/', ProductIndexView.as_view(), name="product_index"),
    path('products/create/', ProductCreateView.as_view(), name="product_create"),
    path('products/<slug:slug>/', ProductView.as_view(), name="product_detail"),
    path('products/<slug:slug>/edit/', ProductEditView.as_view(), name="product_edit"),
    path('products/<slug:slug>/delete/', ProductDeleteView.as_view(), name="product_delete"),
    path('latest/', LatestSupplementsView.as_view(), name='latest'),
    path('top-sellers/', TopSellersView.as_view(), name='top_sellers'),

    # ——— CARRITO ———
    path('cart/',  CartView.as_view(), name='cart_view'),
    path('cart/add/<int:id>/',  add_to_cart, name='add_to_cart'),
]
