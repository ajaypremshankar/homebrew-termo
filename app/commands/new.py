import os
import tempfile
from pathlib import Path

import click

from app.commands.base_command import Command
from app.utils.click_utils import get_argument, get_param
from app.utils.config_utils import load_head, save_head, load_macros, save_macros


class NewCommand(Command):
    def __init__(self):
        super().__init__(name="new",
                         help_text="Add/start recording a new macro",
                         arguments=[get_argument(["name"]),
                                    get_param(["--editor", "-e"], True,
                                              "Use editor to create the macro. Uses vim btw")
                                    ])

    def execute(self, name, editor):
        macros = load_macros()

        if name in macros:
            click.echo(f"A macro with the name '{name}' already exists.")
            return

        if load_head():
            click.echo("Another macro recording is in progress. Please finish or abort it first.")
            return

        if editor:
            with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".macro") as temp_file:
                temp_file_path = temp_file.name
                temp_file_path_obj = Path(temp_file_path)

                temp_file.write("# Enter the macro commands below.\n")
                temp_file.write("# Each line represents one command.\n")
                temp_file.write("# Leave the file empty or exit without saving to cancel macro creation.\n\n")
                temp_file.flush()

            original_mtime = temp_file_path_obj.stat().st_mtime

            click.echo(f"Opening editor to create macro '{name}'...")
            os.system(f"{"vim"} {temp_file_path}")

            updated_mtime = temp_file_path_obj.stat().st_mtime

            if updated_mtime == original_mtime:
                click.echo("No changes were saved. Macro creation canceled.")
                os.unlink(temp_file_path)
                return

            with open(temp_file_path, "r") as temp_file:
                commands = [
                    line.strip() for line in temp_file.readlines()
                    if line.strip() and not line.startswith("#")
                ]

            os.unlink(temp_file_path)

            if not commands:
                click.echo("No commands were added. Macro creation canceled.")
                return

            macros[name] = commands
            save_macros(macros)
            click.echo(f"Macro '{name}' saved successfully.")
        else:
            save_head(name)
            click.echo(f"Recording macro '{name}' started.")
