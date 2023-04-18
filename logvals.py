import requests
import time

def logvals():
    while True:
        res = requests.get('https://thankful-elk-windbreaker.cyclic.app/test')
        time.sleep(60)
        
