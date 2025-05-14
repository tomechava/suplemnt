from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView, AboutView,
    RegisterView, LoginView, LogoutView, ProfileView, ProfileEditView,
    ProductIndexView, ProductCreateView, ProductView,
    ProductEditView, ProductDeleteView, LatestSupplementsView,
    TopSellersView, add_to_cart, remove_from_cart, clear_cart, CartView,
    OrderCreateView, OrderSuccessView, OrderDetailView
)

urlpatterns = [
    # PÁGINAS ESTÁTICAS
    path('', HomePageView.as_view(), name="home"),
    path('about/', AboutView.as_view(), name="about"),

    # AUTENTICACIÓN
    path('register/', RegisterView.as_view(), name="register"),
    path('login/',    LoginView.as_view(),    name="login"),
    path('logout/',   LogoutView.as_view(),   name="logout"),
    path('profile/',  ProfileView.as_view(),  name="profile"),
    path('profile/edit/', ProfileEditView.as_view(), name="profile_edit"),

    # PRODUCTOS
    path('products/',               ProductIndexView.as_view(),   name="product_index"),
    path('products/create/',        ProductCreateView.as_view(),  name="product_create"),
    path('products/<slug:slug>/',   ProductView.as_view(),        name="product_detail"),
    path('products/<slug:slug>/edit/',   ProductEditView.as_view(), name="product_edit"),
    path('products/<slug:slug>/delete/', ProductDeleteView.as_view(), name="product_delete"),
    path('latest/',           LatestSupplementsView.as_view(), name="latest"),
    path('top-sellers/',      TopSellersView.as_view(),        name="top_sellers"),

    # CARRITO
    path('cart/',          CartView.as_view(),            name='cart_view'),
    path('cart/add/<int:id>/', add_to_cart,              name='add_to_cart'),
    path('cart/remove/<int:id>/', remove_from_cart,           name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),  # Cambiado a remove_from_cart para limpiar el carrito

    # PEDIDOS
    path('order/create/',  OrderCreateView.as_view(),     name='order_create'),
    path('order/success/<int:order_id>/', OrderSuccessView.as_view(), name='order_success'),
    path('order/detail/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
]

if settings.DEBUG:  # Solo en modo de desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)