"""Test d'intégration pour vérifier la connexion avec un email valide.

Ce module s'assure que la connexion avec un email valide fonctionne
correctement.
"""

import pytest

from server import app


def test_valid_email_login(client):
    """Test de la connexion avec un email valide.

    Args:
        client: Le client de test pour l'application Flask.
    """
    rv = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert rv.status_code == 200
    assert b"Welcome, Simply Lift" in rv.data
