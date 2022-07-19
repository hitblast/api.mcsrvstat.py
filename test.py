import asyncio
from mcsrvstat import Server
from mcsrvstat.ext import ServerPlatform

server = Server('bedcraft.minecraftersbd.com')

async def main():
    icon = await server.icon
    icon.save()

if __name__ == '__main__':
    asyncio.run(main())