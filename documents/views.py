from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Vehicule

from .forms import DocumentVehiculeForm
from .models import DocumentVehicule


def _staff_required(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(_staff_required, login_url="/admin/login/")
def cms_document_vehicule_list(request):
    """Liste des vehicules avec nombre de documents."""
    vehicules = (
        Vehicule.objects.annotate(nb_documents=Count("documents"))
        .order_by("-ordre_affichage", "-created_at")
    )
    return render(request, "documents/vehicule_list.html", {"vehicules": vehicules})


@login_required
@user_passes_test(_staff_required, login_url="/admin/login/")
def cms_document_list(request, vehicule_pk):
    """Documents d'un vehicule, groupes par type."""
    vehicule = get_object_or_404(Vehicule, pk=vehicule_pk)
    documents = vehicule.documents.select_related("uploaded_by").order_by("-uploaded_at")
    type_filter = request.GET.get("type", "").strip()
    if type_filter:
        documents = documents.filter(type_document=type_filter)

    documents_by_type = {}
    for doc in documents:
        documents_by_type.setdefault(doc.type_document, []).append(doc)

    grouped_documents = []
    for type_value, type_label in DocumentVehicule.TYPE_CHOICES:
        docs = documents_by_type.get(type_value, [])
        if docs:
            grouped_documents.append(
                {"type": type_value, "label": type_label, "documents": docs}
            )

    return render(
        request,
        "documents/document_list.html",
        {
            "vehicule": vehicule,
            "documents": documents,
            "grouped_documents": grouped_documents,
            "type_choices": DocumentVehicule.TYPE_CHOICES,
            "type_filter": type_filter,
        },
    )


@login_required
@user_passes_test(_staff_required, login_url="/admin/login/")
def cms_document_create(request, vehicule_pk):
    vehicule = get_object_or_404(Vehicule, pk=vehicule_pk)
    form = DocumentVehiculeForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        doc = form.save(commit=False)
        doc.vehicule = vehicule
        doc.uploaded_by = request.user
        doc.save()
        messages.success(request, "Document ajoute.")
        return redirect("cms_document_list", vehicule_pk=vehicule.pk)
    return render(
        request,
        "documents/document_form.html",
        {"form": form, "vehicule": vehicule, "is_edit": False},
    )


@login_required
@user_passes_test(_staff_required, login_url="/admin/login/")
def cms_document_delete(request, pk):
    document = get_object_or_404(DocumentVehicule.objects.select_related("vehicule"), pk=pk)
    vehicule = document.vehicule
    if request.method == "POST":
        document.fichier.delete(save=False)
        document.delete()
        messages.success(request, "Document supprime.")
        return redirect("cms_document_list", vehicule_pk=vehicule.pk)
    return render(
        request,
        "documents/document_confirm_delete.html",
        {"document": document, "vehicule": vehicule},
    )
