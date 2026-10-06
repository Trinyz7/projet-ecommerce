def test_nombre_clients(compter):
    assert compter("SELECT COUNT(*) FROM client") == 100


def test_nombre_produits(compter):
    assert compter("SELECT COUNT(*) FROM produit") == 65


def test_nombre_commandes(compter):
    assert compter("SELECT COUNT(*) FROM commande") == 500


def test_nombre_lignes_commande(compter):
    assert compter("SELECT COUNT(*) FROM ligne_commande") == 1547