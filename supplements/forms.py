from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="Name", max_length=30, required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
    )
    last_name = forms.CharField(label="Last Name", max_length=30, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Last Name"}),
    )
    username = forms.CharField( label="Username", max_length=150, required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Username"}),
    )
    email = forms.EmailField( label="Emailo", required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@example.com"}),
    )
    phone = forms.CharField( label="Phone Number", max_length=15, required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Phone Number"}),
    )
    password1 = forms.CharField( label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )
    password2 = forms.CharField( label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repeat your Password"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Encripta la contraseña
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Your Password"})
    )
