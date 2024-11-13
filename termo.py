#!/usr/bin/env python3
import click
import os
import json
from pathlib import Path
import subprocess

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

def save_head(macro_name):
    """Save the current macro name to HEAD file."""
    with open(HEAD_FILE, "w") as file:
        file.write(macro_name)

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

def get_macro_commands_from_history(macro_name):
    """Extract commands between 'tm new <macro_name>' and 'tm save' in the zsh_history file."""
    history_path = Path.home() / ".zsh_history"
    
    if not history_path.exists():
        print("zsh_history file not found.")
        return []

    with open(history_path, "r") as file:
        lines = file.readlines()

    start_index = None
    for i in range(len(lines) - 1, -1, -1):
        if f"tm new {macro_name}" in lines[i]:
            start_index = i
            break

    if start_index is None:
        print(f"No 'new {macro_name}' found in zsh_history.")
        return []

    end_index = None
    for i in range(start_index + 1, len(lines)):
        if "tm save" in lines[i]:
            end_index = i
            break

    if end_index is None:
        print(f"No 'finish' found after 'record start {macro_name}'.")
        return []

    macro_commands = []
    for line in lines[start_index + 1 : end_index]:
        # Each line is in the format ": <timestamp>:<duration>;<command>"
        parts = line.split(";", maxsplit=1)  # Split only on the first `;`
        if len(parts) > 1:
            command = parts[1].strip()
            macro_commands.append(command)

    return macro_commands

@click.group()
def cli():
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

@cli.command("exe")
@click.argument("name")
def run(name):
    """Run a saved macro."""
    run_macro(name)

def run_macro(name):
    macros = load_macros()
    if name not in macros:
        click.echo(f"No macro found with the name '{name}'")
        click.echo(click.style(f"\nNOTE: use `tm search <keyword>` command to search macros", fg='blue'))
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
        macro_content = {name: macros[name]}
        click.echo(json.dumps(macro_content, indent=4))
    else:
        click.echo(f"No macro with this name was found")
        click.echo(click.style(f"\nNOTE: use `tm list` command to see all saved macros", fg='blue'))

@cli.command("ls")
def list():
    """List all the saved marcos."""
    
    macros = load_macros()

    if not macros:
        click.echo(click.style("No macros were found", fg='blue'))
        return

    for key in macros.keys():
        click.echo(f"- {key}")

    click.echo(click.style(f"\nNOTE: use `tm describe <macro name>` command to see more details", fg='blue'))

if __name__ == "__main__":
    cli()
