from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm, SupplementForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Supplement, Category
from django.utils.text import slugify


# Create your views here.
class HomePageView(View):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name)


class AboutView(View):
    template_name = "about.html"

    def get(self, request):
        return render(request, self.template_name)


# USERS VIEWS:
class RegisterView(View):
    template_name = "users/register.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión después del registro
            return redirect("home")  # Cambia "home" por tu vista de inicio

        # Si el formulario no es válido, vuelve a renderizar la página con los errores
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "users/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(
                request, username=username, password=password
            )  # Autenticar usuario

            if user is not None:
                login(request, user)  # Iniciar sesión
                return redirect("home")  # Redirigir a la página principal

            else:
                form.add_error(
                    None, "Invalid username or password"
                )  # Mostrar error en el formulario

        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(
            "login"
        )  # Redirige a la página de login después de cerrar sesión


class ProfileView(LoginRequiredMixin, View):
    template_name = "users/profile.html"

    def get(self, request):
        return render(request, self.template_name, {"user": request.user})


# SUPPLEMENTS VIEWS:
class ProductIndexView(View):
    template_name = "supplements/product_index.html"

    def get(self, request):
        supplements = Supplement.objects.filter(is_active=True)
        categories = Category.objects.all()

        # Filtrar por categoría si se proporciona
        category_slug = request.GET.get("category")
        if category_slug:
            supplements = supplements.filter(category__slug=category_slug)

        context = {
            "supplements": supplements,
            "categories": categories,
            "selected_category": category_slug,
        }
        return render(request, self.template_name, context)


class ProductView(View):
    template_name = "supplements/product.html"

    def get(self, request, slug):
        supplement = get_object_or_404(Supplement, slug=slug, is_active=True)
        related_products = Supplement.objects.filter(
            category=supplement.category
        ).exclude(id=supplement.id)[
            :4
        ]  # Mostrar 4 productos relacionados

        context = {"supplement": supplement, "related_products": related_products}
        return render(request, self.template_name, context)


class ProductCreateView(LoginRequiredMixin, View):
    template_name = "supplements/product_edit.html"

    def get(self, request):
        form = SupplementForm()
        context = {"form": form, "is_edit": False, "title": "Crear Nuevo Suplemento"}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SupplementForm(request.POST, request.FILES)
        if form.is_valid():
            supplement = form.save(commit=False)
            supplement.slug = slugify(supplement.name)
            supplement.save()
            return redirect("product_detail", slug=supplement.slug)

        context = {"form": form, "is_edit": False, "title": "Crear Nuevo Suplemento"}
        return render(request, self.template_name, context)


class ProductEditView(LoginRequiredMixin, View):
    template_name = "supplements/product_edit.html"

    def get(self, request, slug):
        supplement = get_object_or_404(Supplement, slug=slug)
        form = SupplementForm(instance=supplement)
        context = {
            "form": form,
            "is_edit": True,
            "supplement": supplement,
            "title": f"Editar: {supplement.name}",
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        supplement = get_object_or_404(Supplement, slug=slug)
        form = SupplementForm(request.POST, request.FILES, instance=supplement)
        if form.is_valid():
            form.save()
            return redirect("product_detail", slug=supplement.slug)

        context = {
            "form": form,
            "is_edit": True,
            "supplement": supplement,
            "title": f"Editar: {supplement.name}",
        }
        return render(request, self.template_name, context)


class ProductDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        supplement = get_object_or_404(Supplement, slug=slug)
        supplement.is_active = False  # Soft delete
        supplement.save()
        return redirect("product_index")
