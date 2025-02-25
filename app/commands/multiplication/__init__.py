from app.commands.command_base import Command

class MultiplyCommand(Command):
    """Command to perform multiplication."""

    def __init__(self, *args):
        self.numbers = list(map(float, args))

    def execute(self):
        result = 1
        for num in self.numbers:
            result *= num
        return result
