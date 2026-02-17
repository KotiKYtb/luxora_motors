from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from .models import Vehicule, ImageVehicule, OptionVehicule


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
