"""Test unitaire pour le chargement des compétitions.

Ce module contient des tests qui vérifient le chargement correct des
compétitions depuis la base de données.
"""

import pytest

from server import loadClubs, loadCompetitions
from tests.conftest import client


def test_load_competitions():
    """Test unitaire pour vérifier que les compétitions sont bien chargées."""
    competitions = loadCompetitions()
    assert len(competitions) > 0
    assert isinstance(competitions, list)
    assert "name" in competitions[0]
