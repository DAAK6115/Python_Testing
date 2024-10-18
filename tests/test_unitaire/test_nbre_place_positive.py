import pytest
from server import validate_places

def test_validate_positive_places():
    """Test unitaire pour vérifier que le nombre de places est supérieur à zéro"""
    with pytest.raises(ValueError, match="Le nombre de places doit être supérieur à zéro."):
        validate_places(0)