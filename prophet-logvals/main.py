import asyncio
from keep_alive import keep_alive
from logvals import logvals
from randotron import randotron
from threading import Thread

keep_alive()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

t1 = Thread(target=loop.run_until_complete, args=(randotron(),))
t1.start()

t2 = Thread(target=loop.run_until_complete, args=(logvals(),))
t2.start()