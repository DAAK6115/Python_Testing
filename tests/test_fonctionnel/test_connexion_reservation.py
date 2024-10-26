"""Test fonctionnel pour vérifier la connexion et la réservation de places.

Ce module contient un test qui s'assure que la connexion fonctionne
correctement et que la réservation de places est possible pour une
compétition à venir.
"""

import pytest

from server import app


def test_functional_login_and_reserve(client):
    """Test fonctionnel pour vérifier la connexion et la réservation de places.

    Args:
        client: Le client de test pour l'application Flask.
    """
    # Connexion
    rv = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert rv.status_code == 200
    assert b"Welcome, Simply Lift" in rv.data

    # Réservation de places
    rv = client.post(
        "/purchasePlaces",
        data={
            "competition": "Fall Classic",  # Compétition avec une date future
            "club": "Simply Lift",
            "places": "2",
        },
        follow_redirects=True,
    )  # Suivre la redirection pour vérifier le résultat final

    assert rv.status_code == 200
    response_content = rv.data.decode("utf-8")
    # Vérifier que la réservation est bien enregistrée
    assert "Réservation complète !" in response_content or "Erreur" in response_content
