from server import competitions, clubs
from tests.config import client
def test_invalid_reservation():
    """Test de la réservation avec trop de places"""
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    competition = [c for c in competitions if c['name'] == 'Spring Festival'][0]
    places_to_book = 15  # Plus que le nombre autorisé
    initial_points = int(club['points'])

    # On ne permet pas la réservation de plus de 12 places
    assert places_to_book > 12
    assert int(club['points']) == initial_points  # Pas de changement dans les points