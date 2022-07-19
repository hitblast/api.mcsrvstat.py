'''
MIT License

Copyright (c) 2022 HitBlast

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


# Import third-party modules.
import click
import asyncio

# Import local modules.
from mcsrvstat.main import Base
from mcsrvstat.ext import ServerPlatform


# Setting up the default group for Click.
@click.group()
def cli():
    pass


# The main command (fetch, in this case).
@cli.command()
@click.option('-a', '--address', required=True, type=str, help='The IP address of the  Minecraft server you wish to fetch.')
@click.option('--bedrock', help='Flags the server as a Bedrock Edition instance.', is_flag=True)
def fetch(address: str, bedrock: bool):
    """Fetches the server data from the Minecraft Server Status API."""
    
    platform = ServerPlatform.bedrock if bedrock else ServerPlatform.java
    base = Base(platform=platform, ip_address=address)

    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(base.fetch_server())

    for key, value in data.items():
        if not type(value) == dict:
            print(f'{key:<20} {value}')
        else:
            print(f'\n{key:<20}'.upper())
            for key2, value2 in value.items():
                print(f'{key2:<20} {value2}')