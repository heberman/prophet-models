from keep_alive import keep_alive
from logvals import logvals
from randotron import randotron
from threading import Thread

keep_alive()

t1 = Thread(target = logvals)
t2 = Thread(target = randotron)

t1.start()
t2.start()