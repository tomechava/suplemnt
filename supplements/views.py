from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Count, Avg
from django.utils.text import slugify

from .models import Supplement, Category, Review, OrderItem
from .forms import RegisterForm, LoginForm, SupplementForm, ReviewForm

# ——— PÁGINAS ESTÁTICAS ———

class HomePageView(View):
    template_name = "home.html"
    def get(self, request):
        return render(request, self.template_name)

class AboutView(View):
    template_name = "about.html"
    def get(self, request):
        return render(request, self.template_name)

# ——— AUTENTICACIÓN ———

class RegisterView(View):
    template_name = "users/register.html"
    def get(self, request):
        return render(request, self.template_name, {"form": RegisterForm()})
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})

class LoginView(View):
    template_name = "users/login.html"
    def get(self, request):
        return render(request, self.template_name, {"form": LoginForm()})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect("home")
            form.add_error(None, "Usuario o contraseña inválidos")
        return render(request, self.template_name, {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

class ProfileView(LoginRequiredMixin, View):
    template_name = "users/profile.html"
    def get(self, request):
        return render(request, self.template_name, {"user": request.user})

# ——— PRODUCTOS ———

class ProductIndexView(View):
    template_name = "supplements/product_index.html"
    def get(self, request):
        supplements = Supplement.objects.filter(is_active=True)
        categories  = Category.objects.all()
        slug = request.GET.get("category")
        if slug:
            supplements = supplements.filter(category__slug=slug)
        return render(request, self.template_name, {
            "supplements": supplements,
            "categories": categories,
            "selected_category": slug
        })

class ProductCreateView(LoginRequiredMixin, View):
    template_name = "supplements/product_edit.html"
    def get(self, request):
        return render(request, self.template_name, {
            "form": SupplementForm(),
            "is_edit": False,
            "title": "Crear Suplemento"
        })
    def post(self, request):
        form = SupplementForm(request.POST, request.FILES)
        if form.is_valid():
            sup = form.save(commit=False)
            sup.slug = slugify(sup.name)
            sup.save()
            return redirect("product_detail", slug=sup.slug)
        return render(request, self.template_name, {
            "form": form,
            "is_edit": False,
            "title": "Crear Suplemento"
        })

class ProductView(View):
    template_name = "supplements/product.html"
    def get(self, request, slug):
        sup     = get_object_or_404(Supplement, slug=slug, is_active=True)
        form    = ReviewForm()
        reviews = sup.reviews.select_related('user')
        related = Supplement.objects.filter(category=sup.category).exclude(id=sup.id)[:4]
        return render(request, self.template_name, {
            "supplement": sup,
            "related_products": related,
            "reviews": reviews,
            "form": form,
        })
    def post(self, request, slug):
        if not request.user.is_authenticated:
            return redirect('login')
        sup  = get_object_or_404(Supplement, slug=slug, is_active=True)
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user = request.user
            rev.supplement = sup
            rev.save()
            return redirect("product_detail", slug=slug)
        reviews = sup.reviews.select_related('user')
        related = Supplement.objects.filter(category=sup.category).exclude(id=sup.id)[:4]
        return render(request, self.template_name, {
            "supplement": sup,
            "related_products": related,
            "reviews": reviews,
            "form": form,
        })

class ProductEditView(LoginRequiredMixin, View):
    template_name = "supplements/product_edit.html"
    def get(self, request, slug):
        sup = get_object_or_404(Supplement, slug=slug)
        return render(request, self.template_name, {
            "form": SupplementForm(instance=sup),
            "is_edit": True,
            "supplement": sup,
            "title": f"Editar {sup.name}"
        })
    def post(self, request, slug):
        sup = get_object_or_404(Supplement, slug=slug)
        form = SupplementForm(request.POST, request.FILES, instance=sup)
        if form.is_valid():
            form.save()
            return redirect("product_detail", slug=sup.slug)
        return render(request, self.template_name, {
            "form": form,
            "is_edit": True,
            "supplement": sup,
            "title": f"Editar {sup.name}"
        })

class ProductDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        sup = get_object_or_404(Supplement, slug=slug)
        sup.is_active = False
        sup.save()
        return redirect("product_index")

class LatestSupplementsView(View):
    template_name = "supplements/latest_supplements.html"
    def get(self, request):
        latest = Supplement.objects.filter(is_active=True).order_by('-created_at')[:6]
        return render(request, self.template_name, {"supplements": latest})

# ——— CARRITO ———

def add_to_cart(request, id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(id)] = cart.get(str(id), 0) + 1
        request.session['cart'] = cart
        return JsonResponse({'total_items': sum(cart.values())})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

class CartView(View):
    template_name = "users/cart.html"
    def get(self, request):
        cart = request.session.get('cart', {})
        items, total = [], 0
        for id_str, qty in cart.items():
            prod = Supplement.objects.get(pk=int(id_str))
            price = prod.discount_price or prod.price
            subtotal = price * qty
            items.append({'product': prod, 'qty': qty, 'price': price, 'subtotal': subtotal})
            total += subtotal
        return render(request, self.template_name, {'items': items, 'total': total})

# ——— TOP SELLERS ———

class TopSellersView(View):
    template_name = "supplements/top_sellers.html"
    def get(self, request):
        top = (OrderItem.objects
               .values('supplement')
               .annotate(sales=Count('quantity'))
               .order_by('-sales')[:10])
        ids = [item['supplement'] for item in top]
        sups = list(Supplement.objects.filter(id__in=ids))
        sups.sort(key=lambda s: ids.index(s.id))
        return render(request, self.template_name, {'supplements': sups})
