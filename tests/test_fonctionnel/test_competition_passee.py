"""Test fonctionnel pour vérifier que les réservations ne sont pas possibles
pour une compétition passée.

Ce module contient un test qui vérifie qu'une tentative de réservation
pour une compétition passée est refusée par le système.
"""

import pytest

from server import app  # Ceci est nécessaire si votre test a besoin de l'application


def test_functional_reserve_past_competition(client):
    """Test fonctionnel pour vérifier que les réservations ne sont pas
    possibles pour une compétition passée.

    Args:
        client: Le client de test pour l'application Flask.
    """
    rv = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",  # Assurez-vous que la date est passée dans les données de test
            "club": "Simply Lift",
            "places": "2",
        },
        follow_redirects=True,
    )

    assert rv.status_code == 200

    # Vérifiez que le message flashé est présent dans la réponse
    response_content = rv.data.decode("utf-8")
    assert (
        "Erreur : Vous ne pouvez pas réserver des places pour une compétition passée."
        in response_content
    )
