import click

from app.commands.base_command import Command
from app.utils.config_utils import load_macros


class FindCommand(Command):
    def __init__(self):
        super().__init__(name="find", help_text="Search for a macro by keyword")

    def execute(self, **kwargs):
        keyword = kwargs.get("keyword")
        macros = load_macros()
        results = [macro for macro in macros if keyword.lower() in macro.lower()]
        if results:
            click.echo(f"Macros found containing '{keyword}':")
            for result in results:
                click.echo(f"- {result}")
        else:
            click.echo(f"No macros found containing '{keyword}'.")
