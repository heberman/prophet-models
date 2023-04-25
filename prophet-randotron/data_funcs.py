from datetime import datetime
import requests
import json
from copy import deepcopy


def get_days_ago(days):
    now = datetime.now()
    timezone_offset = now.utcoffset().total_seconds() * 1000  # Convert timezone offset to milliseconds
    eastern_timezone_offset = -5 * 60 * 60 * 1000  # Eastern Timezone is UTC-4
    
    days_ago = datetime.fromtimestamp((now.timestamp() - (days * 24 * 60 * 60)) * 1000 + timezone_offset + eastern_timezone_offset / 1000)
    
    return days_ago


async def get_user(username):
    res = await requests.get(f'https://thankful-elk-windbreaker.cyclic.app/user/{username}')
    user_data = json.loads(res.content)
    return user_data.foundUser


async def get_ticker_price(ticker):
    API_KEY = 'MG0ID5XPDBCTO9FF'
    api_call = 'https://www.alphavantage.co/query?' \
               + 'function=TIME_SERIES_INTRADAY' \
               + '&symbol=' + ticker \
               + '&interval=1min' \
               + '&outputsize=full' \
               + '&apikey=' + API_KEY

    curr_day = None
    curr_price = None
    tradable = None
    error = None

    try:
        res = await requests.get(api_call)
        res.raise_for_status()
        data = res.json()
        if 'Error Message' in data:
            raise ValueError(f"Ticker '{ticker}' does not exist.")
        new_data = data['Time Series (1min)']
        yesterday = get_days_ago(1)
        times = list(new_data.keys())

        i = 0
        while yesterday.timestamp() * 1000 - datetime.fromisoformat(times[i]).timestamp() * 1000 < 0:
            i += 1
            if i >= len(times):
                raise ValueError("Loop went wrong.")
        curr_day = times[i]
        curr_price = new_data[times[i]]['4. close']
        tradable = (yesterday.timestamp() * 1000 - (10 * 60 * 1000)) - datetime.fromisoformat(times[i]).timestamp() * 1000 <= 0
    except Exception as err:
        error = str(err)
        print(err)

    return {'currPrice': curr_price, 'currDay': curr_day, 'tradable': tradable, 'error': error}


async def get_ticker_data(ticker, func, interval=None, outputsize=None, data_key=None):
    API_KEY = 'MG0ID5XPDBCTO9FF'
    api_call = 'https://www.alphavantage.co/query?' \
               + 'function=' + func \
               + '&symbol=' + ticker \
               + (f'&interval={interval}' if interval else '') \
               + '&outputsize=' + outputsize \
               + '&apikey=' + API_KEY
    new_data = None
    error = None

    try:
        res = await requests.get(api_call)
        res.raise_for_status()
        data = res.json()
        if 'Error Message' in data:
            raise ValueError(f"{ticker}: {data['Error Message']}")
        new_data = data[data_key]
    except Exception as err:
        error = str(err)
        print(err)

    return {'newData': new_data, 'error': error}


def make_trade(user, ticker, numShares, price):
    newUser = deepcopy(user)
    trade = {'ticker': ticker, 'numShares': numShares, 'date': datetime.now(), 'price': price}
    print(trade)
    newUser['trades'] = [trade] + newUser['trades']
    if ticker in newUser['portfolio']:
        newUser['portfolio'][ticker] += numShares
        if newUser['portfolio'][ticker] <= 0:
            del newUser['portfolio'][ticker]
    else:
        newUser['portfolio'][ticker] = numShares
    newUser['cash'] -= numShares * price
    return newUser


async def get_portfolio_value(portfolio):
    priceMap = {}
    portVal = 0
    for ticker in portfolio.keys():
        shares = portfolio.get(ticker)
        data = await get_ticker_price(ticker)
        currPrice = data["currPrice"]
        priceMap[ticker] = currPrice
        portVal += shares * currPrice
    return {"priceMap": priceMap, "portVal": portVal}