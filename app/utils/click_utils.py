import click


def get_argument(param_decls: list[str], nargs=False):
    if nargs:
        return click.Argument(param_decls=param_decls, nargs=-1)
    return click.Argument(param_decls=param_decls)


def get_param(param_decls: list[str], is_flag=False, help=None):
    return click.Option(
        param_decls=param_decls, is_flag=is_flag, help=help
    )
