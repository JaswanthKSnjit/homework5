from app.commands.command_base import Command
import sys

class ExitCommand(Command):
    """Command to exit the calculator."""

    def execute(self):
        print("Goodbye!")
        sys.exit(0)  # Properly terminates the program
