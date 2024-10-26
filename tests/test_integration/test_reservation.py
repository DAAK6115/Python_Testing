"""Test d'intégration pour la vérification du processus de réservation.

Ce module contient un test pour vérifier que l'interaction entre
l'affichage des compétitions et la réservation de places fonctionne
correctement.
"""

import pytest
from bs4 import BeautifulSoup


def test_integration_reservation_workflow(client):
    """Vérifie le workflow de réservation d'une place."""
    competition_name = "Fall Classic"  # Utilisez le nom d'une compétition existante
    club_name = "Simply Lift"  # Utilisez le nom d'un club existant

    # Créez l'URL à partir du nom de la compétition et du club
    url = f"/book/{competition_name}/{club_name}"
    rv = client.get(url)

    # Vérifiez si le code de statut est 200 et la page est rendue correctement
    assert rv.status_code == 200

    # Analysez le contenu HTML
    soup = BeautifulSoup(rv.data, "html.parser")

    # Vérifiez si le titre de la compétition est présent
    assert soup.find("h2", string=competition_name) is not None

    # Vérifiez si le texte "Places available" est présent
    assert (
        soup.find("div", class_="info", string=lambda t: "Places available" in t)
        is not None
    )

    # Vérifiez si le bouton "Réserver" est présent
    assert soup.find("button", string="Réserver") is not None
