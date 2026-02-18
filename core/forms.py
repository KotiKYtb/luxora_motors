import os
import os
from django import forms
from django.forms import inlineformset_factory

from .models import Vehicule, OptionVehicule, ImageVehicule, RendezVous

# Pièces jointes contact : extensions autorisées (documents + images)
CONTACT_ALLOWED_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".jpg", ".jpeg", ".png", ".gif",
}
CONTACT_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 Mo
CONTACT_MAX_FILES = 5, RendezVous

# Extensions autorisées pour les pièces jointes contact (pas de .exe, .config, etc.)
CONTACT_ALLOWED_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".jpg", ".jpeg", ".png", ".gif",
}
CONTACT_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 Mo
CONTACT_MAX_FILES = 5


class MultipleFileInput(forms.FileInput):
    """Widget qui rend un <input type="file" multiple> sans déclencher l’erreur Django."""
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["multiple"] = True
        return attrs


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


class RendezVousForm(forms.ModelForm):
    """Formulaire de prise de rendez-vous (page contact). Pièces jointes validées côté serveur."""

    fichiers = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={
            "class": "contact-file-input",
            "accept": ".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif",
        }),
        label="Pièces jointes (optionnel)",
        help_text=f"Documents ou images. Max {CONTACT_MAX_FILES} fichiers, 10 Mo chacun. Types : PDF, DOC, DOCX, XLS, XLSX, JPG, PNG, GIF.",
    )

    class Meta:
        model = RendezVous
        fields = ["nom", "prenom", "email", "telephone", "raison", "message"]
        labels = {
            "nom": "Nom",
            "prenom": "Prénom",
            "email": "E-mail",
            "telephone": "Téléphone",
            "raison": "Raison de la demande",
            "message": "Message (optionnel)",
        }
        widgets = {
            "nom": forms.TextInput(attrs={"class": "contact-input", "placeholder": "Nom"}),
            "prenom": forms.TextInput(attrs={"class": "contact-input", "placeholder": "Prénom"}),
            "email": forms.EmailInput(attrs={"class": "contact-input", "placeholder": "Adresse e-mail"}),
            "telephone": forms.TextInput(attrs={"class": "contact-input", "placeholder": "Téléphone"}),
            "raison": forms.Select(attrs={"class": "contact-select"}),
            "message": forms.Textarea(attrs={"class": "contact-textarea", "rows": 5, "placeholder": "Votre message..."}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_fichiers(self):
        """On valide un seul fichier ici ; les multiples sont validés dans la vue."""
        return self.cleaned_data.get("fichiers")

    def clean(self):
        data = super().clean()
        if not self.request:
            return data
        files = self.request.FILES.getlist("fichiers")
        if len(files) > CONTACT_MAX_FILES:
            self.add_error(
                "fichiers",
                forms.ValidationError(f"Maximum {CONTACT_MAX_FILES} fichiers autorisés.")
            )
            return data
        for f in files:
            ext = os.path.splitext(getattr(f, "name", "") or "")[1].lower()
            if ext not in CONTACT_ALLOWED_EXTENSIONS:
                self.add_error(
                    "fichiers",
                    forms.ValidationError(f"Type de fichier non autorisé : {ext or '(inconnu)'}. Autorisés : PDF, DOC, DOCX, XLS, XLSX, JPG, PNG, GIF.")
                )
                break
            if f.size > CONTACT_MAX_FILE_SIZE:
                self.add_error(
                    "fichiers",
                    forms.ValidationError(f"Fichier trop volumineux : {f.name}. Maximum 10 Mo par fichier.")
                )
                break
        return data
