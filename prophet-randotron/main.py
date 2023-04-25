import asyncio

from randotron import randotron
from keep_alive import keep_alive

keep_alive()


async def main():
  await randotron()


asyncio.run(main())
