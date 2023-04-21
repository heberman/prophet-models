import requests
import time
import datetime

def logvals():
    eastern_offset = datetime.timedelta(hours=-5)
    eastern_tz = datetime.timezone(eastern_offset)
    while True:
        now = datetime.datetime.now(eastern_tz)
        while now.weekday() in range(1, 6) and now.hour >= 4 and now.hour < 20:
            res = requests.post('https://thankful-elk-windbreaker.cyclic.app/logvals')
            res.raise_for_status()
            time.sleep(600)
            now = datetime.datetime.now(eastern_tz)