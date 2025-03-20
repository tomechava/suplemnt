import os
import django
import sys
from django.utils.text import slugify

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Set up Django environment (Modify 'your_project.settings' with your actual project settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suplemnt.settings')
django.setup()

from supplements.models import Category, Supplement

# 1️⃣ Define Categories
categories_data = [
    "Protein Powder", "Pre-Workout", "Post-Workout", "Vitamins", "Fat Burners"
]

categories = {}

for category_name in categories_data:
    category, created = Category.objects.get_or_create(
        name=category_name,
        slug=slugify(category_name)
    )
    categories[category_name] = category  # Store category reference

# 2️⃣ Define Supplements
supplements_data = [
    {
        "name": "Whey Protein Isolate",
        "brand": "Optimum Nutrition",
        "description": "High-quality whey protein isolate for muscle recovery.",
        "category": categories["Protein Powder"],
        "price": 39.99,
        "discount_price": 34.99,
        "stock": 50,
        "image": "supplements/whey_protein.jpg",
        "weight": 2.0,
        "flavor": "Vanilla",
        "servings": 60,
        "ingredients": "Whey protein isolate, natural flavors, lecithin, enzymes.",
    },
    {
        "name": "Creatine Monohydrate",
        "brand": "MuscleTech",
        "description": "Pure creatine monohydrate for strength and endurance.",
        "category": categories["Post-Workout"],
        "price": 19.99,
        "discount_price": None,
        "stock": 100,
        "image": "supplements/creatine.jpg",
        "weight": 0.3,
        "flavor": None,
        "servings": 80,
        "ingredients": "Micronized creatine monohydrate.",
    },
    {
        "name": "BCAA 2:1:1",
        "brand": "Xtend",
        "description": "Branched-chain amino acids for muscle recovery and hydration.",
        "category": categories["Post-Workout"],
        "price": 24.99,
        "discount_price": 21.99,
        "stock": 75,
        "image": "supplements/bcaa.jpg",
        "weight": 0.5,
        "flavor": "Watermelon",
        "servings": 50,
        "ingredients": "L-Leucine, L-Isoleucine, L-Valine, Electrolytes.",
    },
    {
        "name": "Multivitamin for Men",
        "brand": "Centrum",
        "description": "Daily essential vitamins and minerals for men's health.",
        "category": categories["Vitamins"],
        "price": 14.99,
        "discount_price": None,
        "stock": 120,
        "image": "supplements/multivitamin.jpg",
        "weight": 0.2,
        "flavor": None,
        "servings": 90,
        "ingredients": "Vitamin A, C, D, E, B-complex, Zinc, Magnesium.",
    },
    {
        "name": "Thermogenic Fat Burner",
        "brand": "Hydroxycut",
        "description": "Weight management supplement with metabolism boosters.",
        "category": categories["Fat Burners"],
        "price": 29.99,
        "discount_price": 25.99,
        "stock": 60,
        "image": "supplements/fat_burner.jpg",
        "weight": 0.1,
        "flavor": None,
        "servings": 30,
        "ingredients": "Caffeine, Green Tea Extract, L-Carnitine.",
    },
    {
        "name": "Vegan Protein Blend",
        "brand": "Garden of Life",
        "description": "Plant-based protein powder with organic ingredients.",
        "category": categories["Protein Powder"],
        "price": 34.99,
        "discount_price": None,
        "stock": 40,
        "image": "supplements/vegan_protein.jpg",
        "weight": 1.8,
        "flavor": "Chocolate",
        "servings": 30,
        "ingredients": "Pea protein, Brown rice protein, Chia seeds.",
    },
    {
        "name": "L-Carnitine Liquid",
        "brand": "NOW Sports",
        "description": "Supports energy production and fat metabolism.",
        "category": categories["Fat Burners"],
        "price": 16.99,
        "discount_price": None,
        "stock": 50,
        "image": "supplements/l_carnitine.jpg",
        "weight": 0.5,
        "flavor": "Berry Blast",
        "servings": 32,
        "ingredients": "L-Carnitine, Citric Acid, Natural Flavors.",
    },
    {
        "name": "Pre-Workout Explosion",
        "brand": "C4",
        "description": "High-intensity pre-workout formula for enhanced performance.",
        "category": categories["Pre-Workout"],
        "price": 29.99,
        "discount_price": 24.99,
        "stock": 90,
        "image": "supplements/preworkout.jpg",
        "weight": 0.6,
        "flavor": "Fruit Punch",
        "servings": 45,
        "ingredients": "Caffeine, Beta-Alanine, Creatine Nitrate.",
    },
    {
        "name": "Zinc + Magnesium",
        "brand": "NOW Foods",
        "description": "Essential minerals to support muscle recovery and sleep.",
        "category": categories["Vitamins"],
        "price": 12.99,
        "discount_price": None,
        "stock": 80,
        "image": "supplements/zma.jpg",
        "weight": 0.2,
        "flavor": None,
        "servings": 60,
        "ingredients": "Zinc, Magnesium, Vitamin B6.",
    },
    {
        "name": "Casein Protein",
        "brand": "Dymatize",
        "description": "Slow-digesting protein for overnight recovery.",
        "category": categories["Protein Powder"],
        "price": 44.99,
        "discount_price": None,
        "stock": 35,
        "image": "supplements/casein.jpg",
        "weight": 1.5,
        "flavor": "Cookies & Cream",
        "servings": 55,
        "ingredients": "Micellar Casein, Cocoa, Natural Flavors.",
    },
]

# 3️⃣ Insert Supplements into Database
for supplement in supplements_data:
    Supplement.objects.get_or_create(
        name=supplement["name"],
        slug=slugify(supplement["name"]),
        brand=supplement["brand"],
        description=supplement["description"],
        category=supplement["category"],
        price=supplement["price"],
        discount_price=supplement["discount_price"],
        stock=supplement["stock"],
        image=supplement["image"],
        weight=supplement["weight"],
        flavor=supplement["flavor"],
        servings=supplement["servings"],
        ingredients=supplement["ingredients"],
    )

print("✅ Database successfully populated with supplements!")
