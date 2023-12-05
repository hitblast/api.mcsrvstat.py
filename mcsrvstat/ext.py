# SPDX-License-Identifier: MIT


# Import built-in modules.
from dataclasses import dataclass
from enum import Enum
from io import BytesIO

# Import third-party modules.
from PIL import Image


# Enums.
class ServerPlatform(Enum):
    java = '3/'
    bedrock = 'bedrock/3/'


# Classes.
class Icon:
    """
    Represents the icon of a server.

    Methods:
        `save()` - Saves the icon locally.
    """

    def __init__(self, data: bytes):
        self.data = data

    def save(self, name: str = 'result') -> str:
        """
        Saves the icon on the local machine.

        Parameters:
            name (`str`): The name to use for the new file (doesn't change the format of the image).
            Defaults to `result`.

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
    Represents a player from the server.

    Attributes:
        `name` - The friendly name of the player.\n
        `uuid` - The UUID of the player.
    """

    name: str
    uuid: str


@dataclass(frozen=True)
class ServerMOTD:
    """
    Represents the 'Message of the Day' or 'MOTD' of the server.

    Attributes:
        `raw` - No formatting, get the raw one.\n
        `clean` - Retrieve the MOTD in an already formatted way.\n
        `html` - Retrieve the MOTD in HTML.
    """

    raw: str
    clean: str
    html: str


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
class ServerPlugin:
    """
    Represents a server plugin.

    Attributes:
        `name` - The name of the plugin.\n
        `version` - The version of the plugin.
    """

    name: str
    version: str


@dataclass(frozen=True)
class ServerMod:
    """
    Represents a server mod.

    Attributes:
        `name` - The name of the mod.\n
        `version` - The version of the mod.
    """

    name: str
    version: str


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
    cachehit: bool
    cachetime: int
    cacheexpire: int
    apiversion: int


@dataclass(frozen=True)
class PlayerCount:
    """
    Represents the current player count of the server.

    Attributes:
        `online` - The amount of players currently online.\n
        `max` - The maximum amount of players the server can hold at a time.
    """

    online: int
    max: int
