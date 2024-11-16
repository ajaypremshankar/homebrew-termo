class Command:
    """Base class for CLI commands."""

    def __init__(self, name, help_text):
        self.name = name
        self.help_text = help_text

    def register(self, cli_group, argument=None):
        """Register the command with the CLI group."""

        @cli_group.command(name=self.name, help=self.help_text)
        def command_handler(**kwargs):
            self.execute(**kwargs)

        if argument:
            argument(command_handler)

    def execute(self, **kwargs):
        """Execute the command logic. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the execute method.")
