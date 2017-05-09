from django import forms
from django.forms import ModelForm
from .models import Meal, Quantity

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))


class RegisterForm(LoginForm):
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))


class MealForm(ModelForm):

    class Meta:
        model = Meal
        exclude = ['created_by']


class QuantityForm(ModelForm):

    class Meta:
        model = Quantity
        exclude = ['meal', 'product']