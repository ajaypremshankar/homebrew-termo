import click

from app.commands.base_command import Command
from app.utils.click_utils import get_argument
from app.utils.config_utils import load_macros, save_macros


class DelCommand(Command):
    def __init__(self):
        super().__init__(name="del",
                         help_text="Delete a saved macro by name.",
                         arguments=[get_argument(["name"])])

    def execute(self, name):
        macros = load_macros()
        if name not in macros:
            click.echo(f"No macro found with the name '{name}'")
            return

        # Confirm deletion
        confirmation = input(f"Are you sure you want to delete the macro '{name}'? (y/n): ").strip().lower()
        if confirmation == "y":
            del macros[name]
            save_macros(macros)
            click.echo(f"Macro '{name}' has been deleted.")
        else:
            click.echo(f"Macro '{name}' was not deleted.")
