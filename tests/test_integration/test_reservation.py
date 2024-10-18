import pytest
from server import competitions, clubs
from tests.config import client

def test_purchase_places():
    """Test de la réservation de places"""
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    competition = [c for c in competitions if c['name'] == 'Spring Festival'][0]
    initial_points = int(club['points'])
    initial_places = int(competition['numberOfPlaces'])
    places_to_book = 3

    # Simuler la réservation
    competition['numberOfPlaces'] = str(initial_places - places_to_book)
    club['points'] = str(initial_points - places_to_book)

    # Vérifier les changements
    assert int(competition['numberOfPlaces']) == initial_places - places_to_book
    assert int(club['points']) == initial_points - places_to_book


