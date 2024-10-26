"""Test unitaire pour la validation du nombre de places comme entier.

Ce module contient un test qui vérifie que la fonction `validate_places` lève une erreur
lorsque le nombre de places n'est pas un entier valide.
"""

import pytest

from server import validate_places


def test_validate_places_as_integer():
    """Test unitaire pour vérifier que le nombre de places est un entier.

    Vérifie que la fonction `validate_places` lève une erreur lorsque le nombre de places n'est pas un entier.
    """
    with pytest.raises(ValueError, match="Le nombre de places doit être un entier."):
        validate_places("invalid")
