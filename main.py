import sys
import parser
import histreader
import policy
import color


columnWidth = 30

def updateHistory(args):
    print("updating...", args)
    return

def showRemider(args):
    print("reminding...", args)
    print("\n\n")
    trades = histreader.readHistoryFile("history.txt")
    result = policy.getSellLimit(trades, policy.processBloombergPolicy)

    numRecords = len(result["no sell limit"])
    for idx, item in enumerate(result["no sell limit"].items()):
        if idx == 0:
            print("{0:=^50}".format(" No Sell Limit Holdings "))
        idxFormatStr = "{{0:>{}d}}".format(numRecords)
        print("    " , (idxFormatStr + ") Ticker: '" + color.R + "{1}" + color.W + "',  Quantity: " + color.Y + "{2}" + color.W).format(idx, item[0], item[1]))

        if idx == numRecords-1:
            print("\n")

    numRecords = len(result["limited"])
    for idx, item in enumerate(result["limited"].items()):
        if idx == 0:
            print("{0:=^50}".format(" Limited Holdings "))
        idxFormatStr = "{{0:>{}d}}".format(numRecords)
        print("    ", (idxFormatStr + ") Ticker: '" + color.R + "{1}" + color.W + "':").format(idx, item[0]))
        numRecords = len(item[1])
        for subidx, limitedItem in enumerate(reversed(item[1])):
            idxFormatStr = "{{0:>{}}}".format(numRecords)
            print("        ", (idxFormatStr + ".  Sell Limit at: " + color.G + "{1}" + color.W + ", Quantity: " + color.Y + "{2}" + color.W).format("i"*(subidx+1), limitedItem["limit"], limitedItem["quantity"]))

    print("\n")

def listRecords(args):
    print("listing...", args)

    # for now just show readin object
    hist = histreader.readHistoryFile("history.txt", plaintext=True)
    title = []
    if len(hist) > 0:
        title = sorted(hist[0].keys())

    # Print title with reserved width for the line number
    lineNumberWidth = len(str(len(hist) + 1)) + 1
    strFormatList = ["{{{}:^{}}}".format(idx, columnWidth + lineNumberWidth) if idx == 0 else "{{{}:^{}}}".format(idx, columnWidth) for idx in range(len(title))]
    print("|".join(strFormatList).format(*tuple(title)))

    # Print records
    for idx, item in enumerate(hist):
        strFormatList = ["{{{}:^{}}}".format(idx, columnWidth) for idx in range(len(title))]
        strValueList = [item[key] for key in title]
        lineNumberStr = "{})".format(idx+1)
        lineNumberFormat = "{{0:>{}}}".format(lineNumberWidth)
        print(lineNumberFormat.format(lineNumberStr) + "|".join(strFormatList).format(*strValueList))

if __name__ == "__main__":
    sys.argv.pop(0)

    startupParms = parser.parseCmdArgs(sys.argv)

    cmdHandlers = {
        "u"     :  updateHistory,
        "update":  updateHistory,
        "r"     :  showRemider,
        "remind":  showRemider,
        "l"     :  listRecords,
        "list"  :  listRecords
    }

    if startupParms == None:
        print("Failed to parser arguments. Abort")
        sys.exit(-1)

    if startupParms.topic in cmdHandlers:
        cmdHandlers[startupParms.topic](startupParms)

    else:
        print("Invalid startupParms:", startupParms)
        sys.exit(-2)

