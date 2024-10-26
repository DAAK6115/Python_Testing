"""Test unitaire pour valider les dates des compétitions.

Ce module contient un test qui vérifie que la validation de la date de
compétition ne permet pas de réserver pour une date passée.
"""

from datetime import datetime, timedelta

import pytest

from server import validate_competition_date


def test_validate_competition_date():
    """Vérifie que la validation lève une erreur pour une date passée."""
    date_passee = datetime.now() - timedelta(days=1)
    with pytest.raises(ValueError, match="La compétition est déjà passée."):
        validate_competition_date(date_passee)
