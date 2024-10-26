"""Ce module contient des tests unitaires pour valider la fonctionnalité liée
au nombre de places dans le système."""

import pytest

from server import validate_places


def test_validate_positive_places():
    """Test unitaire pour vérifier que le nombre de places est supérieur à
    zéro.

    Vérifie que la fonction `validate_places` lève une erreur si le nombre de places est égal à zéro.
    """
    with pytest.raises(
        ValueError, match="Le nombre de places doit être supérieur à zéro."
    ):
        validate_places(0)
