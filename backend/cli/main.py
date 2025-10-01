import click

from cli.groups.run import run
from cli.groups.tools import tools


@click.group(help="Основная CLI группа")
def cli():
    pass


cli.add_command(tools)  # noqa
cli.add_command(run)  # noqa
