from django import forms
from django.forms import ModelForm
from .models import Meal, Quantity, Target

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


class TargetForm(ModelForm):

    class Meta:
        model = Target
        exclude = ['created_by', 'is_active']
        widgets = {
            'calories':forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calories in kcal',
                'title':"Calories in kcal",
                'data - toggle':"popover",
                'data - trigger':"hover",
                'step':'0.1'}),
            'protein':forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Protein in g',
                'title':"Protein in g",
                'data - toggle':"popover",
                'data - trigger':"hover",
                'step':'0.1'}),
            'carbohydrates': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Carbohydrates in g',
                'title': "Carbohydrates in g",
                'data - toggle': "popover",
                'data - trigger': "hover",
                'step': '0.1'}),
            'sugars': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sugars in g',
                'title': "Sugars in g",
                'data - toggle': "popover",
                'data - trigger': "hover",
                'step': '0.1'}),
            'salt': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Salt in g',
                'title': "Salt in g",
                'data - toggle': "popover",
                'data - trigger': "hover",
                'step': '0.1'}),
            'fat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fat in g',
                'title': "Fat in g",
                'data - toggle': "popover",
                'data - trigger': "hover",
                'step': '0.1'})
        }