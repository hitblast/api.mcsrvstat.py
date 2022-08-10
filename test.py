# Importing the libraries required.
import asyncio
import mcsrvstat

# Setting up our Server instance.
server = mcsrvstat.Server(
    address='play.applecraft.org',
    platform=mcsrvstat.ext.ServerPlatform.java
)


# Writing some code inside our main() coroutine.
async def main():
    if await server.is_online:
        print('Server is online!')

# Calling main() using asyncio.
if __name__ == '__main__':
    asyncio.run(main())
