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
from functools import wraps
from typing import Any, List

# Import third-party modules.
import aiohttp

# Import local modules.
from mcsrvstat.ext import *
from mcsrvstat.exceptions import *


# The main coroutine for performing GET requests to the API.
async def perform_get_request(endpoint: str) -> Any | bytes:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as request:
                if request.status != 200:
                    raise DataNotFoundError(f'Request status not OK (failed).')
                elif request.headers['Content-Type'] == 'image/png':
                    return await request.read()
                else:
                    return await request.json()

    except aiohttp.ClientConnectionError:
        raise UnstableInternetError


# The Base class, which does all the hard work for the Stats class.
class Base:
    """
    The root class of the library for directly interacting with the API.

    Parameters:
        - address (`str`): The IP address / link used to join the server.\n
        - platform (`ServerPlatform`): The platform in which the server is running. Defaults to Java.
    """

    endpoints = {
        'server': 'https://api.mcsrvstat.us/',
        'icon': 'https://api.mcsrvstat.us/icon/'
    }

    def __init__(self, address: str, platform: ServerPlatform=ServerPlatform.java) -> None:
        self.platform = platform
        self.address = address

    async def fetch_server(self) -> Any:
        """
        Returns an application/json value for the given server once invoked.
        """
        
        if not isinstance(self.platform, ServerPlatform):
            raise InvalidServerTypeError

        url = self.endpoints['server'] + self.platform.value + self.address
        return await perform_get_request(url)

    async def fetch_server_icon(self) -> Any:
        """
        Returns an image which refers to the server's icon.
        - The image is returned in `bytes`.
        """

        url = self.endpoints['icon'] + self.address
        return await perform_get_request(url)


# The Server class, which is the recommended class to use while interacting with the API.
class Server:
    """
    Represents an instance of a Minecraft server.

    Parameters:
        - address (`str`): The IP address / link used to join the server.\n
        - platform (`ServerPlatform`): The platform in which the server is running. Defaults to Java.
    """

    def __init__(self, address: str, platform: ServerPlatform=ServerPlatform.java) -> None:
        self.base = Base(address=address, platform=platform)

    def fetch_server_decor(type: int=1):
        def decorated(func):
            @wraps(func)
            async def wrapper(self):
                data = await self.base.fetch_server_icon() if type == 2 else self.base.fetch_server()
                return func(self, data)

            return wrapper
        return decorated

    @property
    @fetch_server_decor
    def is_online(self, *args) -> bool:
        """
        Returns a boolean value which indicates whether the server is online or not.
        """

        return args[0]['online']

    @property
    @fetch_server_decor
    def ip(self, *args) -> str:
        """
        The raw IP address of the server.
        """

        return args[0]['ip']

    @property
    @fetch_server_decor
    def port(self, *args) -> int:
        """
        The port used to enter the server.
        """

        return args[0]['port']

    @property 
    @fetch_server_decor
    def hostname(self, *args) -> str:
        """
        The hostname of the server.
        """

        return args[0]['hostname']

    @property
    @fetch_server_decor
    def id(self, *args) -> str:
        """
        The ID of the server. Returns `None` if it's a Java Edition server.
        """

        try:
            return args[0]['serverid']
        except KeyError:
            return None

    @property
    @fetch_server_decor
    def gamemode(self, *args) -> str:
        """
        The default gamemode of the server. Returns `None` if it's a Java Edition server.
        """

        try: 
            return args[0]['gamemode']
        except KeyError:
            return None

    @fetch_server_decor(type=2)
    def get_icon(self, *args) -> Icon:
        """
        Gives out an `Icon` object containing the icon of the server.
        """
        
        return Icon(args[0])

    @fetch_server_decor
    def get_motd(self, *args) -> ServerMOTD:
        """
        Gives out a `ServerMOTD` object containing the server's MOTD in different types (clean, raw, HTML).

        Exceptions:
        - `DataNotFoundError` - If the MOTD of the server is not found.
        """

        try:
            motd = args[0]['motd']
        except KeyError:
            raise DataNotFoundError('Failed to fetch server MOTD.')
        else:
            return ServerMOTD(raw=motd['raw'], clean=motd['clean'], html=motd['html'])

    @fetch_server_decor
    def get_info(self, *args) -> ServerInfo:
        """
        Gives out a `ServerInfo` object containing the server's base information (if any).

        Exceptions:
        - `DataNotFoundError` - If the server information data is not found.
        """

        try:
            info = args[0]['info']
        except KeyError:
            raise DataNotFoundError('Failed to fetch server base information.')
        else:
            return ServerInfo(raw=info['raw'], clean=info['clean'], html=info['html'])
    
    @fetch_server_decor
    def get_plugins(self, *args) -> ServerPlugins:
        """
        Gives out a `ServerPlugins` object containing the names of the plugins that have been used in the development of the server.

        Exceptions:
        - `DataNotFoundError` - If the data for installed plugins is not found.
        """

        try:
            plugins = args[0]['plugins']
        except KeyError:
            raise DataNotFoundError('Failed to fetch server plugin data.')
        else:
            return ServerPlugins(names=plugins['names'], raw=plugins['raw'])

    @fetch_server_decor
    def get_mods(self, *args) -> ServerMods:
        """
        Gives out a `ServerMods` object containing the names of active mods that are being used the server.

        Exceptions:
        - `DataNotFoundError` - If the data for installed mods is not found.
        """

        try:
            mods = args[0]['mods']
        except KeyError:
            raise DataNotFoundError('Failed to fetch server mods data.')
        else:
            return ServerPlugins(names=mods['names'], raw=mods['raw'])

    @fetch_server_decor
    def get_software(self, *args) -> ServerSoftware:
        """
        Gives out a `ServerSoftware` object containing the version and software information of the given server.

        Exceptions:
        - `DataNotFoundError` - If the server software data is not found.
        """

        try:
            return ServerSoftware(version=args[0]['version'], software=args[0]['software'])
        except KeyError:
            raise DataNotFoundError('Failed to fetch server software data.')

    @fetch_server_decor
    def get_debug_values(self, *args) -> ServerDebugInfo:
        """
        Gives out a `ServerDebugValue` object containing all the accessible debug values of the given server.
        """

        debug_values = args[0]['debug']
        return ServerDebugInfo(
            ping=debug_values['ping'],
            query=debug_values['query'],
            srv=debug_values['srv'],
            querymismatch=debug_values['querymismatch'],
            ipinsrv=debug_values['ipinsrv'],
            cnameinsrv=debug_values['cnameinsrv'],
            animatedmotd=debug_values['animatedmotd'],
            cachetime=debug_values['cachetime'],
            apiversion=debug_values['apiversion']
        )
        
    @fetch_server_decor
    def get_player_by_name(self, *args, player_name: str) -> Player:
        """
        Gives out a `Player` object if a player is found active / online by the given name. 
        
        Exceptions:
        - `DataNotFoundError` - If the player data is not found.
        """

        try:
            uuid = args[0]['players']['uuid']
            if player_name in uuid:
                return Player(name=player_name, uuid=uuid[player_name])

        except KeyError:
            raise DataNotFoundError('Failed to fetch player data.')

    @fetch_server_decor
    def get_player_count(self, *args) -> ServerPlayerCount:
        """
        Gives out a `ServerPlayerCount` object containing both the online and the max player count. 
        
        Exceptions:
        - `DataNotFoundError` - If the player count data is not found.
        """
        
        try:
            return ServerPlayerCount(
                online=args[0]['players']['online'], 
                max=args[0]['players']['max']
            )
        except KeyError:
            raise DataNotFoundError('Failed to fetch player count data.')

    @fetch_server_decor
    def get_players(self, *args) -> List[Player] | None:
        """
        Gives out a list containing `Player` objects, each indicating an online player. 
        Returns `None` if no players are found.
        """

        try:
            players = [
                Player(name=name, uuid=uuid) for name, uuid in args[0]['players']['uuid'].items()
            ]
            return players

        except KeyError:
            return None
