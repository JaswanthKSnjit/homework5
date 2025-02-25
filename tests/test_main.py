import pytest
import main
import subprocess
from app.calculator import Calculator

@pytest.fixture(scope="function", autouse=True)
def disable_multiprocessing(monkeypatch):
    """Replace multiprocessing in compute() with a direct call to avoid pytest hanging."""
    original_compute = Calculator.compute

    def sync_compute(operation, *args):
        """Run compute() synchronously instead of using multiprocessing."""
        if operation not in Calculator.COMMANDS:
            raise ValueError(f"Unsupported operation: {operation}")
        command = Calculator.COMMANDS[operation](*args)
        return command.execute()

    monkeypatch.setattr(Calculator, "compute", sync_compute)

def test_main_function(monkeypatch, capsys):
    """Test that main() runs Calculator.run() without hanging and exits correctly."""
    monkeypatch.setattr("builtins.input", lambda _: "exit")  # Simulate "exit" input

    # Run main() and capture output
    main.main()
    
    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out  # Check if exit message is printed

def test_main_entry_point():
    """Test if main.py runs as a script and executes main()."""
    # Run `python main.py` as an actual subprocess
    result = subprocess.run(["python", "main.py"], input="exit\n", text=True, capture_output=True)

    # Check that the script ran correctly and exited
    assert "Welcome to the Plugin-Based Calculator!" in result.stdout
    assert "Type 'menu' to view options or 'exit' to quit." in result.stdout
    assert "Goodbye!" in result.stdout
    assert result.returncode == 0  # Ensure script exits cleanly
