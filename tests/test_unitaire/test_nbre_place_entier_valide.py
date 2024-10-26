"""Test unitaire pour la validation du nombre de places.

Ce module contient un test qui vérifie que la fonction `validate_places` accepte un entier valide.
"""

import pytest

from server import validate_places


def test_validate_places_success():
    """Test unitaire pour vérifier que la validation des places passe avec un
    entier valide.

    Assure que la fonction `validate_places` ne lève aucune erreur lorsqu'un entier positif est fourni.
    """
    try:
        validate_places(5)  # Aucune exception ne devrait être levée
    except ValueError:
        pytest.fail("validate_places a levé une erreur avec un entier positif.")
