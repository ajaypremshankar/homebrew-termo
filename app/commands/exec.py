import os

import click

from app.commands.base_command import Command
from app.utils.config_utils import load_macros


class ExecCommand(Command):
    def __init__(self):
        super().__init__(name="exec", help_text="Execute a saved macro")

    def execute(self, **kwargs):
        name = kwargs.get("name")

        macros = load_macros()
        if name not in macros:
            click.echo(f"No macro found with the name '{name}'")
            click.echo(click.style(f"\nNOTE: use `tm find <keyword>` command to search macros", fg='blue'))
            return

        click.echo(click.style(f"Executing macro '{name}':\n", bold=True))
        for cmd in macros[name]:
            click.echo(click.style(f"→ {cmd}", fg='green'))
            os.system(cmd)
            click.echo("")
