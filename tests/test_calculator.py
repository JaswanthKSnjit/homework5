import pytest
import sys
from io import StringIO
from app.calculator import Calculator
from app.commands.exit import ExitCommand


@pytest.fixture(autouse=True)
def clear_calculator_history():
    """Ensure calculator history is cleared before each test."""
    Calculator.clear_history()


def test_addition():
    """Test addition operation through Calculator.compute()."""
    assert Calculator.compute("add", 3, 2) == 5


def test_subtraction():
    """Test subtraction operation through Calculator.compute()."""
    assert Calculator.compute("subtract", 10, 4) == 6


def test_multiplication():
    """Test multiplication operation through Calculator.compute()."""
    assert Calculator.compute("multiply", 2, 3) == 6


def test_division():
    """Test division operation through Calculator.compute()."""
    assert Calculator.compute("divide", 8, 2) == 4


def test_division_by_zero():
    """Test division by zero handling in Calculator.compute()."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero."):
        Calculator.compute("divide", 8, 0)


def test_compute_invalid_operation():
    """Test compute() with an invalid operation."""
    with pytest.raises(ValueError, match="Unsupported operation: invalid"):
        Calculator.compute("invalid", 5, 3)


def test_history():
    """Test history functionality records operations correctly."""
    Calculator.compute("add", 3, 2)
    Calculator.compute("multiply", 4, 5)
    
    assert len(Calculator.history) == 2
    assert "3 2 add = 5" in Calculator.history
    assert "4 5 multiply = 20" in Calculator.history


def test_show_history_empty(capsys):
    """Test show_history() when history is empty (Covers lines 40-41)."""
    Calculator.show_history()
    captured = capsys.readouterr()
    assert "No calculations recorded." in captured.out


def test_show_history_with_entries(capsys):
    """Test show_history() when there are calculations recorded (Fix for lines 40-42)."""
    Calculator.compute("add", 3, 2)
    Calculator.compute("subtract", 10, 4)
    Calculator.show_history()

    captured = capsys.readouterr()
    assert "Calculation History:" in captured.out
    assert "3 2 add = 5" in captured.out
    assert "10 4 subtract = 6" in captured.out


def test_clear_history_message(capsys):
    """Test clear_history() displays message."""
    Calculator.compute("add", 3, 2)  # Add history
    Calculator.clear_history()  # Clear history
    captured = capsys.readouterr()
    assert "History has been cleared." in captured.out


def test_clear_history_removes_entries():
    """Test that clear_history() actually removes all history."""
    Calculator.compute("multiply", 5, 5)
    assert len(Calculator.history) == 1  # Ensure history exists

    Calculator.clear_history()
    assert len(Calculator.history) == 0  # Ensure history is cleared


def test_menu_display(capsys):
    """Test that menu is displayed correctly."""
    Calculator.show_menu()
    captured = capsys.readouterr()
    assert "Available Commands:" in captured.out
    assert "- add <num1> <num2>" in captured.out
    assert "- subtract <num1> <num2>" in captured.out
    assert "- multiply <num1> <num2>" in captured.out
    assert "- divide <num1> <num2>" in captured.out
    assert "- history" in captured.out
    assert "- clear" in captured.out
    assert "- exit" in captured.out


def test_exit_command():
    """Test exit command to ensure it raises SystemExit."""
    with pytest.raises(SystemExit) as exit_exception:
        ExitCommand().execute()
    assert exit_exception.value.code == 0  # Ensure exit code is 0 (successful termination)


def test_run_invalid_command(monkeypatch, capsys):
    """Test invalid command handling in the calculator REPL."""
    inputs = iter(["invalid_command", "exit"])  # Simulate invalid command then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):  # Expect exit after 'exit'
        Calculator.run()

    captured = capsys.readouterr()
    assert "Invalid command. Type 'menu' to see available commands." in captured.out


def test_run_valid_addition(monkeypatch, capsys):
    """Test valid addition in the REPL mode."""
    inputs = iter(["add 5 3", "exit"])  # Simulate adding numbers then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):  # Expect exit after 'exit'
        Calculator.run()

    captured = capsys.readouterr()
    assert "Result: 8" in captured.out


def test_run_clear_history(monkeypatch, capsys):
    """Test clearing history from the REPL."""
    inputs = iter(["clear", "exit"])  # Simulate clearing history then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):  # Expect exit after 'exit'
        Calculator.run()

    captured = capsys.readouterr()
    assert "History has been cleared." in captured.out


def test_run_history_when_empty(monkeypatch, capsys):
    """Test history when there are no previous calculations."""
    inputs = iter(["history", "exit"])  # Simulate viewing history then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):  # Expect exit after 'exit'
        Calculator.run()

    captured = capsys.readouterr()
    assert "No calculations recorded." in captured.out


def test_run_history_with_entries(monkeypatch, capsys):
    """Test history in REPL mode after performing calculations."""
    inputs = iter(["add 2 2", "subtract 5 3", "history", "exit"])  # Perform operations, then view history
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):  # Expect exit after 'exit'
        Calculator.run()

    captured = capsys.readouterr()

    # Ensure history entries exist
    assert "Calculation History:" in captured.out
    assert "2.0 2.0 add = 4" in captured.out
    assert "5.0 3.0 subtract = 2" in captured.out



def test_run_menu_display(monkeypatch, capsys):
    """Test menu command in REPL mode."""
    inputs = iter(["menu", "exit"])  # Simulate displaying menu then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):  # Expect exit after 'exit'
        Calculator.run()

    captured = capsys.readouterr()
    assert "Available Commands:" in captured.out


def test_run_invalid_number_input(monkeypatch, capsys):
    """Test non-numeric input handling."""
    inputs = iter(["add abc def", "exit"])  # Simulate entering invalid numbers then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):  # Expect exit after 'exit'
        Calculator.run()

    captured = capsys.readouterr()
    assert "Invalid input. Please enter numeric values." in captured.out


def test_run_division_by_zero(monkeypatch, capsys):
    """Test division by zero handling in REPL mode."""
    inputs = iter(["divide 10 0", "exit"])  # Simulate division by zero then exit
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):  # Expect exit after 'exit'
        Calculator.run()

    captured = capsys.readouterr()
    assert "Error: Cannot divide by zero." in captured.out
