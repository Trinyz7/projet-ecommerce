
def test_prix_produit_positif(compter):
    nb = compter("SELECT COUNT(*) FROM produit WHERE prix IS NULL OR prix <= 0")
    assert nb == 0, f"{nb} produit(s) avec un prix absent ou <= 0"


def test_stock_non_negatif(compter):
    nb = compter("SELECT COUNT(*) FROM produit WHERE stock IS NULL OR stock < 0")
    assert nb == 0, f"{nb} produit(s) avec un stock absent ou négatif"


def test_cinq_produits_ne_sont_jamais_vendus(compter):
    nb = compter("""
        SELECT COUNT(*) FROM produit p
        LEFT JOIN ligne_commande l ON l.produit_id = p.id
        WHERE l.produit_id IS NULL
    """)
    assert nb == 5, f"{nb} produit(s) jamais vendu(s), 5 attendus"