# SPDX-License-Identifier: MIT


# Import built-in modules.
import asyncio

# Import third-party modules.
import click

# Import local modules.
from mcsrvstat.ext import Icon, ServerPlatform
from mcsrvstat.main import Base


# Setting up the default group for Click.
@click.group()
def cli():
    pass


# The main command (fetch, in this case).
@cli.command()
@click.option('-a', '--address', required=True, type=str, help='The IP address of a Minecraft server.')
@click.option('--bedrock', help='Flags the server as a Bedrock Edition instance.', is_flag=True)
@click.option('--save-icon', help='Downloads the icon of the server and saves it locally.', is_flag=True)
def fetch(address: str, bedrock: bool, save_icon: bool):
    """Fetches the server data from the Minecraft Server Status API."""

    platform = ServerPlatform.bedrock if bedrock else ServerPlatform.java
    base = Base(platform=platform, address=address)
    loop = asyncio.get_event_loop()

    if save_icon:
        data = loop.run_until_complete(base.fetch_server_icon())
        icon = Icon(data)
        return click.echo(f'Icon saved as {icon.save(address)}')

    data = loop.run_until_complete(base.fetch_server())
    for key, value in data.items():
        if not isinstance(value, dict):
            click.echo(f'{key:<20} {value}')
        else:
            click.echo(f'\n{key:<20}'.upper())
            for key2, value2 in value.items():
                click.echo(f'{key2:<20} {value2}')
