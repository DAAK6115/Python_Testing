"""Test unitaire pour la validation des points disponibles.

Ce module contient un test qui vérifie que la fonction de calcul des
points restants fonctionne correctement.
"""

import pytest

from server import calcul_points


def test_calcul_points():
    """Vérifie le calcul des points restants après une réservation."""
    points_avant = 30
    places_reservees = 5
    points_par_place = 3
    points_restants = calcul_points(points_avant, places_reservees, points_par_place)
    assert points_restants == 15
