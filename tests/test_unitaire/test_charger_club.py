import pytest
from server import loadClubs, loadCompetitions
from tests.config import client

def test_load_clubs():
    """Test unitaire pour vérifier que les clubs sont bien chargés"""
    clubs = loadClubs()
    assert len(clubs) > 0
    assert isinstance(clubs, list)
    assert 'name' in clubs[0]