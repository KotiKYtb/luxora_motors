# luxora Motors

Site vitrine pour l’achat et la revente de véhicules d’exception (Lamborghini, Ferrari, Porsche, McLaren, etc.).  
**Pas de vente en ligne** : prise de rendez-vous et contact par téléphone uniquement.

## Palette

- **Gris titane** : `#2B2F34`
- **Argent métallique** : `#BFC3C9`
- **Vert racing profond** : `#0F3D2E`
- **Blanc froid** : `#F2F2F2`

## Environnement

- Python 3 + **venv**
- Django 5+
- Pillow (images)

## Installation

```bash
# Créer et activer le venv
python -m venv venv
# Windows PowerShell :
.\venv\Scripts\Activate.ps1
# Windows CMD : venv\Scripts\activate.bat
# Linux/macOS : source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py load_demo_vehicules   # véhicules de démo
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/

## Admin

- Créer un superutilisateur : `python manage.py createsuperuser`
- Interface d’admin : http://127.0.0.1:8000/admin/
- Gérer les véhicules (marque, modèle, prix, km, image, « en vedette », etc.)

## Structure

- **Landing** : hero + sélection « en vedette » + lien vers la collection
- **Collection** : liste de tous les véhicules avec cartes animées
- **Fiche véhicule** : galerie, specs, description, CTA « Appeler pour un rendez-vous » (pas d’achat en ligne)
- **Contact** : bandeau téléphone + « Sur rendez-vous uniquement »

Les animations (fade-up, scroll reveal, hover sur les cartes) sont en CSS/JS pur, sans framework front.
