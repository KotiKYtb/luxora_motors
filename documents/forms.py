import os

from django import forms

from .models import DocumentVehicule

DOCUMENT_ALLOWED_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
}
DOCUMENT_MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 Mo


class DocumentVehiculeForm(forms.ModelForm):
    class Meta:
        model = DocumentVehicule
        fields = ["type_document", "titre", "fichier", "date_document", "notes"]
        widgets = {
            "type_document": forms.Select(attrs={"class": "cms-select"}),
            "titre": forms.TextInput(
                attrs={"class": "cms-input", "placeholder": "ex. CT du 12/03/2024"}
            ),
            "fichier": forms.FileInput(
                attrs={
                    "class": "cms-file",
                    "accept": ".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif,.webp",
                }
            ),
            "date_document": forms.DateInput(
                attrs={"class": "cms-input", "type": "date"}
            ),
            "notes": forms.Textarea(
                attrs={"class": "cms-textarea", "rows": 3, "placeholder": "Notes internes (optionnel)"}
            ),
        }

    def clean_fichier(self):
        fichier = self.cleaned_data.get("fichier")
        if not fichier and not (self.instance.pk and self.instance.fichier):
            raise forms.ValidationError("Un fichier est requis.")
        if not fichier:
            return fichier
        ext = os.path.splitext(getattr(fichier, "name", "") or "")[1].lower()
        if ext not in DOCUMENT_ALLOWED_EXTENSIONS:
            raise forms.ValidationError(
                f"Type non autorise ({ext or 'inconnu'}). "
                "Autorises : PDF, DOC, DOCX, XLS, XLSX, JPG, PNG, GIF, WEBP."
            )
        if fichier.size > DOCUMENT_MAX_FILE_SIZE:
            raise forms.ValidationError("Fichier trop volumineux (max 25 Mo).")
        return fichier
