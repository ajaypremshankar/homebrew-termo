import click

from app.commands.base_command import Command
from app.utils.config_utils import load_macros


class DescCommand(Command):
    def __init__(self):
        super().__init__(name="desc", help_text="Shows macro definition by name")

    def execute(self, **kwargs):
        name = kwargs.get("name")

        macros = load_macros()
        if name in macros:
            click.echo(click.style(f"Macro '{name}' runs commands in following order:", fg='blue'))
            for index, value in enumerate(macros[name]):
                click.echo(f"{index + 1}: {value}")
        else:
            click.echo(f"No macro with this name was found")
            click.echo(click.style(f"\nNOTE: use `tm ls` command to see all saved macros", fg='blue'))
