"""Test unitaire pour le chargement des compétitions.

Ce module contient des tests qui vérifient que les compétitions sont
correctement chargées depuis le fichier JSON.
"""

import pytest

from server import loadClubs, loadCompetitions


def test_load_competitions():
    """Test unitaire pour vérifier que les compétitions sont bien chargées."""
    competitions = loadCompetitions()
    assert len(competitions) > 0
    assert isinstance(competitions, list)
    assert "name" in competitions[0]
