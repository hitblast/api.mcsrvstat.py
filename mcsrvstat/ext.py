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
    """Represents the icon of a server.

    Methods:
        save(): Saves the icon locally.
    """

    def __init__(self, data: bytes):
        self.data = data

    def save(self, name: str = 'result') -> str:
        """Saves the icon locally.

        Args:
            name (str): The name to use for the image file. Defaults to "result".
        """

        im = Image.open(BytesIO(self.data))
        file_name = f'{name}.{im.format.lower()}'

        im.save(file_name)
        return file_name


# Data classes.
@dataclass(frozen=True)
class Player:
    """Represents a player from the server.

    Attributes:
        name (str): The friendly name of the player.
        uuid (str): The UUID of the player.
    """

    name: str
    uuid: str


@dataclass(frozen=True)
class ServerMOTD:
    """Represents the 'Message of the Day' or 'MOTD' of the server.

    Attributes:
        raw (str): No formatting, get the raw one.
        clean (str): Retrieve the MOTD in an already formatted way.
        html (str): Retrieve the MOTD in HTML.
    """

    raw: str
    clean: str
    html: str


@dataclass(frozen=True)
class ServerInfo:
    """The default class for accessing base server information in different formats.

    Attributes:
        raw (list): No formatting, get the raw one.
        cleaw (list): Retrieve the info in an already formatted way.
        htmw (list): Retrieve the info in HTML.
    """

    raw: list
    clean: list
    html: list


@dataclass(frozen=True)
class ServerPlugin:
    """Represents a server plugin.

    Attributes:
        name (str): The name of the plugin.
        version (str): The version of the plugin.
    """

    name: str
    version: str


@dataclass(frozen=True)
class ServerMod:
    """Represents a mod installed on the server.

    Attributes:
        name (str): The name of the mod.
        version (str): The version of the mod.
    """

    name: str
    version: str


@dataclass(frozen=True)
class ServerDebugInfo:
    """The default class for accessing server debug values.

    Attributes:
        Get information on different debug values from the official [documentation](https://api.mcsrvstat.us).
    """

    # TODO: Add detailed explanation on the debug values instead of refering to external links

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
        online (int): The amount of players currently online.\n
        max (int): The maximum amount of players the server can hold at a time.
    """

    online: int
    max: int
