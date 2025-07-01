from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("about",views.about, name="about"),
    path("help",views.help, name="help"),
    path("contact",views.contact, name="contact"),
    path("login",views.login, name="login"),
]