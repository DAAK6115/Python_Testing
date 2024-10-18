import pytest
from server import app
from tests.config import client

def test_functional_reserve_past_competition(client):
    """Test fonctionnel pour vérifier que les réservations ne sont pas possibles pour une compétition passée"""
    rv = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic',  # Assurez-vous que la date est passée dans les données de test
        'club': 'Simply Lift',
        'places': '2'
    }, follow_redirects=True)

    assert rv.status_code == 200

    # Debug : Afficher le contenu de la réponse pour mieux comprendre
    response_content = rv.data.decode('utf-8')
    print(response_content)

    # Vérifiez que le message flashé est présent dans la réponse
    assert "Erreur : Vous ne pouvez pas réserver des places pour une compétition passée." in response_content