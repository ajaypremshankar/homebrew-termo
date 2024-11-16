import click

from app.commands.base_command import Command
from app.utils.config_utils import load_head, save_head


class NewCommand(Command):
    def __init__(self):
        super().__init__(name="new", help_text="Start recording a new macro")

    def execute(self, **kwargs):
        name = kwargs.get("name")

        if load_head():
            click.echo("Another macro recording is in progress. Please finish or abort it first.")
            return

        save_head(name)
        click.echo(f"Recording macro '{name}' started.")
