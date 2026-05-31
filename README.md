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
- PyMySQL (connexion MySQL)

## Installation

```bash
# Créer et activer le venv
python -m venv venv
# Windows PowerShell :
.\venv\Scripts\Activate.ps1
# Windows CMD : venv\Scripts\activate.bat
# Linux/macOS : source venv/bin/activate

pip install -r requirements.txt
```

## Architecture séparée (public + admin + documents)

Le projet est séparé en **3 applications Django distinctes** dans `docker_app` :

- `docker_app/app-user` : application publique
- `docker_app/app-admin` : application admin/cms + Django admin
- `docker_app/app-documents` : répertoire documentaire véhicules (CT, cartes grises, entretiens…)
- code partagé (models, templates, static) monte via `/shared` dans les conteneurs

## Docker (3 apps + MySQL)

La stack Docker est définie dans `docker_app/docker-compose.yml` avec separation physique :

- `docker_app/app-user` : projet Django public
- `docker_app/app-admin` : projet Django admin/cms
- `docker_app/app-documents` : projet Django documents internes
- `docker_app/db-init` : scripts SQL optionnels executes au premier demarrage MySQL

Services exposes :

- `app_user` (public) sur `http://127.0.0.1:8000`
- `app_admin` (admin/cms) sur `http://127.0.0.1:8001`
- `app_documents` (documents) sur `http://127.0.0.1:8002`
- `database` (MySQL) isolee sur le reseau interne

Lancement :

```bash
cd docker_app
docker compose up --build
```

## Admin & documents (Tailscale requis)

- Créer un superutilisateur (une seule fois, base partagée) :
  - `docker compose exec app_admin python manage.py createsuperuser`
- **CMS véhicules** : http://127.0.0.1:8001/cms/
- **Documents véhicules** : http://127.0.0.1:8002/ (app Docker dédiée, port 8002)
- Django admin CMS : http://127.0.0.1:8001/admin/
- Django admin documents : http://127.0.0.1:8002/admin/

### Acces via Tailscale (localhost)

Les apps admin (`8001`) et documents (`8002`) restent sur **localhost**.
L’accès n’est autorisé que si Tailscale est **connecté** sur la machine hôte.
Sinon, redirection vers le site public (`8000`).

1. Lancer la stack Docker :
   - `cd docker_app && docker compose up -d --build`
2. Lancer la surveillance Tailscale (2e fenetre PowerShell) :
   - `.\scripts\tailscale-watch.ps1`
3. Ouvrir en local (Tailscale actif) :
   - CMS : http://127.0.0.1:8001/cms/
   - Documents : http://127.0.0.1:8002/

Pour desactiver temporairement (dev local) : `TAILSCALE_ADMIN_REQUIRED: "0"` dans `docker-compose.yml`.


## Acces MySQL (Docker)

- Ouvrir un shell MySQL :
  - `docker compose exec database mysql -u root -p`
- Se connecter directement a la base applicative :
  - `docker compose exec database mysql -u luxora_user -p luxora_motors`
- Afficher les tables :
  - `SHOW TABLES;`

## Structure

- **Landing** : hero + sélection « en vedette » + lien vers la collection
- **Collection** : liste de tous les véhicules avec cartes animées
- **Fiche véhicule** : galerie, specs, description, CTA « Appeler pour un rendez-vous » (pas d’achat en ligne)
- **Contact** : bandeau téléphone + « Sur rendez-vous uniquement »

Les animations (fade-up, scroll reveal, hover sur les cartes) sont en CSS/JS pur, sans framework front.
