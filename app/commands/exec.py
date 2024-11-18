import os
import platform
import re
import subprocess

import click

from app.commands.base_command import Command
from app.utils.click_utils import get_argument, get_param
from app.utils.config_utils import load_macros


def _run_as_admin(cmd):
    """Run a command with administrative privileges."""
    system = platform.system()

    try:
        if system in ["Darwin"]:
            # Use 'sudo' on Linux/macOS
            click.echo(click.style(f"Running as admin: {cmd}", fg="yellow"))
            subprocess.run(["sudo", "sh", "-c", cmd], check=True)
        else:
            click.echo(click.style("Unsupported platform for admin execution.", fg="red"))
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error: Command failed with error: {e}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"Error: Unable to elevate privileges: {e}", fg="red"))


class ExecCommand(Command):
    def __init__(self):
        super().__init__(name="exec",
                         help_text="Execute a saved macro, can take positional params for commands",
                         arguments=[get_argument(["name"]),
                                    get_argument(["params"], True),
                                    get_param(["--admin", "-a"], True, "Run the macro with administrative privileges")
                                    ])

    def execute(self, name, params, admin):
        macros = load_macros()
        if name not in macros:
            click.echo(f"No macro found with the name '{name}'")
            click.echo(click.style(f"\nNOTE: use `tm find <keyword>` command to search macros", fg='blue'))
            return

        param_dict = {str(i + 1): param for i, param in enumerate(params)}

        for cmd in macros[name]:
            try:
                formatted_cmd = re.sub(
                    r"\{(\d+)\}",
                    lambda match: param_dict.get(match.group(1), f"{{{match.group(1)}}}"),
                    cmd
                )

                click.echo(click.style(f"→ {formatted_cmd}", fg='green'))
                if admin:
                    _run_as_admin(formatted_cmd)
                else:
                    os.system(formatted_cmd)
                click.echo("")
            except KeyError as e:
                click.echo(click.style(f"Error: Missing parameter for placeholder '{e.args[0]}'", fg='red'))
                return
            except IndexError as e:
                click.echo(click.style(f"Error: Invalid formatting in command '{cmd}': {e}", fg='red'))
                return
