from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Meal, Product, Category, MEAL_NAME, Target
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.db.models import Q
from datetime import datetime, timedelta

# Create your views here.
def category_choices(request):
    result = Category.objects.filter(Q(created_by=request.user) | Q(created_by=None)).values_list('id', 'name')
    return result

def product_choices(request):
    result = Product.objects.filter(Q(created_by=request.user) | Q(created_by=None)).values_list('id', 'name')
    return result


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
        form = TargetForm()
        current_target = Target.objects.get(created_by=request.user, is_active=True)
        current_date = datetime.now().date()
        week_back = current_date - timedelta(days=7)
        meals = Meal.objects.filter(meal_date__gt=week_back, meal_date__lt=current_date)
        today_meals = Meal.objects.filter(meal_date=current_date)
        all_targets = Target.objects.filter(created_by=request.user).values('calories',
                                                                            'carbohydrates',
                                                                            'protein',
                                                                            'sugars',
                                                                            'salt',
                                                                            'fat').distinct()
        today_eaten = {'calories':0,
                       'carbohydrates':0,
                       'protein':0,
                       'sugars':0,
                       'salt':0,
                       'fat':0}
        for meal in today_meals:
            today_eaten['calories'] += meal.calories
            today_eaten['carbohydrates'] += meal.carbohydrates
            today_eaten['protein'] += meal.protein
            today_eaten['sugars'] += meal.sugars
            today_eaten['salt'] += meal.salt
            today_eaten['fat'] += meal.fat

        ctx = {
               'meals':meals,
               'current_date':current_date,
               'week_back':week_back,
               'form':form,
               'current_target':current_target,
               'today_meals':today_meals,
               'today_eaten':today_eaten,
               'all_targets':all_targets
               }
        return render(request, 'manager/index.html', ctx)

    def post(self, request):
        current_target = Target.objects.get(created_by=request.user, is_active=True)
        current_target.is_active = False
        current_target.save()
        new_target = Target.objects.create(calories=request.POST.get('calories'),
                                           carbohydrates=request.POST.get('carbohydrates'),
                                           protein=request.POST.get('protein'),
                                           sugars=request.POST.get('sugars'),
                                           salt=request.POST.get('salt'),
                                           fat=request.POST.get('fat'),
                                           is_active=True,
                                           created_by=request.user,
                                           target_date=datetime.now().date())
        new_target.save()
        return HttpResponseRedirect('/index/')


class AddMealView(LoginRequiredMixin, View):
    def get(self, request):
        form = MealForm()
        form.fields['meal_date'].widget = forms.DateInput(attrs={'class':'form-control', 'type':'date', 'placeholder':'Meal date'})
        form.fields['name'].widget = forms.Select(attrs={'class': 'form-control'}, choices=MEAL_NAME)
        form.fields['product'].widget = forms.SelectMultiple(attrs={'class': 'form-control'}, choices=product_choices(self.request))

        ctx = {
            'form':form,
        }
        return render(request, 'manager/meal_form.html', ctx)

    def post(self, request):
        products = Product.objects.all()
        meal_name = request.POST.get('name')
        meal_date = request.POST.get('meal_date')
        meal_user = request.user
        meal_products = {}
        calories = 0.0
        carbohydrates = 0.0
        protein = 0.0
        sugars = 0.0
        salt = 0.0
        fat = 0.0
        new_meal = Meal.objects.create(name=meal_name, meal_date=meal_date, created_by=meal_user)
        for product in products:
            quan = int(request.POST.get(str(product.name)))
            if quan != 0:
                Quantity.objects.create(quantity=quan, meal = new_meal, product = product)
                calories += (product.calories * quan) / 100
                carbohydrates += (product.carbohydrates * quan) / 100
                protein += (product.protein * quan) / 100
                sugars += (product.sugars * quan) / 100
                salt += (product.salt * quan) / 100
                fat += (product.fat * quan) / 100
                meal_products[str(product.name)] = request.POST.get(str(product.name))
        new_meal.calories = calories
        new_meal.carbohydrates = carbohydrates
        new_meal.protein = protein
        new_meal.sugars = sugars
        new_meal.salt = salt
        new_meal.fat = fat
        new_meal.save()
        return HttpResponseRedirect("/list_meal/")


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'calories', 'carbohydrates', 'protein', 'sugars', 'salt', 'fat', 'category']

    def get_form(self):
        form = super(AddProductView, self).get_form()

        form.fields['name'].widget = forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Products name',
            'title':"Products name",
            'data - toggle':"popover",
            'data - trigger':"hover"
        })
        form.fields['description'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Description of a product',
            'title':"Products description",
            'data - toggle':"popover",
            'data - trigger':"hover"
        })
        form.fields['calories'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calories in 100g/100ml',
            'title':"Calories in 100g/100ml",
            'data - toggle':"popover",
            'data - trigger':"hover",
            'step':'0.1'
        })
        form.fields['carbohydrates'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Carbohydrates in 100g/100ml',
            'title':"Carbohydrates in 100g/100ml",
            'data - toggle':"popover",
            'data - trigger':"hover",
            'step': '0.1'
        })
        form.fields['protein'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder':'Protein in 100g/100ml',
            'title':"Protein in 100g/100ml",
            'data - toggle':"popover",
            'data - trigger':"hover",
            'step': '0.1'
        })
        form.fields['sugars'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sugars in 100g/100ml',
            'title':"Sugars in 100g/100ml",
            'data - toggle':"popover",
            'data - trigger':"hover",
            'step': '0.1'
        })
        form.fields['salt'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Salt in 100g/100ml',
            'title':"Salt in 100g/100ml",
            'data - toggle':"popover",
            'data - trigger':"hover",
            'step': '0.1'
        })
        form.fields['fat'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Fat in 100g/100ml',
            'title':"Fat in 100g/100ml",
            'data - toggle':"popover",
            'data - trigger':"hover",
            'step': '0.1'
        })
        form.fields['category'].widget = forms.SelectMultiple(attrs={'class': 'form-control'}, choices=category_choices(self.request))
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(AddProductView, self).form_valid(form)


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']

    def get_form(self):
        form = super(AddCategoryView, self).get_form()
        form.fields['name'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Category name'})
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(AddCategoryView, self).form_valid(form)


class ListCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.filter(Q(created_by=request.user) | Q(created_by=None))
        products = {}
        for category in categories:
            products[str(category.name)] = Product.objects.filter(category=category)
        ctx = {
            'categories':categories,
            'products':products
               }
        return render(request, 'manager/category_list.html', ctx)

    def post(self, request):
        categories = Category.objects.filter(Q(created_by=request.user) | Q(created_by=None))
        products = {}
        for category in categories:
            products[str(category.name)] = Product.objects.filter(category=category)
        ctx = {
            'categories': categories,
            'products': products
        }
        return render(request, 'manager/category_list.html', ctx)


class ListProductView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.filter(Q(created_by=request.user) | Q(created_by=None))
        ctx = {
            'products':products
        }
        return render(request, 'manager/product_list.html', ctx)


class ListMealView(LoginRequiredMixin, View):
    def get(self, request):
        meals = Meal.objects.filter(created_by=request.user).order_by('-meal_date')
        quantity = Quantity.objects.all()
        products = []
        for meal in meals:
            for quan in quantity:
                if quan.meal == meal:
                    products.append([meal.pk, quan.product, quan.quantity])

        ctx = {
            'meals':meals,
            'products':products,
               }
        return render(request, 'manager/meal_list.html', ctx)


class EditProductView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'
    template_name_suffix = '_update_form'

    def get_form(self):
        form = super(EditProductView, self).get_form()
        form.fields['name'].widget = forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Products name',
            'title':"Products name",
        })
        form.fields['description'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Description of a product',
            'title':"Products description",
        })
        form.fields['calories'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calories in 100g/100ml',
            'title':"Calories in 100g/100ml",
            'step':'0.1'
        })
        form.fields['carbohydrates'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Carbohydrates in 100g/100ml',
            'title':"Carbohydrates in 100g/100ml",
            'step': '0.1'
        })
        form.fields['protein'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder':'Protein in 100g/100ml',
            'title':"Protein in 100g/100ml",
            'step': '0.1'
        })
        form.fields['sugars'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sugars in 100g/100ml',
            'title':"Sugars in 100g/100ml",
            'step': '0.1'
        })
        form.fields['salt'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Salt in 100g/100ml',
            'title':"Salt in 100g/100ml",
            'step': '0.1'
        })
        form.fields['fat'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Fat in 100g/100ml',
            'title':"Fat in 100g/100ml",
            'step': '0.1'
        })
        form.fields['category'].widget = forms.SelectMultiple(attrs={'class': 'form-control'}, choices=category_choices(self.request))
        return form


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = '/list_category'


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/list_product'


class DeleteMealView(LoginRequiredMixin, DeleteView):
    model = Meal
    success_url = '/list_meal'