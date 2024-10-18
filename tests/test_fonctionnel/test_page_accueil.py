import pytest
from server import app
from tests.config import client

def test_home_page(client):
    """Test que la page d'accueil se charge correctement"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert "Welcome to the GUDLFT Registration Portal" in rv.data.decode('utf-8')




