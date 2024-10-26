"""Test d'intégration de la route /purchasePlaces.

Ce module vérifie le comportement lorsque les points du club sont
insuffisants. Il s'assure qu'une tentative de réservation avec des
points insuffisants est refusée.
"""

import pytest


def test_purchase_places_not_enough_points(client):
    """Test d'intégration de la route /purchasePlaces avec des points
    insuffisants.

    Args:
        client: Le client de test pour l'application Flask.
    """
    rv = client.post(
        "/purchasePlaces",
        data={
            "competition": "Fall Classic",  # Assurez-vous que cette compétition n'est pas passée
            "club": "Simply Lift",
            "places": "100",  # Un nombre supérieur aux points du club
        },
        follow_redirects=True,
    )

    assert rv.status_code == 200
    response_content = rv.data.decode("utf-8")
    print(response_content)  # Pour vérifier la réponse complète si besoin

    # Vérifiez si une partie du message d'erreur est présente
    assert "pas assez de points" in response_content
