#!/usr/bin/env python3
import click
import os
import json
from pathlib import Path
import subprocess

MACRO_DIR = Path.home() / ".macros"
MACRO_DIR.mkdir(exist_ok=True)
HEAD_FILE = MACRO_DIR / "HEAD"

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

# Load macros from file
def load_macros():
    print(MACRO_FILE)
    if MACRO_FILE.exists():
        with open(MACRO_FILE, "r") as file:
            return json.load(file)
    return {}

# Save macros to file
def save_macros(macros):
    with open(MACRO_FILE, "w") as file:
        json.dump(macros, file)

def get_macro_commands_from_history(macro_name):
    """Extract commands between 'mrec start <macro_name>' and 'mrec finish' in the zsh_history file."""
    history_path = Path.home() / ".zsh_history"
    
    if not history_path.exists():
        print("zsh_history file not found.")
        return []

    # Read the history file and initialize variables
    with open(history_path, "r") as file:
        lines = file.readlines()

    # Find the last 'record start <macro_name>'
    start_index = None
    for i in range(len(lines) - 1, -1, -1):
        if f"mrec start {macro_name}" in lines[i]:
            start_index = i
            break

    if start_index is None:
        print(f"No 'start {macro_name}' found in zsh_history.")
        return []

    # Find the first 'record finish' after the start
    end_index = None
    for i in range(start_index + 1, len(lines)):
        if "mrec finish" in lines[i]:
            end_index = i
            break

    if end_index is None:
        print(f"No 'finish' found after 'record start {macro_name}'.")
        return []

    # Extract and parse commands between start and finish
    macro_commands = []
    for line in lines[start_index + 1 : end_index]:
        # Each line is in the format ": <timestamp>:<duration>;<command>"
        parts = line.split(";", 1)  # Split only on the first `;`
        if len(parts) > 1:
            command = parts[1].strip()
            macro_commands.append(command)

    return macro_commands

@click.group()
def cli():
    pass

@cli.command()
@click.argument("name")
def start(name):
    """Start recording a new macro."""
    if load_head():
        click.echo("Another macro recording is in progress. Please finish or abort it first.")
        return
    
    save_head(name)
    click.echo(f"Recording macro '{name}' started.")


@cli.command()
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


@cli.command()
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

    clear_head()  # Clear the HEAD file

@cli.command()
@click.argument("name")
def run(name):
    """Run a saved macro."""
    macros = load_macros()
    if name not in macros:
        click.echo(f"No macro found with the name '{name}'")
        return
    click.echo(f"Running macro '{name}':")

    for cmd in macros[name]:
        os.system(cmd)


@cli.command()
@click.argument("keyword")
def content(keyword):
    """Search for a macro by keyword."""
    macros = load_macros()
    results = {macro: commands for macro, commands in macros.items() if any(keyword in command for command in commands)}
    if results:
        click.echo(f"Macros found containing '{keyword}':")
        for macro, commands in results.items():
            click.echo(f"- {macro}:")
            for command in commands:
                print(f"  - {command}")
    else:
        click.echo(f"No macros found containing '{keyword}'.")


@cli.command()
@click.argument("name")
def describe(name):
    """Describe a macro by returning its content in JSON format. If name not provided describes all the macros"""
    macros = load_macros()
    if name in macros:
        # Format and print the macro content in JSON format
        macro_content = {name: macros[name]}
        click.echo(json.dumps(macro_content, indent=4))
    else:
        click.echo(json.dumps(macros, indent=4))

if __name__ == "__main__":
    cli()
