import click

from app.commands.base_command import Command
from app.utils.click_utils import get_argument
from app.utils.config_utils import load_macros, save_macros
import tempfile
import os
from pathlib import Path


class EditCommand(Command):
    def __init__(self):
        super().__init__(name="edit",
                         help_text="Edit a saved macro by name, uses vim btw",
                         arguments=[get_argument(["name"])])

    def execute(self, name):
        macros = load_macros()
        if name not in macros:
            click.echo(f"No macro found with the name '{name}'")
            return

        click.echo(f"Editing macro '{name}'...")

        # Create a temporary file for editing
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".macro") as temp_file:
            temp_file_path = temp_file.name
            temp_file_path_obj = Path(temp_file_path)
            # Write the macro to the file with comments
            temp_file.write("# Edit the macro commands below.\n")
            temp_file.write("# Lines starting with '#' will be ignored.\n")
            temp_file.writelines(f"{cmd}\n" for cmd in macros[name])
            temp_file.flush()

        original_mtime = temp_file_path_obj.stat().st_mtime

        click.echo(f"Opening macro '{name}' for editing in {"vim"}...")
        os.system(f"{"vim"} {temp_file_path}")

        updated_mtime = temp_file_path_obj.stat().st_mtime

        if updated_mtime == original_mtime:
            click.echo("No changes were saved. Aborting edit.")
            os.unlink(temp_file_path)
            return

        with open(temp_file_path, "r") as temp_file:
            updated_commands = [
                line.strip() for line in temp_file.readlines()
                if line.strip() and not line.startswith("#")
            ]

        os.unlink(temp_file_path)

        macros[name] = updated_commands
        save_macros(macros)
        click.echo(f"Macro '{name}' has been updated.")
