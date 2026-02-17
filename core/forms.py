from django import forms
from django.forms import inlineformset_factory

from .models import Vehicule, OptionVehicule, ImageVehicule


class VehiculeForm(forms.ModelForm):
    """Formulaire complet pour créer/éditer un véhicule (tous les champs)."""

    class Meta:
        model = Vehicule
        fields = [
            "titre",
            "marque",
            "modele",
            "annee",
            "kilometrage",
            "prix",
            "puissance_ch",
            "moteur",
            "description",
            "image_principale",
            "image_url",
            "en_vedette",
            "ordre_affichage",
        ]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "cms-input", "placeholder": "ex. Ferrari Roma"}),
            "marque": forms.Select(attrs={"class": "cms-select"}),
            "modele": forms.TextInput(attrs={"class": "cms-input", "placeholder": "ex. Roma"}),
            "annee": forms.NumberInput(attrs={"class": "cms-input", "min": 1900, "max": 2030}),
            "kilometrage": forms.NumberInput(attrs={"class": "cms-input", "min": 0}),
            "prix": forms.NumberInput(attrs={"class": "cms-input", "min": 0}),
            "puissance_ch": forms.NumberInput(attrs={"class": "cms-input", "min": 0}),
            "moteur": forms.TextInput(attrs={"class": "cms-input", "placeholder": "ex. V8 3.9 L twin-turbo"}),
            "description": forms.Textarea(attrs={"class": "cms-textarea", "rows": 4}),
            "image_principale": forms.FileInput(attrs={"class": "cms-file", "accept": "image/*"}),
            "image_url": forms.URLInput(attrs={"class": "cms-input", "placeholder": "https://..."}),
            "en_vedette": forms.CheckboxInput(attrs={"class": "cms-checkbox"}),
            "ordre_affichage": forms.NumberInput(attrs={"class": "cms-input", "min": 0}),
        }


OptionVehiculeFormSet = inlineformset_factory(
    Vehicule,
    OptionVehicule,
    fields=("libelle", "ordre"),
    extra=1,
    can_delete=True,
    max_num=1000,
    widgets={
        "libelle": forms.TextInput(attrs={"class": "cms-input", "placeholder": "Nom de l'option"}),
        "ordre": forms.NumberInput(attrs={"class": "cms-input cms-input-sm", "min": 0}),
    },
)

class ImageVehiculeForm(forms.ModelForm):
    """Une image secondaire : fichier OU URL (au moins un des deux)."""

    class Meta:
        model = ImageVehicule
        fields = ("image", "image_url", "legende", "ordre")
        widgets = {
            "image": forms.FileInput(attrs={"class": "cms-file-input", "accept": "image/*"}),
            "image_url": forms.URLInput(attrs={"class": "cms-input", "placeholder": "https://..."}),
            "legende": forms.TextInput(attrs={"class": "cms-input", "placeholder": "Légende (optionnel)"}),
            "ordre": forms.NumberInput(attrs={"class": "cms-input cms-input-sm", "min": 0}),
        }

    def clean(self):
        data = super().clean()
        if data.get("DELETE"):
            return data
        image = data.get("image")
        image_url = (data.get("image_url") or "").strip()
        has_new = bool(image) or bool(image_url)
        has_existing = self.instance.pk and self.instance.get_image_display_url()
        if not has_new and not has_existing:
            raise forms.ValidationError("Indiquez soit un fichier image, soit une URL d'image.")
        return data


ImageVehiculeFormSet = inlineformset_factory(
    Vehicule,
    ImageVehicule,
    form=ImageVehiculeForm,
    extra=1,
    can_delete=True,
    max_num=50,
)
