from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from .models import Vehicule, ImageVehicule, OptionVehicule, RendezVous, RendezVousFichier


class OptionVehiculeInline(TabularInline):
    model = OptionVehicule
    extra = 1


class ImageVehiculeInline(TabularInline):
    model = ImageVehicule
    extra = 1


@admin.register(Vehicule)
class VehiculeAdmin(ModelAdmin):
    list_display = ("titre", "marque", "annee", "kilometrage", "prix", "en_vedette", "ordre_affichage")
    list_filter = ("marque", "en_vedette")
    search_fields = ("titre", "modele", "marque")
    inlines = [OptionVehiculeInline, ImageVehiculeInline]


@admin.register(OptionVehicule)
class OptionVehiculeAdmin(ModelAdmin):
    list_display = ("vehicule", "libelle", "ordre")


@admin.register(ImageVehicule)
class ImageVehiculeAdmin(ModelAdmin):
    list_display = ("vehicule", "ordre", "legende")


class RendezVousFichierInline(TabularInline):
    model = RendezVousFichier
    extra = 0
    readonly_fields = ("fichier",)


@admin.register(RendezVous)
class RendezVousAdmin(ModelAdmin):
    list_display = ("prenom", "nom", "email", "telephone", "raison", "created_at")
    list_filter = ("raison", "created_at")
    search_fields = ("nom", "prenom", "email")
    readonly_fields = ("created_at",)
    inlines = [RendezVousFichierInline]
