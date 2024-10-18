import pytest
from server import validate_places

def test_validate_places_success():
    """Test unitaire pour vérifier que la validation des places passe avec un entier valide"""
    try:
        validate_places(5)  # Aucun exception ne devrait être levée
    except ValueError:
        pytest.fail("validate_places a levé une erreur avec un entier positif.")