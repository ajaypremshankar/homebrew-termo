from difflib import unified_diff

import click

from app.commands.base_command import Command
from app.utils.click_utils import get_argument
from app.utils.config_utils import load_macros, save_macros
from app.utils.diff_utils import print_diff


class EditCommand(Command):
    def __init__(self):
        super().__init__(name="edit",
                         help_text="Edit a saved macro by name",
                         arguments=get_argument("name"))

    def execute(self, name):
        macros = load_macros()
        if name not in macros:
            click.echo(f"No macro found with the name '{name}'")
            return

        click.echo(f"Editing macro '{name}'...")

        macro_copy_for_edit = macros[name].copy()

        click.echo("Current commands:")
        for idx, command in enumerate(macros[name], start=1):
            click.echo(f"{idx}. {command}")

        while True:

            click.echo("\nOptions:")
            click.echo("  1. Add a new command")
            click.echo("  2. Remove a command by index")
            click.echo("  3. Replace a command by index")
            click.echo("  4. Save")
            click.echo("  5. Abort\n")

            diff = list(unified_diff(
                macros[name],
                macro_copy_for_edit,
                fromfile="original",
                tofile="edited",
                lineterm=""
            ))

            print_diff(diff)

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                # Add a new command
                new_command = input("Enter the new command: ").strip()
                macro_copy_for_edit.append(new_command)
                click.echo(f"Command added: {new_command}")

            elif choice == "2":
                # Remove a command by index
                try:
                    index = int(input("Enter the index of the command to remove: ")) - 1
                    if 0 <= index < len(macro_copy_for_edit):
                        removed_command = macro_copy_for_edit.pop(index)
                        click.echo(f"Command removed: {removed_command}")
                    else:
                        click.echo("Invalid index.")
                except ValueError:
                    click.echo("Please enter a valid number.")

            elif choice == "3":
                # Replace a command by index
                try:
                    index = int(input("Enter the index of the command to replace: ")) - 1
                    if 0 <= index < len(macro_copy_for_edit):
                        new_command = input("Enter the new command: ").strip()
                        old_command = macro_copy_for_edit[index]
                        macro_copy_for_edit[index] = new_command
                        click.echo(f"Command replaced: '{old_command}' → '{new_command}'")
                    else:
                        click.echo("Invalid index.")
                except ValueError:
                    click.echo("Please enter a valid number.")

            elif choice == "4":
                macros[name] = macro_copy_for_edit
                save_macros(macros)
                click.echo(f"Changes to macro '{name}' have been saved.")
                click.echo(f"Exiting edit mode for macro '{name}'.")
                break
            elif choice == "5":
                click.echo(f"Aborting edit for macro '{name}'.")
                break
            else:
                click.echo("Invalid choice. Please enter a number between 1 and 4.")
