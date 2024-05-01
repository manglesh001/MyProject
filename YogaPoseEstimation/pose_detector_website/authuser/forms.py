from django import forms
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=65)
    password = forms.CharField(max_length=65)

class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=65)
    password = forms.CharField(max_length=25, min_length=3, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'password')