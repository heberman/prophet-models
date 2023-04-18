import requests
import time
import datetime

def logvals():
    while True:
        now = datetime.datetime.now()

        while now.weekday() in range(1,6) and now.hour >= 5 and now.hour <= 20:
            res = requests.post('https://thankful-elk-windbreaker.cyclic.app/logvals')
            time.sleep(3600)
            now = datetime.datetime.now()
        
