from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("vehicules/", views.vehicule_list, name="vehicule_list"),
    path("vehicules/<int:pk>/", views.vehicule_detail, name="vehicule_detail"),
    path("contact/", views.contact, name="contact"),
    # cms (gestion véhicules, staff uniquement)
    path("cms/", views.cms_vehicule_list, name="cms_vehicule_list"),
    path("cms/vehicules/ajouter/", views.cms_vehicule_create, name="cms_vehicule_create"),
    path("cms/vehicules/<int:pk>/modifier/", views.cms_vehicule_edit, name="cms_vehicule_edit"),
    path("cms/vehicules/<int:pk>/supprimer/", views.cms_vehicule_delete, name="cms_vehicule_delete"),
]
