# supplements/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Supplement(models.Model):
    name           = models.CharField(max_length=255)
    slug           = models.SlugField(unique=True)
    brand          = models.CharField(max_length=255)
    description    = models.TextField()
    category       = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='supplements')
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock          = models.PositiveIntegerField()
    image          = models.ImageField(upload_to='supplements/')
    weight         = models.DecimalField(max_digits=6, decimal_places=2)
    flavor         = models.CharField(max_length=100, null=True, blank=True)
    servings       = models.PositiveIntegerField(null=True, blank=True)
    ingredients    = models.TextField(null=True, blank=True)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.brand}"

    @property
    def average_rating(self):
        """
        Retorna el promedio de todas las reseñas (rating) o 0 si no hay ninguna.
        Se expone como propiedad para usar directamente en plantillas.
        """
        agg = self.reviews.aggregate(avg=Avg('rating'))
        return agg['avg'] or 0

    @property
    def reviews_count(self):
        """
        Retorna el número total de reseñas.
        Se expone como propiedad para llamarse directamente en plantillas.
        """
        return self.reviews.count()


class Review(models.Model):
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE, related_name='reviews')
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    rating     = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.supplement.name} ({self.rating})"


class Order(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    quantity   = models.PositiveIntegerField(default=1)
