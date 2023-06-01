import click
from records import commands as records_commands

RECORDS_TABLE = '.records.json'
@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    ctx.obj['records_table'] = RECORDS_TABLE
    pass

cli.add_command(records_commands.all)