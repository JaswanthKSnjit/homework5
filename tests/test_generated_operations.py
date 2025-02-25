import pytest
from app.calculator import Calculator

def test_generated_operations():
    """Test basic arithmetic operations using Calculator.compute()."""
    
    # Test addition
    result = Calculator.compute("addition", 3.0, 2.0)
    assert result == 5.0

    # Test subtraction
    result = Calculator.compute("subtraction", 10.0, 4.0)
    assert result == 6.0

    # Test multiplication
    result = Calculator.compute("multiplication", 2.0, 3.0)
    assert result == 6.0

    # Test division
    result = Calculator.compute("division", 8.0, 2.0)
    assert result == 4.0

    # Test division by zero (should raise an error)
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero."):
        Calculator.compute("division", 10.0, 0.0)
