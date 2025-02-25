import pytest
import main
import sys
import subprocess
from app.calculator import Calculator


def test_main_function(monkeypatch):
    """Test that main() runs Calculator.run()."""
    monkeypatch.setattr("builtins.input", lambda _: "exit")  # Simulate "exit" input
    with pytest.raises(SystemExit):  # Expect SystemExit when exiting
        main.main()


def test_main_entry_point():
    """Test if main.py runs as a script and executes main()."""
    # ✅ This runs `python main.py` as an actual subprocess
    result = subprocess.run(["python", "main.py"], input="exit\n", text=True, capture_output=True)

    # ✅ Check that the script ran correctly and exited
    assert "Welcome to the Command Pattern Calculator!" in result.stdout
    assert "Type 'menu' to view options or 'exit' to quit." in result.stdout
    assert "Goodbye!" in result.stdout
    assert result.returncode == 0  # Ensure script exits cleanly
