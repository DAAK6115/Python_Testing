"""Test d'intégration pour la connexion et la visualisation des points.

Ce module contient un test pour vérifier que l'utilisateur peut se
connecter et consulter ses points de fidélité.
"""

import pytest


def test_integration_login_and_points_view(client):
    """Vérifie la connexion et la visualisation des points."""
    rv = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}, follow_redirects=True
    )
    assert rv.status_code == 200

    # Affiche la réponse pour vérifier le contenu en cas d'erreur
    response_content = rv.data.decode("utf-8")
    print(response_content)  # Pour voir tout le HTML rendu

    # Assurez-vous que le texte "points" est présent, peu importe la forme
    assert (
        "points" in response_content.lower()
    )  # Recherche générique pour vérifier la présence du mot "points"
