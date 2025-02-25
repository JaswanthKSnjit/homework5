import pytest
from faker import Faker
from decimal import Decimal
from app.calculator import Calculator

fake = Faker()

@pytest.fixture(scope="session", autouse=True)
def load_plugins():
    """Ensure plugins are loaded before running tests."""
    Calculator.load_plugins()

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

def generate_test_data(num_records):
    """Generate test data for arithmetic operations using Calculator.compute()."""
    operations = ["addition", "subtraction", "multiplication", "division"]  # Updated to match plugin names
    test_cases = []

    for _ in range(num_records):
        num1 = Decimal(fake.random_int(min=-100, max=100))
        num2 = Decimal(fake.random_int(min=-100, max=100))
        operation = fake.random_element(elements=operations)

        # Avoid division by zero input
        if operation == "division" and num2 == 0:
            num2 = Decimal(1)

        # Compute expected result using actual production logic
        try:
            result = Calculator.compute(operation, float(num1), float(num2))
            test_cases.append((num1, num2, operation, result))
        except ValueError as e:
            print(f"Skipping test case due to error: {e}")

    return test_cases

def pytest_addoption(parser):
    """Add CLI option to control the number of test records."""
    parser.addoption(
        "--num_records",
        action="store",
        default=10,
        type=int,
        help="Number of test records to generate",
    )

def pytest_generate_tests(metafunc):
    """Dynamically parameterize tests requiring (num1, num2, operation, expected_result)."""
    if {"num1", "num2", "operation", "expected_result"}.issubset(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        test_data = generate_test_data(num_records)
        metafunc.parametrize("num1,num2,operation,expected_result", test_data)
