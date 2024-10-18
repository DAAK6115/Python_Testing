import pytest
from tests.config import client

def test_purchase_places_not_enough_points(client):
    """Test d'intégration de la route /purchasePlaces avec des points insuffisants"""
    rv = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '100'
    }, follow_redirects=True)

    assert rv.status_code == 200
    assert "Erreur : Vous n&#39;avez pas assez de points pour réserver autant de places." in rv.data.decode('utf-8')
