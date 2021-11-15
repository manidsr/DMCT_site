from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        strip=False,
        widget=forms.TextInput(attrs={'autofocus': True,'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder': 'Confirmation Password'}),
        strip=False,
    )
    def Getuser(self):
        return self.username
    def Getpassword(self):
        return self.password2