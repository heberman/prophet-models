from keep_alive import keep_alive
from logvals import logvals
from threading import Thread

keep_alive()

t = Thread(target = logvals)
t.start()