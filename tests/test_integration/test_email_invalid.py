import pytest
from server import competitions, clubs
from tests.config import client

def test_invalid_email(client):
    """Test qu'un email invalide affiche un message d'erreur et renvoie à la page d'accueil"""
    rv = client.post('/showSummary', data=dict(email="invalid@example.com"), follow_redirects=True)

    # Vérifier que le statut est 200 (la page d'accueil est affichée après redirection)
    assert rv.status_code == 200

    # Vérifier que le message d'erreur flashé est présent dans la réponse
    assert "Email invalide, veuillez réessayer." in rv.data.decode('utf-8')  # Conversion de rv.data en chaîne UTF-8