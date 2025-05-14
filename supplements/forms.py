from django import forms
from django.contrib.auth.models import User
from .models import Supplement, Review, Order, Profile
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import pytz
#timezone config
timezone.activate(pytz.timezone('America/Bogota'))

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("Name"), max_length=30, required=True,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":_("Your Name")})
    )
    last_name = forms.CharField(
        label=_("Last Name"), max_length=30, required=False,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":_("Your Last Name")})
    )
    username = forms.CharField(
        label=_("Username"), max_length=150, required=True,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":_("Your Username")})
    )
    email = forms.EmailField(
        label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"email@example.com"})
    )
    phone = forms.CharField(
        label=_("Phone"), max_length=15, required=True,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":_("Your Phone Number")})
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":_("Password")})
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":_("Repeat your Password")})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError(_("The passwords do not match."))
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Guardar el número de teléfono en el perfil
            profile = Profile.objects.get(user=user)
            profile.phone = self.cleaned_data["phone"]
            profile.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":_("Your Username")})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":_("Your Password")})
    )

class ProfileEditForm(forms.ModelForm):
    phone = forms.CharField(
        label=_("Phone Number"), max_length=15, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Your Phone Number")})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Set initial phone from profile
        if self.user and hasattr(self.user, 'profile'):
            self.fields['phone'].initial = self.user.profile.phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("This username is already taken."))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("This email is already registered."))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if Profile.objects.filter(phone=phone).exclude(user=self.instance).exists():
            raise forms.ValidationError(_("This phone number is already registered."))
        return phone

    def save(self, commit=True):
        user = super().save(commit=commit)
        phone = self.cleaned_data.get("phone")
        profile = user.profile
        profile.phone = phone
        if commit:
            profile.save()
        return user


class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = [
            'name','brand','description','category','price',
            'discount_price','stock','image','weight',
            'flavor','servings','ingredients','is_active'
        ]
        widgets = {
            'name':           forms.TextInput(attrs={'class':'form-control','placeholder':_('Nombre del producto')}),
            'brand':          forms.TextInput(attrs={'class':'form-control','placeholder':_('Marca')}),
            'description':    forms.Textarea(attrs={'class':'form-control','rows':4,'placeholder':_('Descripción del producto')}),
            'category':       forms.Select(attrs={'class':'form-control'}),
            'price':          forms.NumberInput(attrs={'class':'form-control','placeholder':_('Precio')}),
            'discount_price': forms.NumberInput(attrs={'class':'form-control','placeholder':_('Precio con descuento (opcional)')}),
            'stock':          forms.NumberInput(attrs={'class':'form-control','placeholder':_('Cantidad en stock')}),
            'weight':         forms.NumberInput(attrs={'class':'form-control','placeholder':_('Peso')}),
            'flavor':         forms.TextInput(attrs={'class':'form-control','placeholder':_('Sabor (opcional)')}),
            'servings':       forms.NumberInput(attrs={'class':'form-control','placeholder':_('Porciones (opcional)')}),
            'ingredients':    forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':_('Ingredientes (opcional)')}),
            'is_active':      forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']
        widgets = {
            'rating':  forms.Select(attrs={'class':'form-select'}),
            'comment': forms.Textarea(attrs={'class':'form-control','rows':3}),
        }


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        created_at = forms.DateTimeField(
            widget=forms.HiddenInput(),
            initial=timezone.now
        )
        total_cost = forms.DecimalField(
            widget=forms.HiddenInput(),
            initial=0.00
        )
        fields = ['address', 'city', 'postal_code']
        widgets = {
            'address':     forms.TextInput(attrs={'class':'form-control','placeholder':_('Dirección')}),
            'city':        forms.TextInput(attrs={'class':'form-control','placeholder':_('Ciudad')}),
            'postal_code': forms.TextInput(attrs={'class':'form-control','placeholder':_('Código postal')}),
        }
    
