from django.db import models


class Vehicule(models.Model):
    """Véhicule de luxe en vitrine (achat/vente sur RDV uniquement)."""

    MARQUES = [
        ("ferrari", "Ferrari"),
        ("lamborghini", "Lamborghini"),
        ("porsche", "Porsche"),
        ("mclaren", "McLaren"),
        ("bentley", "Bentley"),
        ("aston_martin", "Aston Martin"),
        ("rolls_royce", "Rolls-Royce"),
        ("other", "Autre"),
    ]

    titre = models.CharField(max_length=200)
    marque = models.CharField(max_length=50, choices=MARQUES)
    modele = models.CharField(max_length=120)
    annee = models.PositiveIntegerField()
    kilometrage = models.PositiveIntegerField(help_text="En km")
    prix = models.DecimalField(max_digits=12, decimal_places=0)
    puissance_ch = models.PositiveIntegerField(null=True, blank=True, verbose_name="Puissance (ch)")
    moteur = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    image_principale = models.ImageField(upload_to="vehicules/", blank=True, null=True)
    image_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL image (externe)",
        help_text="Image depuis internet si pas de fichier uploadé.",
    )
    en_vedette = models.BooleanField(default=False)
    ordre_affichage = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-ordre_affichage", "-created_at"]
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"

    def __str__(self):
        return f"{self.titre} ({self.annee})"


class OptionVehicule(models.Model):
    """Option / équipement du véhicule (liste libre, une entrée par ligne)."""

    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="options")
    libelle = models.CharField(max_length=200, verbose_name="Option")
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["ordre"]
        verbose_name = "Option véhicule"
        verbose_name_plural = "Options véhicule"

    def __str__(self):
        return self.libelle


class ImageVehicule(models.Model):
    """Images supplémentaires pour un véhicule (fichier ou URL)."""

    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vehicules/galerie/", blank=True, null=True)
    image_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL image (externe)",
        help_text="Lien vers une image si pas de fichier uploadé.",
    )
    legende = models.CharField(max_length=120, blank=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["ordre"]

    def __str__(self):
        return f"Image {self.ordre} - {self.vehicule.titre}"

    def get_image_display_url(self):
        """Retourne l'URL à afficher (fichier uploadé ou image_url)."""
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None


class RendezVous(models.Model):
    """Demande de rendez-vous depuis la page contact."""

    RAISON_CHOICES = [
        ("vendre", "Vendre son véhicule"),
        ("interesse", "Intéressé par un véhicule"),
        ("autre", "Autre"),
    ]

    nom = models.CharField(max_length=120)
    prenom = models.CharField(max_length=120)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    raison = models.CharField(max_length=20, choices=RAISON_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Demande de rendez-vous"
        verbose_name_plural = "Demandes de rendez-vous"

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.get_raison_display()}"


def contact_upload_to(instance, filename):
    """Chemin sécurisé : contact_uploads/année/mois/uuid_nom_sanitifé."""
    import uuid
    import os
    ext = os.path.splitext(filename)[1].lower()
    safe_name = f"{uuid.uuid4().hex[:12]}{ext}"
    return f"contact_uploads/{instance.rendez_vous.created_at:%Y/%m}/{safe_name}"


class RendezVousFichier(models.Model):
    """Pièce jointe d'une demande de rendez-vous."""

    rendez_vous = models.ForeignKey(
        RendezVous, on_delete=models.CASCADE, related_name="fichiers"
    )
    fichier = models.FileField(upload_to=contact_upload_to)

    class Meta:
        verbose_name = "Pièce jointe"
        verbose_name_plural = "Pièces jointes"

    def __str__(self):
        return self.fichier.name
