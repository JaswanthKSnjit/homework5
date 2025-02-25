import pytest
from app.calculator import Calculator

def test_compute_no_args():
    """Test compute() with no arguments (edge case)."""
    with pytest.raises(TypeError, match="compute\\(\\) missing .* required positional argument.*"):
        Calculator.compute()

def test_addition():
    """Test addition command using plugins."""
    result = Calculator.compute("addition", 3, 2)
    assert result == 5.0

def test_subtraction():
    """Test subtraction command using plugins."""
    result = Calculator.compute("subtraction", 10, 4)
    assert result == 6.0

def test_multiplication():
    """Test multiplication command using plugins."""
    result = Calculator.compute("multiplication", 2, 3)
    assert result == 6.0

def test_division():
    """Test division command using plugins."""
    result = Calculator.compute("division", 8, 2)
    assert result == 4.0

def test_division_by_zero():
    """Test division by zero handling in Calculator.compute()."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero."):
        Calculator.compute("division", 8, 0)

def test_compute_invalid_operation():
    """Test compute() with an invalid operation."""
    with pytest.raises(ValueError, match="Unsupported operation: invalid"):
        Calculator.compute("invalid", 5, 3)

def test_compute_large_numbers():
    """Test compute() with large numbers."""
    result = Calculator.compute("addition", 1e6, 1e6)
    assert result == 2e6

def test_compute_negative_numbers():
    """Test compute() with negative numbers."""
    result = Calculator.compute("subtraction", -10, -5)
    assert result == -5.0

def test_show_menu(capsys):
    """Test that show_menu() correctly prints available commands."""
    Calculator.show_menu()
    captured = capsys.readouterr()
    assert "Available Commands:" in captured.out
    assert "addition" in captured.out
    assert "subtraction" in captured.out
    assert "multiplication" in captured.out
    assert "division" in captured.out
    assert "exit" in captured.out  

def test_run_exit(monkeypatch, capsys):
    """Test if run() exits correctly when 'exit' is entered."""
    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    Calculator.run()
    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out

def test_run_invalid_command(monkeypatch, capsys):
    """Test handling of invalid commands."""
    inputs = iter(["invalid_command", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    Calculator.run()
    captured = capsys.readouterr()
    assert "Invalid command. Type 'menu' to see available commands." in captured.out

# ✅ New test cases for missing coverage ✅

def test_plugin_loading():
    """Test that plugins are loaded correctly into Calculator.COMMANDS."""
    Calculator.load_plugins()
    assert "addition" in Calculator.COMMANDS
    assert "subtraction" in Calculator.COMMANDS
    assert "multiplication" in Calculator.COMMANDS
    assert "division" in Calculator.COMMANDS
    assert "exit" in Calculator.COMMANDS

def test_compute_plugin_missing():
    """Test compute() raises an error for missing operations."""
    with pytest.raises(ValueError, match="Unsupported operation: invalid_op"):
        Calculator.compute("invalid_op", 5, 2)

def test_run_unexpected_error(monkeypatch, capsys):
    """Test handling of unexpected errors in run()."""
    inputs = iter(["invalid_command", "exit"])  # Simulate input with an invalid command
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    Calculator.run()

    captured = capsys.readouterr()
    assert "Invalid command. Type 'menu' to see available commands." in captured.out
