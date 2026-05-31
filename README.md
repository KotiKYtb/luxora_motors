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

Services exposes (accessibles via IP du serveur, ex. `http://192.168.1.10:8000`) :

- `app_user` (public) sur le port **8000** — toujours accessible
- `app_admin` (CMS) sur le port **8001** — Tailscale requis sur le serveur
- `app_documents` sur le port **8002** — Tailscale requis sur le serveur
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

### Acces via Tailscale (IP serveur ou localhost)

- **Site public (8000)** : accessible via l'IP du serveur sans Tailscale.
- **CMS (8001) et documents (8002)** : accessibles via la meme IP **uniquement si Tailscale est connecte sur le serveur**. Sinon redirection vers le site public (`8000`).

1. Lancer la stack Docker :
   - `cd docker_app && docker compose up -d --build`
2. Lancer la surveillance Tailscale :
   - **Linux/Debian** : `chmod +x scripts/tailscale-watch.sh && ./scripts/tailscale-watch.sh`
   - **Windows** : `.\scripts\tailscale-watch.ps1`
3. Acceder (remplacer `IP_SERVEUR` par l'IP de la machine) :
   - Site : `http://IP_SERVEUR:8000/`
   - CMS : `http://IP_SERVEUR:8001/cms/` (Tailscale actif)
   - Documents : `http://IP_SERVEUR:8002/` (Tailscale actif)

Pour desactiver temporairement la protection : `TAILSCALE_ADMIN_REQUIRED: "0"` dans `docker-compose.yml`.


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
