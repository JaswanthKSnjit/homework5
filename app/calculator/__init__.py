from app.commands.addition import AddCommand
from app.commands.subtraction import SubtractCommand
from app.commands.multiplication import MultiplyCommand
from app.commands.division import DivideCommand
from app.commands.exit import ExitCommand  # Import the ExitCommand

class Calculator:
    """Handles execution of arithmetic operations using modular commands."""

    history = []
    COMMANDS = {
        "add": AddCommand,
        "subtract": SubtractCommand,
        "multiply": MultiplyCommand,
        "divide": DivideCommand,
        "exit": ExitCommand  # Register the ExitCommand
    }

    @staticmethod
    def compute(operation, *args):
        """Executes the given operation using the command pattern."""
        if operation not in Calculator.COMMANDS:
            raise ValueError(f"Unsupported operation: {operation}")
        
        command = Calculator.COMMANDS[operation](*args)
        result = command.execute()
        
        # Ensure whole numbers are formatted without ".0"
        formatted_result = int(result) if result.is_integer() else result
        Calculator.history.append(f"{' '.join(map(str, args))} {operation} = {formatted_result}")
        
        return result

    @staticmethod
    def show_history():
        """Displays calculation history."""
        if not Calculator.history:
            print("No calculations recorded.")
        else:
            print("\nCalculation History:")
            for entry in Calculator.history:
                print(entry)

    @staticmethod
    def clear_history():
        """Clears the history."""
        Calculator.history.clear()
        print("History has been cleared.")

    @staticmethod
    def show_menu():
        """Displays available commands dynamically."""
        print("\nAvailable Commands:")
        for command in Calculator.COMMANDS.keys():
            print(f"- {command} <num1> <num2> (e.g., {command} 5 5)")
        print("- history (View calculation history)")
        print("- clear (Clear calculation history)")
        print("- exit (Exit the calculator)")

    @staticmethod
    def run():
        """Interactive REPL for the calculator."""
        print("Welcome to the Command Pattern Calculator!")
        print("Type 'menu' to view options or 'exit' to quit.")

        while True:
            user_input = input(">>> ").strip().lower()

            if user_input == "exit":
                Calculator.compute("exit")  # Execute exit command
            elif user_input == "menu":
                Calculator.show_menu()
            elif user_input == "history":
                Calculator.show_history()
            elif user_input == "clear":
                Calculator.clear_history()
            else:
                parts = user_input.split()
                if len(parts) >= 2 and parts[0] in Calculator.COMMANDS:
                    try:
                        numbers = list(map(float, parts[1:]))
                        result = Calculator.compute(parts[0], *numbers)
                        print(f"Result: {result}")
                    except ValueError:
                        print("Invalid input. Please enter numeric values.")
                    except ZeroDivisionError as e:
                        print(f"Error: {e}")
                else:
                    print("Invalid command. Type 'menu' to see available commands.")
