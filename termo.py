#!/usr/bin/env python3
import click

from app.commands.cancel import CancelCommand
from app.commands.delete import DelCommand
from app.commands.desc import DescCommand
from app.commands.edit import EditCommand
from app.commands.exec import ExecCommand
from app.commands.find import FindCommand
from app.commands.list import ListCommand
from app.commands.new import NewCommand
from app.commands.save import SaveCommand
from app.default_group import DefaultGroup
from app.utils.config_utils import (is_first_run,
                                    display_setup_guide,
                                    complete_first_run)


@click.group(cls=DefaultGroup, default_if_no_args=False,
             help="Pass command to run or just macro name to 'exec' given macro")
def cli():
    if is_first_run():
        display_setup_guide()
        complete_first_run()
    pass


def _get_click_argument(name):
    return click.argument(name)


NewCommand().register(cli, _get_click_argument("name"))
ListCommand().register(cli)
CancelCommand().register(cli)
SaveCommand().register(cli)
ExecCommand().register(cli, _get_click_argument("name"))
FindCommand().register(cli, _get_click_argument("keyword"))
DescCommand().register(cli, _get_click_argument("name"))
DelCommand().register(cli, _get_click_argument("name"))
EditCommand().register(cli, _get_click_argument("name"))

if __name__ == "__main__":
    cli()
