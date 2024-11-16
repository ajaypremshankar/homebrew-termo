import click


def get_argument(arg: str):
    return [click.Argument([arg])]
