import pytest
from tests.config import client  # Import explicite depuis config.py

def test_show_summary(client):
    """Test que la route showSummary fonctionne avec un email valide"""
    rv = client.post('/showSummary', data=dict(email="john@simplylift.co"))
    assert rv.status_code == 200
    assert "Welcome, Simply Lift" in rv.data.decode('utf-8')
