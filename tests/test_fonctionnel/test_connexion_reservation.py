import pytest
from server import app
from tests.config import client

def test_functional_login_and_reserve(client):
    """Test fonctionnel pour vérifier la connexion et la réservation de places"""
    # Connexion
    rv = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert rv.status_code == 200
    assert b"Welcome, Simply Lift" in rv.data

    # Réservation de places
    rv = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    })
    assert rv.status_code == 200
    assert "Réservation complète !" in rv.data.decode('utf-8')
