from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Meal, Product, Category, MEAL_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

# Create your views here.
category_choices = Category.objects.all().values_list('id', 'name')
product_choices = Product.objects.all().values_list('id', 'name')

class RegisterUserView(View):
    def get(self, request):
        form = RegisterForm()
        ctx = {'form': form}
        return render(request, 'manager/register.html', ctx)

    def post(self, request):
        User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
        ctx = {"success": "Użytkownik dodany!"}
        return render(request, 'manager/index.html', ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {'form':form}
        return render(request, 'manager/login.html', ctx)

    def post(self, request):
        form = LoginForm()
        ctx = {'form': form}
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            ctx = {'form': form, 'error': "Błędne dane logowania"}
            return render(request, "manager/login.html", ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class MainPageView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {'success': "Super!"}
        return render(request, 'manager/index.html', ctx)

    def post(self, request):
        ctx = {'success': "Super!"}
        return render(request, 'manager/index.html', ctx)


class AddMealView(LoginRequiredMixin, CreateView):
    model = Meal
    fields = ['name', 'meal_date', 'product']
    # initial = {'user': 3}
    def get_form(self):
        form = super(AddMealView, self).get_form()
        form.fields['meal_date'].widget = forms.DateInput(attrs={'class':'form-control', 'type':'date', 'placeholder':'Meal date'})
        form.fields['name'].widget = forms.Select(attrs={'class': 'form-control'}, choices=MEAL_NAME)
        form.fields['product'].widget = forms.SelectMultiple(attrs={'class': 'form-control'}, choices=product_choices)
        return form

    # auto-set logged user to the form
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(AddMealView, self).form_valid(form)


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    fields = '__all__'

    def get_form(self):
        form = super(AddProductView, self).get_form()
        form.fields['name'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Product'})
        form.fields['description'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description of a product'})
        form.fields['calories'].widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Calories in 100g/100ml'})
        form.fields['category'].widget = forms.SelectMultiple(attrs={'class': 'form-control'}, choices=category_choices)
        return form


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'

    def get_form(self):
        form = super(AddCategoryView, self).get_form()
        form.fields['name'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Category name'})
        return form


class ListCategoryView(LoginRequiredMixin, ListView):
    model = Category


class ListProductView(LoginRequiredMixin, ListView):
    model = Product


class ListMealView(LoginRequiredMixin, ListView):
    model = Meal