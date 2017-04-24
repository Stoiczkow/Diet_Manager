from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)