from app.commands.command_base import Command

class SubtractCommand(Command):
    """Command to perform subtraction."""

    def __init__(self, *args):
        self.numbers = list(map(float, args))

    def execute(self):
        return self.numbers[0] - sum(self.numbers[1:])
