from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.utils.text import slugify
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import render

import random

from .models import Supplement, Category, Review, Order, OrderItem
from .forms import (
    RegisterForm,
    LoginForm,
    SupplementForm,
    ReviewForm,
    OrderCreateForm,
    ProfileEditForm,
)
from .reports import createInvoice
from .gemini_utils import ask_gemini, generate_prompt

# ——— PÁGINAS ESTÁTICAS ———


class HomePageView(View):
    template_name = "home.html"

    def get(self, request):
        random_supplements = Supplement.objects.filter(is_active=True).order_by("?")[:6]
        return render(
            request,
            self.template_name,
            {
                "supplements": random_supplements,
            },
        )


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
                password=form.cleaned_data["password"],
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
        # Obtener la información del usuario
        profile = request.user.profile

        # Orders del usuario
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        return render(
            request,
            self.template_name,
            {"user": request.user, "profile": profile, "orders": orders},
        )


class ProfileEditView(LoginRequiredMixin, View):
    template_name = "users/profile_edit.html"

    def get(self, request):
        form = ProfileEditForm(instance=request.user)
        return render(request, "users/profile_edit.html", {"form": form})

    def post(self, request):
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profile updated successfully."))
            return redirect("profile")
        else:
            messages.error(request, _("Error updating profile."))
        return render(request, "users/profile_edit.html", {"form": form})


# ——— PRODUCTOS ———


class ProductIndexView(View):
    template_name = "supplements/product_index.html"

    def get(self, request):
        supplements = Supplement.objects.filter(is_active=True)
        categories = Category.objects.all()
        slug = request.GET.get("category")
        if slug:
            supplements = supplements.filter(category__slug=slug)
        return render(
            request,
            self.template_name,
            {
                "supplements": supplements,
                "categories": categories,
                "selected_category": slug,
            },
        )


class ProductCreateView(LoginRequiredMixin, View):
    template_name = "supplements/product_edit.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {"form": SupplementForm(), "is_edit": False, "title": "Crear Suplemento"},
        )

    def post(self, request):
        form = SupplementForm(request.POST, request.FILES)
        if form.is_valid():
            sup = form.save(commit=False)
            sup.slug = slugify(sup.name)
            sup.save()
            return redirect("product_detail", slug=sup.slug)
        return render(
            request,
            self.template_name,
            {"form": form, "is_edit": False, "title": "Crear Suplemento"},
        )


class ProductView(View):
    template_name = "supplements/product.html"

    def get(self, request, slug):
        sup = get_object_or_404(Supplement, slug=slug, is_active=True)
        form = ReviewForm()
        reviews = sup.reviews.select_related("user")
        related = Supplement.objects.filter(category=sup.category).exclude(id=sup.id)[
            :4
        ]
        return render(
            request,
            self.template_name,
            {
                "supplement": sup,
                "related_products": related,
                "reviews": reviews,
                "form": form,
            },
        )

    def post(self, request, slug):
        if not request.user.is_authenticated:
            return redirect("login")
        sup = get_object_or_404(Supplement, slug=slug, is_active=True)
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user = request.user
            rev.supplement = sup
            rev.save()
            return redirect("product_detail", slug=slug)
        reviews = sup.reviews.select_related("user")
        related = Supplement.objects.filter(category=sup.category).exclude(id=sup.id)[
            :4
        ]
        return render(
            request,
            self.template_name,
            {
                "supplement": sup,
                "related_products": related,
                "reviews": reviews,
                "form": form,
            },
        )


class ProductEditView(LoginRequiredMixin, View):
    template_name = "supplements/product_edit.html"

    def get(self, request, slug):
        sup = get_object_or_404(Supplement, slug=slug)
        return render(
            request,
            self.template_name,
            {
                "form": SupplementForm(instance=sup),
                "is_edit": True,
                "supplement": sup,
                "title": f"Editar {sup.name}",
            },
        )

    def post(self, request, slug):
        sup = get_object_or_404(Supplement, slug=slug)
        form = SupplementForm(request.POST, request.FILES, instance=sup)
        if form.is_valid():
            form.save()
            return redirect("product_detail", slug=sup.slug)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "is_edit": True,
                "supplement": sup,
                "title": f"Editar {sup.name}",
            },
        )


class ProductDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        sup = get_object_or_404(Supplement, slug=slug)
        sup.is_active = False
        sup.save()
        return redirect("product_index")


class LatestSupplementsView(View):
    template_name = "supplements/latest_supplements.html"

    def get(self, request):
        latest = Supplement.objects.filter(is_active=True).order_by("-created_at")[:6]
        return render(request, self.template_name, {"supplements": latest})


# ——— CARRITO ———


def add_to_cart(request, id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        cart[str(id)] = cart.get(str(id), 0) + 1
        request.session["cart"] = cart
        return JsonResponse({"total_items": sum(cart.values())})
    return JsonResponse({"error": "Método no permitido"}, status=405)


def remove_from_cart(request, id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        if str(id) in cart:
            del cart[str(id)]
            request.session["cart"] = cart
        return JsonResponse({"total_items": sum(cart.values())})
    return JsonResponse({"error": "Método no permitido"}, status=405)


def clear_cart(request):
    request.session["cart"] = {}
    request.session.modified = True


class CartView(View):
    template_name = "users/cart.html"

    def get(self, request):
        cart = request.session.get("cart", {})
        items, total = [], 0
        for id_str, qty in cart.items():
            prod = get_object_or_404(Supplement, pk=int(id_str))
            price = prod.discount_price or prod.price
            subtotal = price * qty
            items.append(
                {"product": prod, "qty": qty, "price": price, "subtotal": subtotal}
            )
            total += subtotal
        return render(request, self.template_name, {"items": items, "total": total})


# ——— PEDIDOS ———


@method_decorator(login_required, name="dispatch")
class OrderCreateView(View):
    template_name = "supplements/order_create.html"

    def get(self, request):
        cart = request.session.get("cart", {})
        if not cart:
            return redirect("cart_view")

        # Construir items y total
        items, total = [], 0
        for id_str, qty in cart.items():
            prod = get_object_or_404(Supplement, pk=int(id_str))
            price = prod.discount_price or prod.price
            subtotal = price * qty
            items.append({"product": prod, "qty": qty, "subtotal": subtotal})
            total += subtotal

        form = OrderCreateForm()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "items": items,
                "total": total,
            },
        )

    def post(self, request):
        cart = request.session.get("cart", {})
        if not cart:
            return redirect("cart_view")

        # Recalcular items y total en caso de error
        items, total = [], 0
        for id_str, qty in cart.items():
            prod = get_object_or_404(Supplement, pk=int(id_str))
            price = prod.discount_price or prod.price
            subtotal = price * qty
            items.append({"product": prod, "qty": qty, "subtotal": subtotal})
            total += subtotal

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_cost = total
            order.save()
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    supplement=item["product"],
                    price=item["product"].discount_price or item["product"].price,
                    quantity=item["qty"],
                )
            request.session["cart"] = {}
            # Crear factura
            createInvoice(
                f"invoice_{order.id}.pdf",
                "Invoice",
                "SUPLEMNT",
                "Order Invoice",
                "Order Details",
                order.user,
                order,
                order.items.all(),
            )
            order.invoice_file = f"invoices/invoice_{order.id}.pdf"
            order.save()
            # Vaciar el carrito
            clear_cart(request)
            # Redirigir a la vista de éxito
            return redirect("order_success", order_id=order.id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "items": items,
                "total": total,
            },
        )


@method_decorator(login_required, name="dispatch")
class OrderSuccessView(View):
    template_name = "supplements/order_success.html"

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, self.template_name, {"order": order})


class OrderDetailView(LoginRequiredMixin, View):
    template_name = "supplements/order_detail.html"

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        items = OrderItem.objects.filter(order=order)
        return render(request, self.template_name, {"order": order, "items": items})


# ——— TOP SELLERS ———


class TopSellersView(View):
    template_name = "supplements/top_sellers.html"

    def get(self, request):
        top = (
            OrderItem.objects.values("supplement")
            .annotate(sales=Count("quantity"))
            .order_by("-sales")[:10]
        )
        ids = [item["supplement"] for item in top]
        sups = list(Supplement.objects.filter(id__in=ids))
        sups.sort(key=lambda s: ids.index(s.id))
        return render(request, self.template_name, {"supplements": sups})


class AskGeminiView(LoginRequiredMixin, View):
    template_name = "supplements/gemini_chat.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        question = request.POST.get("question")
        clear = request.POST.get("clear", "false") == "true"

        if clear:
            request.session["chat_history"] = []
            return JsonResponse({"answer": "Chat history has been cleared."})

        if not question:
            return JsonResponse({"error": "No question provided"}, status=400)

        # Genera base del prompt
        base_prompt = generate_prompt(request.user)

        # Recupera historial y añade pregunta actual
        chat_history = request.session.get("chat_history", [])
        chat_history.append(f"User: {question}")

        # Construye el prompt completo
        full_prompt = base_prompt + "\n".join(chat_history)

        # Obtiene respuesta de Gemini
        answer = ask_gemini(full_prompt)
        chat_history.append(f"Gemini: {answer}")

        # Guarda el nuevo historial en la sesión
        request.session["chat_history"] = chat_history

        return JsonResponse({"answer": answer})
