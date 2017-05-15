"""diet_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from manager.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', RegisterUserView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^index/$', MainPageView.as_view(), name='index'),
    url(r'^add_meal/$', AddMealView.as_view(), name='add_meal'),
    url(r'^add_product/$', AddProductView.as_view(), name='add_product'),
    url(r'^add_category/$', AddCategoryView.as_view(), name='add_category'),
    url(r'^list_meal/$', ListMealView.as_view(), name='list_meal'),
    url(r'^list_product/$', ListProductView.as_view(), name='list_product'),
    url(r'^list_category/$', ListCategoryView.as_view(), name='list_category'),
    url(r'^edit_product/(?P<pk>(\d)+)$', EditProductView.as_view(), name='edit_product'),
    url(r'^delete_category/(?P<pk>(\d)+)$', DeleteCategoryView.as_view(), name='delete_category'),
    url(r'^delete_product/(?P<pk>(\d)+)$', DeleteProductView.as_view(), name='delete_product'),
    url(r'^delete_meal/(?P<pk>(\d)+)$', DeleteMealView.as_view(), name='delete_meal'),
]
