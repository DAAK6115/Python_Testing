"""Test unitaire pour le chargement des clubs.

Ce module contient des tests qui vérifient que les clubs sont
correctement chargées depuis le fichier JSON.
"""

import pytest

from server import loadClubs, loadCompetitions


def test_load_clubs():
    """Test unitaire pour vérifier que les clubs sont bien chargés."""
    clubs = loadClubs()
    assert len(clubs) > 0
    assert isinstance(clubs, list)
    assert "name" in clubs[0]
