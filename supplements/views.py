from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
class HomePageView(View):
    template_name = "home.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
class AboutView(View):
    template_name = "about.html"
    
    def get(self, request):
        return render(request, self.template_name)

#USERS VIEWS:
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
            user = authenticate(request, username=username, password=password)  # Autenticar usuario

            if user is not None:
                login(request, user)  # Iniciar sesión
                return redirect("home")  # Redirigir a la página principal

            else:
                form.add_error(None, "Invalid username or password")  # Mostrar error en el formulario

        return render(request, self.template_name, {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")  # Redirige a la página de login después de cerrar sesión

@login_required
class ProfileView(View):
    template_name = "users/profile.html"
    
    def get(self, request):
            return render(request, self.template_name, {"user": request.user})


#SUPPLEMENTS VIEWS:
class ProductIndexView(View):
    template_name = "products/product_index.html"
    
    def get(self, request):
        return render(request, self.template_name)

class ProductView(View):
    template_name = "products/product.html"
    
    def get(self, request):
        return render(request, self.template_name)

class ProductEditView(View):
    template_name = "products/products.html"
    
    def get(self, request):
        return render(request, self.template_name)

