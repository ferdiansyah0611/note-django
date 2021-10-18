from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('signin', views.signin, name = 'signin'),
    path('addregister', views.createuser, name = 'addregister'),
    path('signout', views.signout, name = 'signout'),
    path('todo/add', views.addtodo, name = 'addtodo'),
    path('todo/create', views.create, name = 'create'),
    path('todo/<int:todo>/delete', views.delete, name = 'deletetodo'),
    path('todo/<int:todo>/edit', views.edit, name = 'edittodo'),
]