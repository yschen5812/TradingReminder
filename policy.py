from collections import deque
from datetime import datetime

def getSellLimit(trades, func, **kw):
    pureBoughtHistory = func(trades)

    # TODO: handle kw parameters

    result = {
        "no sell limit":{}, # {ticker: quantity(int)}
        "limited": {}       # {ticker: deque( { limit: int, quantity: int, date: date} ) }
    }

    asOfDay = datetime.now().date() # Currently only handle current date

    for item in pureBoughtHistory.items():
        ticker, trades = item[0], item[1]
        for trade in reversed(trades):
            date = trade["Date"]
            ticker = trade["Ticker"]
            quantity = trade["Quantity"]
            value = trade["Value"]

            if (asOfDay - date).days > 30:
                # no limit
                if not ticker in result["no sell limit"]:
                    result["no sell limit"][ticker] = 0
                result["no sell limit"][ticker] += int(quantity)

            else:
                if not ticker in result["limited"]:
                    result["limited"][ticker] = deque()
                stack = result["limited"][ticker]
                stack.appendleft({"limit": value, "quantity": quantity, "date": date})
                result["limited"][ticker] = stack

    return result


def processBloombergPolicy(trades):
    boughtStocksToTrades, soldStocksToTrades = {}, {}

    for trade in trades:
        ticker, action = trade["Ticker"], trade["Action"]

        if action == "sell":
            if ticker in soldStocksToTrades:
                stack = soldStocksToTrades[ticker]
                stack.appendleft(trade)
                soldStocksToTrades[ticker] = stack
            else:
                stack = deque()
                stack.appendleft(trade)
                soldStocksToTrades[ticker] = stack
        elif action == "buy":
            if ticker in boughtStocksToTrades:
                stack = boughtStocksToTrades[ticker]
                stack.appendleft(trade)
                boughtStocksToTrades[ticker] = stack
            else:
                stack = deque()
                stack.appendleft(trade)
                boughtStocksToTrades[ticker] = stack


    for item in soldStocksToTrades.items():
        ticker, soldTrades = item[0], item[1]
        boughtTrades = boughtStocksToTrades[ticker]

        fifo_single_ticker(soldTrades, boughtTrades)

        boughtStocksToTrades[ticker] = boughtTrades

    return boughtStocksToTrades


#
# param soldTrades: deque
# param boughtTrades: deque
#
def fifo_single_ticker(soldTrades, boughtTrades):
    if len(soldTrades) == 0:
        return;

    soldTrade, boughtTrade = soldTrades.pop(), boughtTrades.pop()
    q_s, q_b = int(soldTrade["Quantity"]), int(boughtTrade["Quantity"])

    if q_s > q_b:
        soldTrade["Quantity"] = str(q_s - q_b)
        soldTrades.append(soldTrade)
    elif q_s < q_b:
        boughtTrade["Quantity"] = str(q_b - q_s)
        boughtTrades.append(boughtTrade)

    return fifo_single_ticker(soldTrades, boughtTrades)

if __name__ == "__main__":
    histReader = __import__("histreader")
    trades = histReader.readHistoryFile("history.txt")
    print(getSellLimit(trades, processBloombergPolicy))
