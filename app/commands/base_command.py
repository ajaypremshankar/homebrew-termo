import click

class Command(click.Command):
    """Base class for CLI commands."""

    def __init__(self, name, help_text, arguments = None):
        self.arguments = arguments or []

        super().__init__(name, 
        callback=self.execute, 
        help=help_text)

        for argument in self.arguments:
            if isinstance(argument, click.Argument):
                self.params.append(argument)
            elif isinstance(argument, click.Option):
                self.params.append(argument)
            else:
                raise ValueError(f"Unsupported parameter type: {type(argument)}")

    def execute(self, *args, **kwargs):
        """Execute the command logic. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the execute method.")
