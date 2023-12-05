# SPDX-License-Identifier: MIT


# Import built-in modules.
import asyncio
from typing import Any, Coroutine, List, Optional, Union

# Import third-party modules.
import aiohttp

# Import local modules.
from mcsrvstat.exceptions import *
from mcsrvstat.ext import *


# The Base class, which does all the hard work for the Stats class.
class Base:
    """
    The root class of the library for directly interacting with the API.

    Caution:
        - The direct usage of this class is not encouraged since this class supports no other
        external wrapper classes and enforces full manual control.

    Parameters:
        `address: str` - The IP address used to join the server.\n
        `platform: ServerPlatform` - The platform of the server. Defaults to Java edition.
    """

    endpoints = {'server': 'https://api.mcsrvstat.us/', 'icon': 'https://api.mcsrvstat.us/icon/'}

    def __init__(self, address: str, platform: ServerPlatform = ServerPlatform.java) -> None:
        self.platform = platform
        self.address = address

    # The primary static method for performing API requests.
    @staticmethod
    async def perform_get_request(endpoint: str) -> Union[Any, bytes]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as request:
                    if request.status != 200:
                        raise DataNotFoundError('Request status not OK (failed).')
                    elif request.headers['Content-Type'] == 'image/png':
                        return await request.read()
                    else:
                        return await request.json()

        except aiohttp.ClientConnectionError:
            raise UnstableInternetError

    # Performs a GET request to the API for loading the server data.
    async def fetch(self) -> Any:
        if not isinstance(self.platform, ServerPlatform):
            raise InvalidServerTypeError

        url = self.endpoints['server'] + self.platform.value + self.address
        return await self.perform_get_request(url)

    # Basically fetch() but modified for getting a server's icon.
    async def fetch_icon(self) -> Any:
        url = self.endpoints['icon'] + self.address
        return await self.perform_get_request(url)


# The Server class, which is the recommended class to use while interacting with the API.
class Server:
    """
    Represents an instance of a Minecraft server.

    Parameters:
        `address: str` - The IP address used to join the server.\n
        `platform: ServerPlatform` - The platform of the server. Defaults to Java edition.
    """

    def __init__(self, address: str, platform: ServerPlatform = ServerPlatform.java) -> None:
        self.base = Base(address=address, platform=platform)
        self.data = None
        self.data_icon = None

    def precheck(func) -> Coroutine:
        """
        A redundancy decorator to ensure that the data of the server has been loaded.
        """

        async def wrapper(self: Server):
            if not self.data or not self.data_icon:
                raise UnloadedError
            else:
                return func(self)

        return wrapper

    async def fetch(self) -> None:
        """
        Performs the required requests to the Minecraft Server Status API and loads the fetched data to the class instance.
        """

        try:
            self.data, self.data_icon = await asyncio.gather(self.base.fetch(), self.base.fetch_icon())
        except Exception:
            pass  # FIXME: just for demonstration right here (testing purposes)

    @property
    @precheck
    def is_online(self) -> bool:
        """
        Returns a `bool` value which indicates whether the server is online or not.
        """

        return self.data['online']

    @property
    @precheck
    def ip(self) -> str:
        """
        The raw IP address of the server.
        """

        return self.data['ip']

    @property
    @precheck
    def port(self) -> int:
        """
        The port used to enter the server.
        """

        return self.data['port']

    @property
    @precheck
    def hostname(self) -> str:
        """
        The hostname of the server.
        """

        return self.data['hostname']

    @property
    @precheck
    def id(self) -> str:
        """
        The ID of the server. (`None` if Java Edition)
        """

        try:
            return self.data['serverid']
        except KeyError:
            return None

    @property
    @precheck
    def gamemode(self) -> str:
        """
        The default gamemode of the server. (`None` if Java Edition)
        """

        try:
            return self.data['gamemode']
        except KeyError:
            return None

    @precheck
    def get_motd(self) -> ServerMOTD:
        """
        Gives out a `ServerMOTD` object containing the server's MOTD in different types (clean, raw, HTML).

        Exceptions:
            `DataNotFoundError` - If the MOTD of the server is not found.
        """

        try:
            motd = self.data['motd']
        except KeyError:
            raise DataNotFoundError('Failed to fetch server MOTD.')
        else:
            return ServerMOTD(raw=motd['raw'], clean=motd['clean'], html=motd['html'])

    @precheck
    def get_info(self) -> ServerInfo:
        """
        Gives out a `ServerInfo` object containing the server's base information (if any).

        Exceptions:
            `DataNotFoundError` - If the server information data is not found.
        """

        try:
            info = self.data['info']
        except KeyError:
            raise DataNotFoundError('Failed to fetch server base information.')
        else:
            return ServerInfo(raw=info['raw'], clean=info['clean'], html=info['html'])

    @precheck
    def get_plugins(self) -> ServerPlugins:
        """
        Gives out a `ServerPlugins` object containing the names of the plugins
        that have been used in the development of the server.

        Exceptions:
            `DataNotFoundError` - If the data for installed plugins is not found.
        """

        try:
            plugins = self.data['plugins']
        except KeyError:
            raise DataNotFoundError('Failed to fetch server plugin data.')
        else:
            return ServerPlugins(names=plugins['names'], raw=plugins['raw'])

    @precheck
    def get_mods(self) -> ServerMods:
        """
        Gives out a `ServerMods` object containing the names of active mods that are being used the server.

        Exceptions:
            `DataNotFoundError` - If the data for installed mods is not found.
        """

        try:
            mods = self.data['mods']
        except KeyError:
            raise DataNotFoundError('Failed to fetch server mods data.')
        else:
            return ServerPlugins(names=mods['names'], raw=mods['raw'])

    @precheck
    def get_software(self) -> ServerSoftware:
        """
        Gives out a `ServerSoftware` object containing the version and software information of the given server.

        Exceptions:
            `DataNotFoundError` - If the server software data is not found.
        """

        try:
            return ServerSoftware(version=self.data['version'], software=self.data['software'])
        except KeyError:
            raise DataNotFoundError('Failed to fetch server software data.')

    @precheck
    def get_debug_values(self) -> ServerDebugInfo:
        """
        Gives out a `ServerDebugValue` object containing all the accessible debug values of the given server.
        """

        debug_values = self.data['debug']
        return ServerDebugInfo(
            ping=debug_values['ping'],
            query=debug_values['query'],
            srv=debug_values['srv'],
            querymismatch=debug_values['querymismatch'],
            ipinsrv=debug_values['ipinsrv'],
            cnameinsrv=debug_values['cnameinsrv'],
            animatedmotd=debug_values['animatedmotd'],
            cachehit=debug_values['cachehit'],
            cachetime=debug_values['cachetime'],
            cacheexpire=debug_values['cacheexpire'],
            apiversion=debug_values['apiversion'],
        )

    @precheck
    def get_player_by_name(self, player_name: str) -> Player:
        """
        Gives out a `Player` object if a player is found active / online by the given name.

        Parameters:
            `player_name: str` - The name of the player you wish to fetch.

        Exceptions:
            `DataNotFoundError` - If the player data is not found.
        """

        try:
            if player_name in (uuid := self.data['players']['uuid']):
                return Player(name=player_name, uuid=uuid[player_name])

        except KeyError:
            raise DataNotFoundError('Failed to fetch player data.')

    @precheck
    def get_player_count(self) -> ServerPlayerCount:
        """
        Gives out a `ServerPlayerCount` object containing both the online and the max player count.

        Exceptions:
            `DataNotFoundError` - If the player count data is not found.
        """

        try:
            return ServerPlayerCount(online=self.data['players']['online'], max=self.data['players']['max'])
        except KeyError:
            raise DataNotFoundError('Failed to fetch player count data.')

    @precheck
    def get_players(self) -> Optional[List[Player]]:
        """
        Gives out a list containing `Player` objects, each indicating an online player.\n
        Returns `None` if no players are found.
        """

        try:
            return [Player(name=name, uuid=uuid) for name, uuid in self.data['players']['uuid'].items()]
        except KeyError:
            return None
