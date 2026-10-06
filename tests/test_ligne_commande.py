def test_colonnes_ligne_commande(conn):
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'ligne_commande'
    """)
    colonnes = {ligne[0] for ligne in cursor.fetchall()}
    attendues = {"id_commande", "id_produit", "quantite", "prix_unitaire"}
    assert attendues <= colonnes, f"Colonnes manquantes : {attendues - colonnes}"


def test_ligne_a_une_commande_existante(compter):
    nb = compter("""
        SELECT COUNT(*) FROM ligne_commande l
        LEFT JOIN commande c ON c.id_commande = l.id_commande
        WHERE c.id_commande IS NULL
    """)
    assert nb == 0, f"{nb} ligne(s) sans commande valide"


def test_ligne_a_un_produit_existant(compter):
    nb = compter("""
        SELECT COUNT(*) FROM ligne_commande l
        LEFT JOIN produit p ON p.id_produit = l.id_produit
        WHERE p.id_produit IS NULL
    """)
    assert nb == 0, f"{nb} ligne(s) sans produit valide"


def test_quantite_positive(compter):
    nb = compter("SELECT COUNT(*) FROM ligne_commande WHERE quantite IS NULL OR quantite <= 0")
    assert nb == 0, f"{nb} ligne(s) avec une quantité absente ou <= 0"


def test_prix_unitaire_renseigne_et_positif(compter):
    nb = compter("SELECT COUNT(*) FROM ligne_commande WHERE prix_unitaire IS NULL OR prix_unitaire <= 0")
    assert nb == 0, f"{nb} ligne(s) avec un prix unitaire absent ou <= 0"


def test_prix_paye_peut_differer_du_prix_actuel(compter):
    ix
    nb = compter("""
        SELECT COUNT(*) FROM ligne_commande l
        JOIN produit p ON p.id_produit = l.id_produit
        WHERE l.prix_unitaire <> p.prix
    """)
    assert nb > 0, "Aucune ligne n'a un prix payé différent du prix actuel"


def test_pas_de_produit_en_double_dans_une_commande(compter):
    nb = compter("""
        SELECT COUNT(*) FROM (
            SELECT id_commande, id_produit FROM ligne_commande
            GROUP BY id_commande, id_produit HAVING COUNT(*) > 1
        ) doublons
    """)
    assert nb == 0, f"{nb} produit(s) en double dans une même commande"