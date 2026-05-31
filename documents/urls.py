from django.urls import path

from . import views

urlpatterns = [
    path("", views.cms_document_vehicule_list, name="cms_document_vehicule_list"),
    path(
        "vehicule/<int:vehicule_pk>/",
        views.cms_document_list,
        name="cms_document_list",
    ),
    path(
        "vehicule/<int:vehicule_pk>/ajouter/",
        views.cms_document_create,
        name="cms_document_create",
    ),
    path("<int:pk>/supprimer/", views.cms_document_delete, name="cms_document_delete"),
]
