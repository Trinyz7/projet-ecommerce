def test_client_sans_commande_est_autorise(compter):
    
    nb = compter("""
        SELECT COUNT(*) FROM client cl
        LEFT JOIN commande c ON c.id_client = cl.id_client
        WHERE c.id_commande IS NULL
    """)
    assert nb > 0, "Aucun client sans commande : la règle n'est pas représentée"


def test_email_client_unique(compter):
    nb = compter("""
        SELECT COUNT(*) FROM (
            SELECT email FROM client GROUP BY email HAVING COUNT(*) > 1
        ) doublons
    """)
    assert nb == 0, f"{nb} e-mail(s) en doublon"


def test_champs_client_renseignes(compter):
    nb = compter("""
        SELECT COUNT(*) FROM client
        WHERE nom IS NULL OR TRIM(nom) = ''
           OR prenom IS NULL OR TRIM(prenom) = ''
           OR email IS NULL OR TRIM(email) = ''
           OR ville IS NULL OR date_creation IS NULL
    """)
    assert nb == 0, f"{nb} client(s) avec un champ obligatoire vide"