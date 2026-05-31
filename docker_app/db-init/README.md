# db-init

Ce dossier est optionnel.

Si tu ajoutes des fichiers `.sql` ou `.sh` ici, MySQL les execute automatiquement au premier demarrage du conteneur (quand le volume est vide).

Avec Django, laisse ce dossier vide dans la plupart des cas et utilise plutot :

- `python manage.py makemigrations`
- `python manage.py migrate`
