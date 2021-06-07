from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.task_create),
    path('login/', views.login),
    path(r'edit/<int:id>/', views.task_edit),
]