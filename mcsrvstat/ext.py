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


# Import built-in modules.
from io import BytesIO
from enum import Enum
from dataclasses import dataclass

# Import third-party modules.
from PIL import Image


# Enums.
class ServerPlatform(Enum):
    java = '2/'
    bedrock = 'bedrock/2/'
    

# Classes.
class Icon:
    """
    Represents the icon of a server.

    Methods:
        `save()` - Saves the icon locally.
    """

    def __init__(self, data: bytes):
        self.data = data

    def save(self, name: str='result') -> str:
        """
        Saves the icon on the local machine.

        Parameters:
            name (`str`): The name to use for the new file (doesn't change the format of the image). Defaults to `result`.

        Returns: 
            The full name (with extension) of the file.
        """

        im = Image.open(BytesIO(self.data))
        file_name = f'{name}.{im.format.lower()}'

        im.save(file_name)
        return file_name


# Data classes.
@dataclass(frozen=True)
class Player:
    """
    Represents a player from a Minecraft server.

    Attributes:
        `name` - The friendly name of the player.\n
        `uuid` - The UUID of the player.
    """

    name: str
    uuid: str


@dataclass(frozen=True)
class ServerMOTD:
    """
    Represents the 'Message of the Day' or 'MOTD'

    Attributes:
        `raw` - No formatting, get the raw one.\n
        `clean` - Retrieve the MOTD in an already formatted way.\n
        `html` - Retrieve the MOTD in HTML.
    """

    raw: list
    clean: list
    html: list


@dataclass(frozen=True)
class ServerInfo:
    """
    The default class for accessing base server information in different formats.

    Attributes:
        `raw` - No formatting, get the raw one.\n
        `clean` - Retrieve the info in an already formatted way.\n
        `html` - Retrieve the info in HTML.
    """

    raw: list
    clean: list
    html: list


@dataclass(frozen=True)
class ServerPlugins: 
    """
    The default class for accessing data on the server's plugins.

    Attributes:
        `names` - Formatted names of the used plugins.\n
        `raw` - No formatting, get the raw ones.
    """

    names: list
    raw: list
        

@dataclass(frozen=True)
class ServerMods: 
    """
    The default class for accessing data on the server's mods.

    Attributes:
        `names` - Formatted names of the used plugins.\n
        `raw` - No formatting, get the raw ones.
    """

    names: list
    raw: list


@dataclass(frozen=True)
class ServerSoftware:
    """
    The default class for accessing server software and version information.

    Attributes:
        `version` - The version of the backend used by the server.\n
        `software` - The software / vendor name.'
    """

    version: str
    software: str


@dataclass(frozen=True)
class ServerDebugInfo:
    """
    The default class for accessing server debug values.

    Attributes:
        Get information on different debug values from the official [documentation](https://api.mcsrvstat.us).
    """

    ping: bool
    query: bool
    srv: bool
    querymismatch: bool
    ipinsrv: bool
    cnameinsrv: bool
    animatedmotd: bool
    cachetime: int
    apiversion: int


@dataclass(frozen=True)
class ServerPlayerCount:
    """
    The default class for accessing server player count.

    Attributes:
        `online` - The amount of players currently online.\n
        `max` - The maximum amount of players the server can hold at a time.
    """

    online: int
    max: int
