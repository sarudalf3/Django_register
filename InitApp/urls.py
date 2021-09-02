from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('SignUp/', views.register),
    path('logIn/', views.access),
    path('logOut/', views.logout),
]
