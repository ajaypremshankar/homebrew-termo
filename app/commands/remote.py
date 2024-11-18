import paramiko
import click
from app.commands.base_command import Command
from app.utils.config_utils import load_macros
import re

class RemoteCommand(Command):
    """Command to execute a macro on a remote machine via SSH."""

    def __init__(self):
        super().__init__(
            name="remote",
            help_text="Execute a macro on a remote machine via SSH (beta)",
            arguments=[
                click.Argument(["name"]),
                click.Argument(["params"], nargs=-1),
                click.Option(["--host", "-h"], required=True, help="Remote host (user@host)."),
                click.Option(["--port", "-p"], default=22, type=int, help="SSH port (default: 22)."),
                click.Option(["--key", "-k"], default=None, help="Path to SSH private key."),
                click.Option(["--password", "-P"], default=None, help="Password for SSH authentication."),
            ],
        )

    def execute(self, name, params, host, port, key, password):
        macros = load_macros()
        if name not in macros:
            click.echo(f"No macro found with the name '{name}'.")
            return

        commands = macros[name]

        # Format commands with parameters if provided
        param_dict = {str(i + 1): param for i, param in enumerate(params)}
        try:
            formatted_commands = [re.sub(
                    r"\{(\d+)\}",
                    lambda match: param_dict.get(match.group(1), f"{{{match.group(1)}}}"),
                    cmd
                ) for cmd in commands]
        except KeyError as e:
            click.echo(f"Error: Missing parameter for placeholder '{e.args[0]}'.")
            return

        # Parse host and user
        if "@" in host:
            user, host = host.split("@", 1)
        else:
            user = "root"

        # Connect to the remote machine
        try:
            click.echo(f"Connecting to {user}@{host}:{port}...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if key:
                ssh.connect(hostname=host, port=port, username=user, key_filename=key)
            elif password:
                ssh.connect(hostname=host, port=port, username=user, password=password)
            else:
                click.echo("Error: Provide either a private key or a password for authentication.")
                return

            # Execute commands remotely
            click.echo(f"Executing macro '{name}' on {host}:\n")
            for cmd in formatted_commands:
                click.echo(click.style(f"→ {cmd}", fg="green"))
                stdin, stdout, stderr = ssh.exec_command(cmd)
                output = stdout.read().decode("utf-8")
                error = stderr.read().decode("utf-8")
                if output:
                    click.echo(output)
                if error:
                    click.echo(click.style(f"Error: {error}", fg="red"))

            ssh.close()
        except Exception as e:
            click.echo(click.style(f"Error: Unable to connect or execute commands: {e}", fg="red"))
