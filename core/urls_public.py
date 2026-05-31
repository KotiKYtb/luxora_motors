from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("vehicules/", views.vehicule_list, name="vehicule_list"),
    path("vehicules/<int:pk>/", views.vehicule_detail, name="vehicule_detail"),
    path("contact/", views.contact, name="contact"),
]
