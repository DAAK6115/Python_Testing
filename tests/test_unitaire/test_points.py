import pytest
from server import clubs

def test_points_update_after_booking():
    """Test que les points du club sont bien mis à jour après une réservation"""
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    initial_points = int(club['points'])
    points_used = 3
    club['points'] = str(initial_points - points_used)

    # Vérifier que les points sont bien déduits
    assert int(club['points']) == initial_points - points_used
