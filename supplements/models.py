from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Supplement(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # For SEO-friendly URLs
    brand = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='supplements')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()  # Only positive values
    image = models.ImageField(upload_to='supplements/')
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in kg or g")
    flavor = models.CharField(max_length=100, null=True, blank=True)
    servings = models.PositiveIntegerField(null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # To manage visibility on the store
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Show newest products first
        verbose_name = 'Supplement'
        verbose_name_plural = 'Supplements'

    def __str__(self):
        return f"{self.name} - {self.brand}"

