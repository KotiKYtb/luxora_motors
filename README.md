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

### Acces CMS / documents (liste blanche IP Tailscale)

Les apps tournent sur **l'IP de la machine** (ex. `http://192.168.1.10:8000`).

- **Site public (`8000`)** : accessible par tout le monde.
- **CMS (`8001`) et documents (`8002`)** : accessibles **uniquement** si l'**IP Tailscale du client** est enregistree sur la VM.

Sinon → redirection vers le site public.

**Enregistrer un utilisateur autorise** — editer `config/allowed_tailscale_ips.txt` sur la VM :

```bash
# Recuperer son IP Tailscale (sur le PC de l'utilisateur)
tailscale ip -4

# Ajouter la ligne dans le fichier sur le serveur
nano ~/luxora_motors/config/allowed_tailscale_ips.txt
# ex. 100.108.154.112
```

Pas besoin de redemarrer Docker : le fichier est relu a chaque requete.

**Acces utilisateur autorise** (ex. IP machine `192.168.1.10`) :
- CMS : `http://192.168.1.10:8001/cms/`
- Documents : `http://192.168.1.10:8002/`

Dev local Windows : `TAILSCALE_ALLOW_LOCALHOST: "1"` dans `docker-compose.yml`.

### Debian / production Linux

Sur Linux, Docker masque souvent l'IP cliente. Utiliser le compose production :

```bash
cd docker_app
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Supprimer l'ancien fichier obsolete (ancienne logique) :

```bash
rm -f ~/luxora_motors/.tailscale_active
```


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
