from django import forms
from django.contrib.auth.models import User
from .models import Supplement, Category, Review

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Name", max_length=30, required=True,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Your Name"})
    )
    last_name = forms.CharField(
        label="Last Name", max_length=30, required=False,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Your Last Name"})
    )
    username = forms.CharField(
        label="Username", max_length=150, required=True,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Your Username"})
    )
    email = forms.EmailField(
        label="Email", required=True,
        widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"email@example.com"})
    )
    phone = forms.CharField(
        label="Phone Number", max_length=15, required=True,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Your Phone Number"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Repeat your Password"})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("The passwords do not match.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Your Username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Your Password"})
    )

class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = [
            'name','brand','description','category','price',
            'discount_price','stock','image','weight',
            'flavor','servings','ingredients','is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del producto'}),
            'brand': forms.TextInput(attrs={'class':'form-control','placeholder':'Marca'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':4,'placeholder':'Descripción del producto'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control','placeholder':'Precio'}),
            'discount_price': forms.NumberInput(attrs={'class':'form-control','placeholder':'Precio con descuento (opcional)'}),
            'stock': forms.NumberInput(attrs={'class':'form-control','placeholder':'Cantidad en stock'}),
            'weight': forms.NumberInput(attrs={'class':'form-control','placeholder':'Peso'}),
            'flavor': forms.TextInput(attrs={'class':'form-control','placeholder':'Sabor (opcional)'}),
            'servings': forms.NumberInput(attrs={'class':'form-control','placeholder':'Porciones (opcional)'}),
            'ingredients': forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Ingredientes (opcional)'}),
            'is_active': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']
        widgets = {
            'rating': forms.Select(attrs={'class':'form-select'}),
            'comment': forms.Textarea(attrs={'class':'form-control','rows':3}),
        }
