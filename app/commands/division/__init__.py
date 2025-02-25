from app.commands.command_base import Command

class DivideCommand(Command):
    """Command to perform division."""

    def __init__(self, *args):
        self.numbers = list(map(float, args))
        if 0 in self.numbers[1:]:
            raise ZeroDivisionError("Cannot divide by zero.")

    def execute(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            result /= num
        return result
