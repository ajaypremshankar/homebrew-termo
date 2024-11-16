import click

from app.commands.base_command import Command
from app.utils.config_utils import (load_head,
                                    get_macro_commands_from_history,
                                    load_macros,
                                    save_macros,
                                    clear_head)


class SaveCommand(Command):
    def __init__(self):
        super().__init__(name="save", help_text="Finish the current recording and save the macro")

    def execute(self, **kwargs):
        recording_macro = load_head()
        if not recording_macro:
            click.echo("No macro recording in progress.")
            return

        commands = get_macro_commands_from_history(recording_macro)
        if commands:
            macro_commands = [line.strip() for line in commands]
            macros = load_macros()
            macros[recording_macro] = macro_commands
            save_macros(macros)
            click.echo(f"Macro '{recording_macro}' saved.")
        else:
            click.echo("No commands were recorded.")

        clear_head()
