# projet-ecommerce

Projet de base de données e-commerce avec PostgreSQL.

## Organisation

- `sql/create_schema.sql` : création des tables et contraintes.
- `sql/seed_ecommerce.sql` : insertion du jeu de données.
- `sql/analysis.sql` : requêtes d'analyse à exécuter après le chargement des données.
- `setup_database.py` : création de la base, du schéma et chargement des données.
- `tests/` : tests Python d'intégrité et de contenu.
- `config.py` : configuration PostgreSQL chargée depuis les variables d'environnement.

## Installation et configuration (PowerShell)

Depuis la racine du dépôt, créez/activez un environnement virtuel et installez les dépendances :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copiez le fichier de configuration exemple puis renseignez les paramètres de connexion :

```powershell
Copy-Item .env.example .env
```

Configurez `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` et `DB_PASSWORD` dans `.env`.
L'utilisateur PostgreSQL doit pouvoir se connecter à la base système `postgres` et
avoir le droit de créer une base (`CREATEDB`). Le serveur doit aussi autoriser cette
connexion dans sa configuration `pg_hba.conf`.

## Créer et remplir la base

Lancez depuis la racine du dépôt :

```powershell
python setup_database.py
```

Le script crée la base indiquée par `DB_NAME`, exécute `sql/create_schema.sql`, puis
charge `sql/seed_ecommerce.sql`. Il s'arrête si la base existe déjà afin d'éviter
d'effacer des données par inadvertance.

Pour supprimer et recréer la base existante, utilisez la commande destructive
suivante et confirmez le nom de la base à l'invite :

```powershell
python setup_database.py --reset
```

## Vérifier les données et lancer les requêtes

Lancez les tests automatisés :

```powershell
pytest
```

Pour exécuter toutes les requêtes d'analyse, utilisez `psql` :

```powershell
psql -h localhost -p 5432 -U groupe_2 -d ecommerce -f sql/analysis.sql
```

Adaptez l'hôte, le port, l'utilisateur et le nom de la base aux valeurs de `.env`.
Par exemple, pour vérifier les volumes du jeu de données dans `psql` :

```sql
SELECT 'client' AS table_name, COUNT(*) FROM client
UNION ALL SELECT 'produit', COUNT(*) FROM produit
UNION ALL SELECT 'commande', COUNT(*) FROM commande
UNION ALL SELECT 'ligne_commande', COUNT(*) FROM ligne_commande;
```

Les nombres attendus sont respectivement 100 clients, 65 produits, 500 commandes
et 1547 lignes de commande.
