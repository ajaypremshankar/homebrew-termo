#!/usr/bin/env python3
import click
import os
import json
from pathlib import Path
import subprocess
import warnings
from difflib import unified_diff

MACRO_DIR = Path.home() / ".termo"
MACRO_DIR.mkdir(exist_ok=True)
HEAD_FILE = MACRO_DIR / "HEAD"
CONFIG_FILE = MACRO_DIR / "config.json"

# ANSI escape codes for colors
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_CYAN = "\033[36m"
COLOR_RESET = "\033[0m"


def print_diff(diff):
    if diff:
        click.echo("Showing changes:")
        for index, line in enumerate(diff, 1):
            if line.startswith("---") or line.startswith("+++"):
                # File headers
                click.echo(f"{COLOR_CYAN}{line}{COLOR_RESET}")
            elif line.startswith("-"):
                # Removed lines
                click.echo(f"{COLOR_RED}{line}{COLOR_RESET}")
            elif line.startswith("+"):
                # Added lines
                click.echo(f"{COLOR_GREEN}{line}{COLOR_RESET}")
            else:
                # Context lines
                click.echo(line)
    else:
        click.echo("No changes made.")


class DefaultGroup(click.Group):
    """Invokes a subcommand marked with `default=True` if any subcommand not
    chosen.

    :param default_if_no_args: resolves to the default command if no arguments
                               passed.

    """

    def __init__(self, *args, **kwargs):
        # To resolve as the default command.
        if not kwargs.get('ignore_unknown_options', True):
            raise ValueError('Default group accepts unknown options')
        self.ignore_unknown_options = True
        self.default_cmd_name = kwargs.pop('default', None)
        self.default_if_no_args = kwargs.pop('default_if_no_args', False)
        super(DefaultGroup, self).__init__(*args, **kwargs)

    def set_default_command(self, command):
        """Sets a command function as the default command."""
        cmd_name = command.name
        self.add_command(command)
        self.default_cmd_name = cmd_name

    def parse_args(self, ctx, args):
        
        if not args and self.default_if_no_args:
            args.insert(0, self.default_cmd_name)
        return super(DefaultGroup, self).parse_args(ctx, args)

    def get_command(self, ctx, cmd_name):
        
        if cmd_name not in self.commands:
            # No command name matched.
            ctx.arg0 = cmd_name
            cmd_name = self.default_cmd_name
        return super(DefaultGroup, self).get_command(ctx, cmd_name)

    def resolve_command(self, ctx, args):
        base = super(DefaultGroup, self)
        cmd_name, cmd, args = base.resolve_command(ctx, args)

        if hasattr(ctx, 'arg0'):
            print(f"{ctx.arg0}")
            args.insert(0, ctx.arg0)
            cmd_name = cmd.name
        return cmd_name, cmd, args

    def format_commands(self, ctx, formatter):
        formatter = DefaultCommandFormatter(self, formatter, mark='*')
        return super(DefaultGroup, self).format_commands(ctx, formatter)

    def command(self, *args, **kwargs):
        default = kwargs.pop('default', False)
        decorator = super(DefaultGroup, self).command(*args, **kwargs)
        if not default:
            return decorator
        warnings.warn('Use default param of DefaultGroup or '
                      'set_default_command() instead', DeprecationWarning)

        def _decorator(f):
            cmd = decorator(f)
            self.set_default_command(cmd)
            return cmd

        return _decorator


class DefaultCommandFormatter(object):
    """Wraps a formatter to mark a default command."""

    def __init__(self, group, formatter, mark='*'):
        self.group = group
        self.formatter = formatter
        self.mark = mark

    def __getattr__(self, attr):
        return getattr(self.formatter, attr)

    def write_dl(self, rows, *args, **kwargs):
        rows_ = []
        for cmd_name, help in rows:
            if cmd_name == self.group.default_cmd_name:
                rows_.insert(0, (cmd_name + self.mark, help))
            else:
                rows_.append((cmd_name, help))
        return self.formatter.write_dl(rows_, *args, **kwargs)


def is_first_run():
    """Check if this is the first run by looking for a config file."""
    if not CONFIG_FILE.exists():
        # If the config file doesn't exist, assume it's the first run
        return True
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
    return config.get("first_run", True)

def complete_first_run():
    """Mark the first run as complete by updating the config file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump({"first_run": False}, file)

def display_setup_guide():
    """Display a welcome message and setup guide for first-time users."""
    click.echo(click.style("\nWelcome to Termo!", fg="green", bold=True))
    click.echo("This quick guide will help you get started with Termo:\n")
    click.echo("Key Commands:")
    click.echo("  - tm new <name>    : Start recording a new macro")
    click.echo("  - tm save          : Save the current macro recording")
    click.echo("  - tm <name>        : Run a saved macro by name")
    click.echo("  - tm ls            : List all macros")
    click.echo("  - tm desc <name>   : Describe a macro in detail\n")
    click.echo(click.style("Happy automating with Termo!\n", fg="green", bold=True))


def load_head():
    """Load the current macro name from HEAD file."""
    if HEAD_FILE.exists():
        with open(HEAD_FILE, "r") as file:
            return file.read().strip()
    return None

def save_head(name):
    """Save the current macro name to HEAD file."""
    with open(HEAD_FILE, "w") as file:
        file.write(name)

def clear_head():
    """Clear the HEAD file when recording ends or is aborted."""
    if HEAD_FILE.exists():
        HEAD_FILE.unlink()

# Set up a storage file for macros
MACRO_FILE = MACRO_DIR / ".macros.json"

def load_macros():
    if MACRO_FILE.exists():
        with open(MACRO_FILE, "r") as file:
            return json.load(file)
    return {}

def save_macros(macros):
    with open(MACRO_FILE, "w") as file:
        json.dump(macros, file)

def get_macro_commands_from_history(name):
    """Extract commands between 'tm new <name>' and 'tm save' in the zsh_history file."""
    history_path = Path.home() / ".zsh_history"
    
    if not history_path.exists():
        print("zsh_history file not found.")
        return []

    with open(history_path, "r") as file:
        lines = file.readlines()

    start_index = None
    for i in range(len(lines) - 1, -1, -1):
        if f"tm new {name}" in lines[i]:
            start_index = i
            break

    if start_index is None:
        print(f"No 'new {name}' found in zsh_history.")
        return []

    end_index = None
    for i in range(start_index + 1, len(lines)):
        if "tm save" in lines[i]:
            end_index = i
            break

    if end_index is None:
        print(f"No 'finish' found after 'record start {name}'.")
        return []

    macro_commands = []
    for line in lines[start_index + 1 : end_index]:
        # Each line is in the format ": <timestamp>:<duration>;<command>"
        parts = line.split(";", maxsplit=1)  # Split only on the first `;`
        if len(parts) > 1:
            command = parts[1].strip()
            macro_commands.append(command)

    return macro_commands

@click.group(cls=DefaultGroup, default_if_no_args=False)
def cli():
    """Pass command to run or just macro name to 'exec' given macro."""
    if is_first_run():
        display_setup_guide()
        complete_first_run()  
    pass
    

@cli.command("new")
@click.argument("name")
def start(name):
    """Start recording a new macro."""
    if load_head():
        click.echo("Another macro recording is in progress. Please finish or abort it first.")
        return
    
    save_head(name)
    click.echo(f"Recording macro '{name}' started.")


@cli.command("cancel")
def abort():
    """Abort the current recording."""
    recording_macro = load_head()
    if not recording_macro:
        click.echo("No macro recording in progress.")
        return

    macro_log_path = MACRO_DIR / f"{recording_macro}.log"
    if macro_log_path.exists():
        macro_log_path.unlink()  # Remove the log file
    clear_head()  # Clear the HEAD file
    click.echo("Macro recording aborted.")


@cli.command("save")
def finish():
    """Finish the current recording and save the macro."""
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

@cli.command("exec", default=True)
@click.argument("name")
def run(name):
    """Run a saved macro."""
    run_macro(name)

def run_macro(name):
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

@cli.command("find")
@click.argument("keyword")
def search(keyword):
    """Search for a macro by keyword."""
    macros = load_macros()
    results = [macro for macro in macros if keyword.lower() in macro.lower()]
    if results:
        click.echo(f"Macros found containing '{keyword}':")
        for result in results:
            click.echo(f"- {result}")
    else:
        click.echo(f"No macros found containing '{keyword}'.")


@cli.command("desc")
@click.argument("name")
def describe(name):
    """Describe a macro by returning its content in JSON format."""

    macros = load_macros()
    if name in macros:
        click.echo(click.style(f"Macro '{name}' runs commands in following order:", fg='blue'))
        for index, value in enumerate(macros[name]):
            click.echo(f"{index + 1}: {value}")
    else:
        click.echo(f"No macro with this name was found")
        click.echo(click.style(f"\nNOTE: use `tm ls` command to see all saved macros", fg='blue'))

@cli.command("ls")
def list_command():
    """List all the saved marcos."""
    
    macros = load_macros()

    if not macros:
        click.echo(click.style("No macros were found", fg='blue'))
        return

    for key in macros.keys():
        click.echo(f"- {key}")

    click.echo(click.style(f"\nNOTE: use `tm desc <macro name>` command to see more details", fg='blue'))

@cli.command("del")
@click.argument("name")
def delete_macro(name):
    """Delete a saved macro by name."""
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


@cli.command("edit")
@click.argument("name")
def edit_macro(name):
    """Edit a saved macro by name."""
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
            macros_copy_for_edit.append(new_command)
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
        else:
            click.echo("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    cli()
