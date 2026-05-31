from django.contrib import admin

from .models import DocumentVehicule


@admin.register(DocumentVehicule)
class DocumentVehiculeAdmin(admin.ModelAdmin):
    list_display = ("libelle", "vehicule", "type_document", "date_document", "uploaded_at")
    list_filter = ("type_document", "uploaded_at")
    search_fields = ("titre", "vehicule__titre", "vehicule__modele", "notes")
    readonly_fields = ("uploaded_at", "uploaded_by")
    raw_id_fields = ("vehicule",)

    def save_model(self, request, obj, form, change):
        if not change or not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
