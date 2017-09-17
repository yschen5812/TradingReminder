columnWidth = 30

columnNames = [ "Action", "Date", "Quantity", "Ticker", "Value" ]

def writeTitle(filename, **kargs):
    width = columnWidth
    if columnWidth in kargs:
        width = kargs["columnWidth"]

    rowFormatVec = ["{{{}:^{}}}".format(i, width) for i in range(5)]
    title = "|".join(rowFormatVec).format(*columnNames)
    f = open(filename, "w")
    f.write(title + "\n")


def writeDataRow(filename, **kargs):
    for check in columnNames:
       if not check in kargs:
            raise Exception({"reason": "No {}".format(check)})

    width = columnWidth
    if columnWidth in kargs:
        width = kargs["columnWidth"]

    rowFormatVec = ["{{{}:^{}}}".format(i, width) for i in range(5)]
    rowData = "|".join(rowFormatVec).format(
        kargs["Action"], kargs["Date"], kargs["Quantity"], kargs["Ticker"], kargs["Value"])

    f = open(filename, "a")
    f.write(rowData + "\n")

def copyFrom(fromFilename, toFilename, **kargs):
    width = columnWidth
    if columnWidth in kargs:
        width = columnWidth
    histreader = __import__("histreader")
    history = histreader.readHistoryFile(fromFilename, plaintext=True)
    writeTitle(toFilename)
    for record in history:
        action, date, ticker, value, quantity = record["Action"], record["Date"], record["Ticker"], record["Value"], record["Quantity"]
        writeDataRow(toFilename, Action=action, Date=date, Ticker=ticker, Value=value, Quantity=quantity, columnWidth=width)


if __name__ == "__main__":
    #writeTitle("test.txt", columnWidth=30)
    #writeDataRow("test.txt", Action="sell", Date="08/21/2019", Ticker="DIX", Value=30.4, Quantity=19, columnWidth=30)
    copyFrom("history.txt", "test.txt")
