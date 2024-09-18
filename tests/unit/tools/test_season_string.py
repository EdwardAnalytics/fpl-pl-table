import pytest
from src.tools.season_string import (
    get_season_string,
)


def test_get_season_string():
    # Test valid inputs
    assert get_season_string(2023) == "2023-24"
    assert get_season_string(1999) == "1999-00"
    assert get_season_string(2000) == "2000-01"
    assert get_season_string(2010) == "2010-11"

    # Test invalid inputs
    with pytest.raises(ValueError):
        get_season_string(23)  # Not a four-digit integer
    with pytest.raises(ValueError):
        get_season_string(202)  # Not a four-digit integer
    with pytest.raises(ValueError):
        get_season_string(20234)  # Not a four-digit integer
    with pytest.raises(ValueError):
        get_season_string("2023")  # Not an integer
