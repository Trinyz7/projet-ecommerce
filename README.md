# projet-ecommerce

Depot du projet de base de donnees e-commerce avec PostgreSQL.

membre du groupe : 
    

## Organisation

- `sql/` : scripts SQL de creation de la base et requetes utilisees dans le projet.
- `tests/` : tests Python de la base de donnees et de ses comportements attendus.
- `random/` : fichiers utiles a conserver qui ne rentrent pas dans les autres dossiers, brouillons et archives.
- `config.py` : configuration de connexion PostgreSQL, chargee depuis les variables d'environnement.
- `.env.example` : modele de configuration locale. Copier vers `.env` et renseigner les identifiants; `.env` ne doit pas etre versionne.
- `repartition_taches.txt` : repartition des taches du projet.

## Environnement Python

Activer l'environnement virtuel avec `./.venv/Scripts/Activate.ps1` dans PowerShell, puis installer les dependances avec `pip install -r requirements.txt`.

La configuration PostgreSQL utilise les variables `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` et `DB_PASSWORD`.