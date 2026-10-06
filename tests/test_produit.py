
def test_prix_produit_positif(compter):
    nb = compter("SELECT COUNT(*) FROM produit WHERE prix IS NULL OR prix <= 0")
    assert nb == 0, f"{nb} produit(s) avec un prix absent ou <= 0"


def test_stock_non_negatif(compter):
    nb = compter("SELECT COUNT(*) FROM produit WHERE stock_dispo IS NULL OR stock_dispo < 0")
    assert nb == 0, f"{nb} produit(s) avec un stock absent ou négatif"


def test_tous_les_produits_ont_ete_vendus(compter):
    nb = compter("""
        SELECT COUNT(*) FROM produit p
        LEFT JOIN ligne_commande l ON l.id_produit = p.id_produit
        WHERE l.id_produit IS NULL
    """)
    assert nb == 0, f"{nb} produit(s) jamais vendu(s)"