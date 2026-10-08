-- Exercise 1
SELECT nom, categorie, prix, stock FROM produit;

SELECT nom, categorie, prix, stock FROM produit WHERE prix > 100;

-- Exercise 2
SELECT * FROM client WHERE ville = 'Paris';

SELECT ville, COUNT(*) AS nombre_clients FROM client GROUP BY ville;

-- Exercise 3
SELECT cmd.id, cmd.date_commande, cmd.statut, cl.*
FROM client cl
JOIN commande cmd ON cl.id = cmd.client_id;

-- Exercise 4
SELECT
    lc.commande_id,
    lc.produit_id,
    lc.quantite,
    lc.prix_unitaire,
    ROUND(lc.quantite * lc.prix_unitaire, 2) AS montant_ligne
FROM ligne_commande lc;

-- Exercise 5
SELECT
    cmd.id,
    cmd.date_commande,
    cmd.statut,
    ROUND(SUM(lc.quantite * lc.prix_unitaire), 2) AS montant_total
FROM commande cmd
JOIN ligne_commande lc ON cmd.id = lc.commande_id
GROUP BY cmd.id, cmd.date_commande, cmd.statut
ORDER BY cmd.id;

-- Exercise 6
SELECT
    p.categorie,
    ROUND(SUM(lc.quantite * lc.prix_unitaire), 2) AS chiffre_affaires,
    SUM(lc.quantite) AS quantite_totale_vendue
FROM ligne_commande lc
JOIN commande cmd ON lc.commande_id = cmd.id
JOIN produit p ON lc.produit_id = p.id
WHERE cmd.statut <> 'annulée'
GROUP BY p.categorie
ORDER BY chiffre_affaires DESC;

-- EXERCICE 10 — PANIER MOYEN
SELECT
    ROUND(
        SUM(lc.quantite * lc.prix_unitaire)
        / NULLIF(COUNT(DISTINCT cmd.id), 0),
        2
    ) AS panier_moyen
FROM commande cmd
JOIN ligne_commande lc ON cmd.id = lc.commande_id
WHERE cmd.statut <> 'annulée';

SELECT
    DATE_TRUNC('month', cmd.date_commande) AS mois,
    ROUND(
        SUM(lc.quantite * lc.prix_unitaire)
        / NULLIF(COUNT(DISTINCT cmd.id), 0),
        2
    ) AS panier_moyen
FROM commande cmd
JOIN ligne_commande lc ON cmd.id = lc.commande_id
WHERE cmd.statut <> 'annulée'
GROUP BY DATE_TRUNC('month', cmd.date_commande)
ORDER BY mois;

-- EXERCICE 11 — CATEGORISER LES COMMANDES
SELECT
    cmd.id AS id_commande,
    cmd.date_commande,
    cmd.statut,
    ROUND(SUM(lc.quantite * lc.prix_unitaire), 2) AS montant_total,
    CASE
        WHEN SUM(lc.quantite * lc.prix_unitaire) < 500 THEN 'Petit panier'
        WHEN SUM(lc.quantite * lc.prix_unitaire) < 1500 THEN 'Panier moyen'
        ELSE 'Gros panier'
    END AS categorie_panier
FROM commande cmd
JOIN ligne_commande lc ON cmd.id = lc.commande_id
GROUP BY cmd.id, cmd.date_commande, cmd.statut
ORDER BY cmd.id;

-- EXERCICE 12 — ANALYSE TEMPORELLE
SELECT
    DATE_TRUNC('month', cmd.date_commande) AS mois,
    ROUND(SUM(lc.quantite * lc.prix_unitaire), 2) AS chiffre_affaires,
    SUM(lc.quantite) AS quantite_vendue,
    COUNT(DISTINCT cmd.id) AS nombre_commandes
FROM commande cmd
JOIN ligne_commande lc ON cmd.id = lc.commande_id
WHERE cmd.statut <> 'annulée'
GROUP BY DATE_TRUNC('month', cmd.date_commande)
ORDER BY mois;

-- EXERCICE 13 — DETECTER UNE INCOHERENCE
SELECT
    cmd.id AS id_commande,
    cl.id AS id_client,
    cmd.date_commande,
    cl.date_inscription
FROM commande cmd
JOIN client cl ON cl.id = cmd.client_id
WHERE cmd.date_commande < cl.date_inscription
ORDER BY cmd.id;

SELECT COUNT(*) AS nombre_anomalies
FROM commande cmd
JOIN client cl ON cl.id = cmd.client_id
WHERE cmd.date_commande < cl.date_inscription;

-- EXERCICE 14 — PRODUITS SANS VENTE
SELECT
    p.id AS id_produit,
    p.nom,
    p.categorie,
    p.prix,
    p.stock
FROM produit p
LEFT JOIN ligne_commande lc ON lc.produit_id = p.id
WHERE lc.produit_id IS NULL
ORDER BY p.id;

-- Exercise 15.A
SELECT 'client' AS table_name, COUNT(*) AS total_rows FROM client
UNION ALL SELECT 'produit', COUNT(*) FROM produit
UNION ALL SELECT 'commande', COUNT(*) FROM commande
UNION ALL SELECT 'ligne_commande', COUNT(*) FROM ligne_commande;

SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('client', 'produit', 'commande', 'ligne_commande')
ORDER BY table_name, column_name;

SELECT *
FROM client
WHERE nom IS NULL OR prenom IS NULL OR email IS NULL
   OR ville IS NULL OR date_inscription IS NULL;

-- Exercise 15.B
SELECT
    SUM(lc.prix_unitaire * lc.quantite) AS chiffre_affaires,
    COUNT(DISTINCT cmd.id) AS nombre_commandes,
    ROUND(
        SUM(lc.prix_unitaire * lc.quantite)
        / NULLIF(COUNT(DISTINCT cmd.id), 0),
        2
    ) AS panier_moyen,
    COUNT(DISTINCT cmd.client_id) AS nombre_clients_actifs
FROM commande cmd
JOIN ligne_commande lc ON lc.commande_id = cmd.id
WHERE cmd.statut <> 'annulée';