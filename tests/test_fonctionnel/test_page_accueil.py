"""Ce module contient un test fonctionnel pour vérifier que la page d'accueil
de l'application se charge correctement.

Il s'assure que la page d'accueil renvoie le bon statut HTTP et contient
le texte approprié.
"""

import pytest

from server import app


def test_home_page(client):
    """Test que la page d'accueil se charge correctement."""
    rv = client.get("/")
    assert rv.status_code == 200
    assert "Welcome to the GUDLFT Registration Portal" in rv.data.decode("utf-8")
