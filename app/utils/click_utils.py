import click


def get_argument(arg: str, nargs=False):
    if nargs:
        return [click.Argument([arg], nargs=-1)]
    return [click.Argument([arg])]


def get_arguments(args: list[str]):
    arguments = []
    for arg in args:
        arguments.append(click.Argument([arg]))

    return arguments
