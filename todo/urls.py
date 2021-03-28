"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from woo import views as woo_views



urlpatterns = [
    path('admin/', admin.site.urls),
    #AUTH_PASSWORD_VALIDATORS
    path('signup/',woo_views.signup,name='signup'),
    path('',woo_views.current,name='current'),
    path('logout/',woo_views.logoutuser,name='logout'),
    path('login/',woo_views.loginuser,name='login'),
    path('create/',woo_views.create,name='create'),
    path('current/<int:pk>',woo_views.viewTodo,name='viewTodo'),
    path('current/<int:pk>/complete/',woo_views.complete,name='complete'),
    path('current/<int:pk>/delete/',woo_views.delete,name='delete'),
    path('completed/',woo_views.completed,name='completed'),

    #Api
    path('api/',include('api.urls')),
]
