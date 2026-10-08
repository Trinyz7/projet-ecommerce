def test_colonnes_ligne_commande(conn):
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'ligne_commande'
    """)
    colonnes = {ligne[0] for ligne in cursor.fetchall()}
    attendues = {"commande_id", "produit_id", "quantite", "prix_unitaire"}
    assert attendues <= colonnes, f"Colonnes manquantes : {attendues - colonnes}"


def test_ligne_a_une_commande_existante(compter):
    nb = compter("""
        SELECT COUNT(*) FROM ligne_commande l
        LEFT JOIN commande c ON c.id = l.commande_id
        WHERE c.id IS NULL
    """)
    assert nb == 0, f"{nb} ligne(s) sans commande valide"


def test_ligne_a_un_produit_existant(compter):
    nb = compter("""
        SELECT COUNT(*) FROM ligne_commande l
        LEFT JOIN produit p ON p.id = l.produit_id
        WHERE p.id IS NULL
    """)
    assert nb == 0, f"{nb} ligne(s) sans produit valide"


def test_quantite_positive(compter):
    nb = compter("SELECT COUNT(*) FROM ligne_commande WHERE quantite IS NULL OR quantite <= 0")
    assert nb == 0, f"{nb} ligne(s) avec une quantité absente ou <= 0"


def test_prix_unitaire_renseigne_et_positif(compter):
    nb = compter("SELECT COUNT(*) FROM ligne_commande WHERE prix_unitaire IS NULL OR prix_unitaire <= 0")
    assert nb == 0, f"{nb} ligne(s) avec un prix unitaire absent ou <= 0"


def test_prix_paye_peut_differer_du_prix_actuel(compter):
    nb = compter("""
        SELECT COUNT(*) FROM ligne_commande l
        JOIN produit p ON p.id = l.produit_id
        WHERE l.prix_unitaire <> p.prix
    """)
    assert nb > 0, "Aucune ligne n'a un prix payé différent du prix actuel"


def test_pas_de_produit_en_double_dans_une_commande(compter):
    nb = compter("""
        SELECT COUNT(*) FROM (
            SELECT commande_id, produit_id FROM ligne_commande
            GROUP BY commande_id, produit_id HAVING COUNT(*) > 1
        ) doublons
    """)
    assert nb == 0, f"{nb} produit(s) en double dans une même commande"