def test_colonnes_commande(conn):
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'commande'
    """)
    colonnes = {ligne[0] for ligne in cursor.fetchall()}
    attendues = {"id_client", "date_cmd", "statut"}
    assert attendues <= colonnes, f"Colonnes manquantes : {attendues - colonnes}"


def test_commande_a_un_client_existant(compter):
    nb = compter("""
        SELECT COUNT(*) FROM commande c
        LEFT JOIN client cl ON cl.id_client = c.id_client
        WHERE cl.id_client IS NULL
    """)
    assert nb == 0, f"{nb} commande(s) sans client valide"


def test_date_commande_renseignee(compter):
    nb = compter("SELECT COUNT(*) FROM commande WHERE date_cmd IS NULL")
    assert nb == 0, f"{nb} commande(s) sans date"


def test_statuts_autorises(compter):
    nb = compter("""
        SELECT COUNT(*) FROM commande
        WHERE statut IS NULL OR statut::text NOT IN ('payée', 'expédiée', 'livrée', 'annulée')
    """)
    assert nb == 0, f"{nb} commande(s) avec un statut absent ou interdit"


def test_un_client_peut_avoir_plusieurs_commandes(compter):
    nb = compter("""
        SELECT COUNT(*) FROM (
            SELECT id_client FROM commande GROUP BY id_client HAVING COUNT(*) > 1
        ) multi
    """)
    assert nb > 0, "Aucun client n'a plusieurs commandes"


def test_toute_commande_a_au_moins_une_ligne(compter):
    nb = compter("""
        SELECT COUNT(*) FROM commande c
        LEFT JOIN ligne_commande l ON l.id_commande = c.id_commande
        WHERE l.id_commande IS NULL
    """)
    assert nb == 0, f"{nb} commande(s) sans ligne"


def test_commande_apres_inscription(compter):
    
    nb = compter("""
        SELECT COUNT(*) FROM commande c
        JOIN client cl ON cl.id_client = c.id_client
        WHERE c.date_cmd < cl.date_creation
    """)
    assert nb == 0, f"{nb} commande(s) antérieure(s) à la création du client"