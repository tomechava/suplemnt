from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='media/profile_images/', blank=True, null=True)  # Opcional

    def __str__(self):
        return f"{self.user.username}'s profile"

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Category name"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))

    def __str__(self):
        return self.name


class Supplement(models.Model):
    name           = models.CharField(max_length=255, verbose_name=_("Name"))
    slug           = models.SlugField(unique=True, verbose_name=_("Slug"))
    brand          = models.CharField(max_length=255, verbose_name=_("Brand"))
    description    = models.TextField(verbose_name=_("Description"))
    category       = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='supplements', verbose_name=_("Category"))
    price          = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Discount price"))
    stock          = models.PositiveIntegerField(verbose_name=_("Stock"))
    image          = models.ImageField(upload_to='supplements/', verbose_name=_("Image"))
    weight         = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Weight"))
    flavor         = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Flavor"))
    servings       = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Servings"))
    ingredients    = models.TextField(null=True, blank=True, verbose_name=_("Ingredients"))
    is_active      = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at     = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at     = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Supplement")
        verbose_name_plural = _("Supplements")

    def __str__(self):
        return f"{self.name} - {self.brand}"

    @property
    def average_rating(self):
        agg = self.reviews.aggregate(avg=Avg('rating'))
        return agg['avg'] or 0

    @property
    def reviews_count(self):
        return self.reviews.count()


class Review(models.Model):
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Supplement"))
    user       = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    rating     = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_("Rating"))
    comment    = models.TextField(verbose_name=_("Comment"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return f"{self.user.username} - {self.supplement.name} ({self.rating})"


class Order(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    address     = models.CharField(max_length=255, verbose_name=_("Address"))
    city        = models.CharField(max_length=100, verbose_name=_("City"))
    postal_code = models.CharField(max_length=20, verbose_name=_("Postal code"))
    paid        = models.BooleanField(default=False, verbose_name=_("Paid"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"#{self.id} – {self.user.username}"


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_("Order"))
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE, verbose_name=_("Supplement"))
    price      = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Unit price"))
    quantity   = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    def __str__(self):
        return f"{self.quantity} × {self.supplement.name}"
