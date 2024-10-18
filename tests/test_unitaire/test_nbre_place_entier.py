import pytest
from server import validate_places

def test_validate_places_as_integer():
    """Test unitaire pour vérifier que le nombre de places est un entier"""
    with pytest.raises(ValueError, match="Le nombre de places doit être un entier."):
        validate_places("invalid")