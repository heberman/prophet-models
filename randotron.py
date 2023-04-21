import time
import datetime
import requests
import json
import random
from data_funcs import make_trade, get_user


def parse_tickers():
    tickers = []
    with open('tickers.txt', 'r') as file:
        for ticker in file:
            tickers.append(ticker.strip())
    return tickers


async def randotron():
    tickers = parse_tickers()
    eastern_offset = datetime.timedelta(hours=-5)
    eastern_tz = datetime.timezone(eastern_offset)

    # Want to buy a random stock every 30 min and choose a random time in the day
    # to sell it (5 min intervals). 6AM - 1PM = 7 hours * 12 5min intervals per hour = 84.
    # if each 5min interval is represented by an index, can trade from 0 to 83,
    # will track with counter

    while True:
        counter = 0
        # porfolio is a list of tuples: (ticker, shares, sell_time)
        day_portfolio = []
        starting_cash = 0
        now = datetime.datetime.now(eastern_tz)
        while now.weekday() in range(1, 6) and now.hour >= 6 and now.hour < 14:
            # default user as None, only get user from db if trade is made
            user = None
            # if counter == 0, get user and log starting cash for the day
            if counter == 0:
                user = await get_user('randotron')
                starting_cash = user['cash']
            # check if stock should be sold
            for (ticker, shares, sell_time) in day_portfolio:
                if user is None:
                    user = await get_user('randotron')
                if sell_time == counter:
                    res = await requests.get(f'https://thankful-elk-windbreaker.cyclic.app/price/{ticker}')
                    ticker_data = json.loads(res.content)
                    price = ticker_data['currPrice']
                    user = make_trade(user, ticker, shares * -1, price)
            if counter % 6 == 0:
                # buy random stock, number of shares will be at most 1/12 of starting cash
                if user is None:
                    user = await get_user('randotron')
                ticker_tradable = False
                while not ticker_tradable:
                    random_ticker = random.choice(tickers)
                    res = await requests.get(f'https://thankful-elk-windbreaker.cyclic.app/price/{random_ticker}')
                    random_ticker_data = json.loads(res.content)
                    ticker_tradable = random_ticker_data['tradable']
                random_ticker_price = random_ticker_data['currPrice']
                buy_shares = (starting_cash / 12) // random_ticker_price
                user = make_trade(user, random_ticker, buy_shares, random_ticker_price)
                sell_time = random.randint(counter + 1, 83)
                day_portfolio.append(random_ticker, buy_shares, sell_time)
            # update user only is trade is made
            if user is not None:
                res = await requests.put('https://thankful-elk-windbreaker.cyclic.app/user/randotron', json=user)
            time.sleep(300)
            counter += 1
            now = datetime.datetime.now(eastern_tz)
