"""Configuration des tests pour l'application Flask."""

import pytest

from server import app


@pytest.fixture
def client():
    """Fixture de client pour tester les routes de l'application Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
