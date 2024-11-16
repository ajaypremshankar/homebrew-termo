import click

from app.commands.base_command import Command
from app.utils.config_utils import load_head, clear_head


class CancelCommand(Command):
    def __init__(self):
        super().__init__(name="cancel",
                         help_text="Abort the current recording.")

    def execute(self):
        recording_macro = load_head()
        if not recording_macro:
            click.echo("No macro recording in progress.")
            return

        clear_head()
        click.echo("Macro recording aborted.")
