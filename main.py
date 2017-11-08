#!/usr/bin/python3
import sys
import parser
import writehistory
import histreader
import policy
import color as Color
import util
from datetime import datetime
from collections import OrderedDict

columnWidth = 30
defaultHistoryFile = "history.txt"

def updateHistory(**kargs):
    print("updating...", kargs)

    if "fromCmd" in kargs:
        args = kargs["fromCmd"]
    else:
        args = kargs

    histFilename = defaultHistoryFile if not "historyFile" in args else args["historyFile"]
    outputStream = sys.stdout if not "outputStream" in args else args["outputStream"]
    printOptions = {
        "file": outputStream,
        "end": "<br>" if "outputStream" in args else "\n"
    }

    action, date, quantity, ticker, value = args["action"], args["date"], args["quantity"], args["ticker"], args["value"]
    writehistory.writeDataRow(histFilename, Action=action, Date=date, Quantity=quantity, Ticker=ticker, Value=value)

    print("Success!", printOptions)

def showReminder(**kargs):
    print("reminding...", kargs)
    print("\n\n")

    if "fromCmd" in kargs:
        args = kargs["fromCmd"]
        if "detail" in args and not args["detail"]:
            del args["detail"]
    else:
        args = kargs

    histFilename = defaultHistoryFile if not "historyFile" in args else args["historyFile"]
    outputStream = sys.stdout if not "outputStream" in args else args["outputStream"]
    printOptions = {
        "file": outputStream,
        "end": "<br>" if "outputStream" in args else "\n"
    }
    color = Color.disabled() if "outputStream" in args else Color
    trades = histreader.readHistoryFile(histFilename)
    result = policy.getSellLimit(trades, policy.processBloombergPolicy)

    numRecords = len(result["no sell limit"])

    result["no sell limit"] = OrderedDict(sorted(result["no sell limit"].items(), key=lambda i:i[0]))
    for idx, item in enumerate(result["no sell limit"].items()):
        if idx == 0:
            print("{0:=^50}".format(" No Sell Limit Holdings "), **printOptions)
        idxFormatStr = "{{0:>{}d}}".format(numRecords)
        print("    " , (idxFormatStr + ") Ticker: '" + color.R + "{1}" + color.W + "',  Quantity: " + color.Y + "{2}" + color.W).format(idx, item[0], item[1]), **printOptions)

        if idx == numRecords-1:
            print(**printOptions)

    result["limited"] = OrderedDict(sorted(result["limited"].items(), key=lambda i:i[0]))
    for idx, item in enumerate(result["limited"].items()):
        numRecords = len(str(len(result["limited"])))
        if idx == 0:
            print("{0:=^50}".format(" Limited Holdings "), **printOptions)
        idxFormatStr = "{{0:<{}}}".format(numRecords+1) # + ")"
        print("    ", (idxFormatStr + " Ticker: '" + color.R + "{1}" + color.W + "':").format(str(idx)+")", item[0]), **printOptions)
        numRecords = len(item[1])
        for subidx, limitedItem in enumerate(reversed(item[1])):
            idxFormatStr = "{{0:>{}}}".format(numRecords + 1) # + "."
            printStr = "        " + (idxFormatStr + "  Sell Limit at: " + color.G + "{1}" + color.W + ", Quantity: " + color.Y + "{2}" + color.W).format("i"*(subidx+1)+".", limitedItem["limit"], limitedItem["quantity"])
            if "detail" in args:
                daysToLift = (limitedItem["date"] - datetime.now().date()).days + 30
                spaceStr = "{{0:>{}d}}".format(80 - len(printStr))
                printStr += (spaceStr + " days left").format(daysToLift)
            print(printStr, **printOptions)

    print(**printOptions)

    if "detail" in args:
        # show full information
        trades = histreader.readHistoryFile(histFilename)
        totalInvest = util.calculateTotalInvest(trades)
        print("Total investment amount: ${}".format(totalInvest), **printOptions)

def listRecords(**kargs):
    print("listing...", kargs)

    if "fromCmd" in kargs:
        args = kargs["fromCmd"]
    else:
        args = kargs

    histFilename = defaultHistoryFile if not "historyFile" in args else args["historyFile"]
    outputStream = sys.stdout if not "outputStream" in args else args["outputStream"]
    printOptions = {
        "file": outputStream,
        "end": "<br>" if "outputStream" in args else "\n"
    }

    # for now just show readin object
    hist = histreader.readHistoryFile(histFilename, plaintext=True)
    title = []
    if len(hist) > 0:
        title = sorted(hist[0].keys())

    title.append("Total")

    # Print title with reserved width for the line number
    lineNumberWidth = len(str(len(hist) + 1)) + 1
    strFormatList = ["{{{}:^{}}}".format(idx, columnWidth + lineNumberWidth) if idx == 0 else "{{{}:^{}}}".format(idx, columnWidth) for idx in range(len(title))]
    print("|".join(strFormatList).format(*tuple(title)), **printOptions)

    # Print records
    for idx, item in enumerate(hist):
        strFormatList = ["{{{}:^{}}}".format(idx, columnWidth) for idx in range(len(title))]
        strValueList = [round(int(item["Quantity"])*float(item["Value"]), 2) if key == "Total" else item[key] for key in title]
        lineNumberStr = "{})".format(idx+1)
        lineNumberFormat = "{{0:>{}}}".format(lineNumberWidth)
        print(lineNumberFormat.format(lineNumberStr) + "|".join(strFormatList).format(*strValueList), **printOptions)

if __name__ == "__main__":
    sys.argv.pop(0)

    startupParms = parser.parseCmdArgs(sys.argv)

    cmdHandlers = {
        "u"     :  updateHistory,
        "update":  updateHistory,
        "r"     :  showReminder,
        "remind":  showReminder,
        "l"     :  listRecords,
        "list"  :  listRecords
    }

    if startupParms == None:
        print("Failed to parser arguments. Abort")
        sys.exit(-1)

    if startupParms.topic in cmdHandlers:
        cmdHandlers[startupParms.topic](fromCmd=vars(startupParms))

    else:
        print("Invalid startupParms:", startupParms)
        sys.exit(-2)

