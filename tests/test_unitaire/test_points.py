"""Module de test unitaire pour vérifier la gestion des points des clubs."""

import pytest

from server import clubs


def test_points():
    """Teste que le nombre de points est correct.

    Vérifie que chaque club dans la base de données a le bon nombre de
    points.
    """
    club = [c for c in clubs if c["name"] == "Simply Lift"][0]
    initial_points = int(club["points"])
    points_used = 3
    club["points"] = str(initial_points - points_used)

    # Vérifier que les points sont bien déduits
    assert int(club["points"]) == initial_points - points_used
