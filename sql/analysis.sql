-- Exercise 1
SELECT nom, categorie, prix, stock_dispo FROM Produit;

SELECT nom, categorie, prix, stock_dispo FROM Produit WHERE prix > 100;

-- Exercise 2
SELECT * FROM Client WHERE ville='Paris';

SELECT ville, COUNT(*) AS nombre_clients FROM Client GROUP BY ville;

-- Exercise 3
SELECT cmd.id_commande, cmd.date_cmd, cmd.statut, cl.* FROM Client cl JOIN Commande cmd ON cl.id_client = cmd.id_client ;

-- Exercise 4
SELECT lc.id_commande, lc.id_produit, lc.quantite, lc.prix_unitaire, ROUND(lc.quantite * lc.prix_unitaire, 2) AS montant_ligne FROM Ligne_commande lc;

-- Exercise 5
SELECT cmd.id_commande, cmd.date_cmd, cmd.statut, ROUND(SUM(lc.quantite * lc.prix_unitaire), 2) AS montant_total FROM Commande cmd JOIN Ligne_commande lc ON cmd.id_commande = lc.id_commande GROUP BY cmd.id_commande, cmd.date_cmd, cmd.statut ORDER BY cmd.id_commande;

-- Exercise 6
SELECT p.categorie, ROUND(SUM(lc.quantite * lc.prix_unitaire), 2) AS chiffre_affaires, SUM(lc.quantite) AS quantite_totale_vendue FROM Ligne_commande lc JOIN Commande cmd ON lc.id_commande = cmd.id_commande JOIN Produit p ON lc.id_produit = p.id_produit WHERE cmd.statut <> 'annulée' GROUP BY p.categorie ORDER BY chiffre_affaires DESC;

-- Exercise 15.A
SELECT 'Client' AS table_name, COUNT(*) AS total_rows FROM Client
UNION ALL SELECT 'Produit' AS table_name, COUNT(*) AS total_rows FROM Produit
UNION ALL SELECT 'Commande' AS table_name, COUNT(*) AS total_rows FROM Commande
UNION ALL SELECT 'Ligne_commande' AS table_name, COUNT(*) AS total_rows FROM Ligne_commande;

SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name IN ('Client', 'Produit', 'Commande', 'Ligne_commande') ORDER BY table_name, column_name;

SELECT * FROM Client WHERE nom is NULL OR prenom is NULL OR email is NULL OR ville is NULL OR date_creation is NULL;

-- Exercise 15.B
SELECT SUM(lc.prix_unitaire * lc.quantite) AS total_affairs, COUNT(DISTINCT cmd.id_commande) AS nombre_commandes, ROUND(SUM(lc.prix_unitaire * lc.quantite) / NULLIF(COUNT(DISTINCT cmd.id_commande), 0), 2) AS panier_moyen, COUNT(DISTINCT cmd.id_commande) AS nombre_clients_actifs FROM Commande cmd JOIN Ligne_commande lc ON cmd.id_commande = lc.id_commande WHERE cmd.statut <> 'annulée';