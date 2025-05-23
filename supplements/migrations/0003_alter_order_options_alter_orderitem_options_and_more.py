# Generated by Django 5.0.2 on 2025-05-13 20:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplements', '0002_alter_supplement_options_alter_supplement_weight_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Order item', 'verbose_name_plural': 'Order items'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at'], 'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
        migrations.AlterModelOptions(
            name='supplement',
            options={'ordering': ['-created_at'], 'verbose_name': 'Supplement', 'verbose_name_plural': 'Supplements'},
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default=0, max_length=255, verbose_name='Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default=0, max_length=100, verbose_name='City'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Paid'),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default=0, max_length=20, verbose_name='Postal code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Unit price'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Category name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='supplements.order', verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='supplement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplements.supplement', verbose_name='Supplement'),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='review',
            name='supplement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='supplements.supplement', verbose_name='Supplement'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='brand',
            field=models.CharField(max_length=255, verbose_name='Brand'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplements', to='supplements.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Discount price'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='flavor',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Flavor'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='image',
            field=models.ImageField(upload_to='supplements/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='ingredients',
            field=models.TextField(blank=True, null=True, verbose_name='Ingredients'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='servings',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Servings'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='stock',
            field=models.PositiveIntegerField(verbose_name='Stock'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Weight'),
        ),
    ]
