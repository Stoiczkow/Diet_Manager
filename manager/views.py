from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
# Create your views here.

class RegisterUserView(CreateView):
    model = User
    fields = ['username', 'password']
    template_name = 'manager/auth/user_form.html'