import os
import uuid

from django.conf import settings
from django.db import models

from core.models import Vehicule


def document_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    safe_name = f"{uuid.uuid4().hex[:12]}{ext}"
    return f"vehicules/documents/{instance.vehicule_id}/{safe_name}"


class DocumentVehicule(models.Model):
    """Document administratif lie a un vehicule (CT, entretien, carte grise, etc.)."""

    TYPE_CHOICES = [
        ("controle_technique", "Contrôle technique"),
        ("rapport_entretien", "Rapport d'entretien"),
        ("carte_grise", "Carte grise"),
        ("carte_grise_ancienne", "Ancienne carte grise"),
        ("facture", "Facture"),
        ("garantie", "Garantie"),
        ("contrat", "Contrat / cession"),
        ("expertise", "Rapport d'expertise"),
        ("autre", "Autre"),
    ]

    vehicule = models.ForeignKey(
        Vehicule, on_delete=models.CASCADE, related_name="documents"
    )
    type_document = models.CharField(max_length=40, choices=TYPE_CHOICES)
    titre = models.CharField(
        max_length=200,
        blank=True,
        help_text="Libelle libre (ex. CT 2024, révision 15 000 km).",
    )
    fichier = models.FileField(upload_to=document_upload_to)
    date_document = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date du document",
        help_text="Date figurant sur le document (CT, facture, etc.).",
    )
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents_uploades",
    )

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Document véhicule"
        verbose_name_plural = "Documents véhicules"

    def __str__(self):
        label = self.titre or self.get_type_document_display()
        return f"{label} — {self.vehicule.titre}"

    @property
    def libelle(self):
        return self.titre or self.get_type_document_display()

    @property
    def extension(self):
        return os.path.splitext(self.fichier.name)[1].lower()
