from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

class RegisterUserView(View):
    pass


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
