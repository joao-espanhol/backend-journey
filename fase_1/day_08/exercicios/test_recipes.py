import pytest
from brewery.recipes import calculate_abv

def test_typical_batch():
    # Arrange / Act
    result = calculate_abv(1.050, 1.010)
    # Assert
    assert result == pytest.approx(5.25)   # approx: float comparison tolerance

def test_zero_fermentation_gives_zero_abv():
    assert calculate_abv(1.050, 1.050) == 0.0

def test_invalid_gravity_raises():
    with pytest.raises(ValueError):
        calculate_abv(1.010, 1.050)

def test_negative_gravity():
    with pytest.raises(ValueError):
        calculate_abv(1.050, -1.000)