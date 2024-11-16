import click

COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_CYAN = "\033[36m"
COLOR_RESET = "\033[0m"


def print_diff(diff):
    if diff:
        click.echo("Showing changes:")
        for index, line in enumerate(diff, 1):
            if line.startswith("---") or line.startswith("+++"):
                click.echo(f"{COLOR_CYAN}{line}{COLOR_RESET}")
            elif line.startswith("-"):
                click.echo(f"{COLOR_RED}{line}{COLOR_RESET}")
            elif line.startswith("+"):
                click.echo(f"{COLOR_GREEN}{line}{COLOR_RESET}")
            else:
                click.echo(line)
    else:
        click.echo("No changes made.")
