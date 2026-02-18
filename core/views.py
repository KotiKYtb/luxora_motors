import json
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Vehicule, RendezVous, RendezVousFichier
from .forms import (
    VehiculeForm,
    OptionVehiculeFormSet,
    ImageVehiculeFormSet,
    RendezVousForm,
    CONTACT_ALLOWED_EXTENSIONS,
    CONTACT_MAX_FILE_SIZE,
    CONTACT_MAX_FILES,
)


def home(request):
    """Landing page avec véhicules en vedette."""
    vedettes = Vehicule.objects.filter(en_vedette=True).prefetch_related("options")[:6]
    return render(request, "core/home.html", {"vedettes": vedettes})


def vehicule_list(request):
    """Liste de tous les véhicules."""
    vehicules = Vehicule.objects.all().prefetch_related("options")
    return render(request, "core/vehicule_list.html", {"vehicules": vehicules})


def vehicule_detail(request, pk):
    """Détail d'un véhicule (pas de bouton achat, contact/RDV uniquement)."""
    from django.templatetags.static import static

    vehicule = get_object_or_404(
        Vehicule.objects.prefetch_related("options", "images"),
        pk=pk,
    )
    marque_image_url = static("img/marque/%s.png" % vehicule.marque)
    return render(
        request,
        "core/vehicule_detail.html",
        {"vehicule": vehicule, "marque_image_url": marque_image_url},
    )


def contact(request):
    """Page contact avec formulaire de prise de rendez-vous (nom, prénom, mail, tél, raison, message, pièces jointes)."""
    form = RendezVousForm(request.POST or None, request.FILES or None, request=request)
    if request.method == "POST" and form.is_valid():
        rdv = form.save()
        # Enregistrer les pièces jointes (validation déjà faite dans le form)
        count = 0
        for f in request.FILES.getlist("fichiers"):
            if count >= CONTACT_MAX_FILES:
                break
            ext = os.path.splitext(getattr(f, "name", "") or "")[1].lower()
            if ext in CONTACT_ALLOWED_EXTENSIONS and f.size <= CONTACT_MAX_FILE_SIZE:
                RendezVousFichier.objects.create(rendez_vous=rdv, fichier=f)
                count += 1
        messages.success(request, "Votre demande de rendez-vous a bien été envoyée. Nous vous recontacterons rapidement.")
        return redirect("contact")
    return render(request, "core/contact.html", {"form": form})


# ---------- cms (réservé aux utilisateurs staff, connexion via /admin/) ----------

def _staff_required(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(_staff_required, login_url="/admin/login/")
def cms_vehicule_list(request):
    """cms : liste des véhicules avec actions modifier / supprimer / ajouter."""
    vehicules = Vehicule.objects.all().order_by("-ordre_affichage", "-created_at")
    return render(request, "cms/vehicule_list.html", {"vehicules": vehicules})


@login_required
@user_passes_test(_staff_required, login_url="/admin/login/")
def cms_vehicule_create(request):
    """cms : ajouter un véhicule."""
    form = VehiculeForm(request.POST or None, request.FILES or None)
    formset = OptionVehiculeFormSet(request.POST or None, instance=None)
    images_formset = ImageVehiculeFormSet(request.POST or None, request.FILES or None, instance=None)
    vehicule_ctx = None
    if request.method == "POST":
        if form.is_valid():
            vehicule = form.save()
            formset = OptionVehiculeFormSet(request.POST, request.FILES, instance=vehicule)
            images_formset = ImageVehiculeFormSet(request.POST, request.FILES, instance=vehicule)
            if formset.is_valid() and images_formset.is_valid():
                formset.save()
                images_formset.save()
                messages.success(request, "Véhicule créé.")
                return redirect("cms_vehicule_list")
            form = VehiculeForm(instance=vehicule)
            vehicule_ctx = vehicule
    return render(request, "cms/vehicule_form.html", {
        "form": form,
        "formset": formset,
        "images_formset": images_formset,
        "vehicule": vehicule_ctx,
        "marques_json": json.dumps(dict(Vehicule.MARQUES)),
    })


@login_required
@user_passes_test(_staff_required, login_url="/admin/login/")
def cms_vehicule_edit(request, pk):
    """cms : modifier un véhicule (tous les champs + options + images secondaires)."""
    vehicule = get_object_or_404(Vehicule, pk=pk)
    form = VehiculeForm(request.POST or None, request.FILES or None, instance=vehicule)
    formset = OptionVehiculeFormSet(request.POST or None, instance=vehicule)
    images_formset = ImageVehiculeFormSet(
        request.POST or None, request.FILES or None, instance=vehicule
    )
    if request.method == "POST":
        if form.is_valid() and formset.is_valid() and images_formset.is_valid():
            form.save()
            formset.save()
            images_formset.save()
            messages.success(request, "Véhicule enregistré.")
            return redirect("cms_vehicule_list")
    return render(request, "cms/vehicule_form.html", {
        "form": form,
        "formset": formset,
        "images_formset": images_formset,
        "vehicule": vehicule,
        "marques_json": json.dumps(dict(Vehicule.MARQUES)),
    })


@login_required
@user_passes_test(_staff_required, login_url="/admin/login/")
def cms_vehicule_delete(request, pk):
    """cms : supprimer un véhicule."""
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == "POST":
        vehicule.delete()
        messages.success(request, "Véhicule supprimé.")
        return redirect("cms_vehicule_list")
    return render(request, "cms/vehicule_confirm_delete.html", {"vehicule": vehicule})
