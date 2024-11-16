import json
from pathlib import Path

import click

MACRO_DIR = Path.home() / ".termo"
MACRO_DIR.mkdir(exist_ok=True)
HEAD_FILE = MACRO_DIR / "HEAD"
CONFIG_FILE = MACRO_DIR / "config.json"


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
    for line in lines[start_index + 1: end_index]:
        # Each line is in the format ": <timestamp>:<duration>;<command>"
        parts = line.split(";", maxsplit=1)  # Split only on the first `;`
        if len(parts) > 1:
            command = parts[1].strip()
            macro_commands.append(command)

    return macro_commands
