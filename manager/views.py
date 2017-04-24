from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


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


class MainPageView(View):
    def get(self, request):
        ctx = {'success': "Super!"}
        return render(request, 'manager/index.html', ctx)

    def post(self, request):
        ctx = {'success': "Super!"}
        return render(request, 'manager/index.html', ctx)
