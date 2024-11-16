import click

from app.commands.base_command import Command
from app.utils.config_utils import load_macros


class ListCommand(Command):
    def __init__(self):
        super().__init__(name="ls",
                         help_text="Lists available macros")

    def execute(self):
        macros = load_macros()

        if not macros:
            click.echo(click.style("No macros were found", fg='blue'))
            return

        for key in macros.keys():
            click.echo(f"- {key}")

        click.echo(click.style(f"\nNOTE: use `tm desc <macro name>` command to see more details", fg='blue'))
