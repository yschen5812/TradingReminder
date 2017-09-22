def calculateTotalInvest(trades):
    return round(sum(list(getInvestSummary(trades).values())), 2)

def cacluateTotalProfit(trades):
    pass


# helper function
def getInvestSummary(trades):
    result = {}
    for item in trades:
        action, ticker, quantity, value = item["Action"], item["Ticker"], item["Quantity"], item["Value"]
        transaction = int(quantity) * float(value) * (-1 if action == "buy" else 1)
        if not ticker in result:
            result[ticker] = 0
        result[ticker] += transaction
    return result
