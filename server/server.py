import sys
sys.path.insert(0, '../')

import main
from io import StringIO
from flask import request

from flask import Flask
app = Flask(__name__)

cmdHandlers = {
    "u"     :  main.updateHistory,
    "update":  main.updateHistory,
    "r"     :  main.showReminder,
    "remind":  main.showReminder,
    "l"     :  main.listRecords,
    "list"  :  main.listRecords
}

@app.route("/list")
def listRecordsRP():
    sys.argv.pop(0)

    output = StringIO()
    startupParms = { "historyFile": "../history.txt", "outputStream": output }

    cmdHandlers["list"](**startupParms)
    return output.getvalue()


@app.route("/remind")
def remindSellLimitRP():
    sys.argv.pop(0)

    output = StringIO()
    startupParms = { "historyFile": "../history.txt", "outputStream": output }

    cmdHandlers["remind"](**startupParms)
    return output.getvalue()


@app.route("/update")
def updateHistoryRP():
    sys.argv.pop(0)

    output = StringIO()
    startupParms = { "historyFile": "../history.txt", "outputStream": output }

    # request arguments
    startupParms["action"]   = request.args.get("a")
    startupParms["date"]     = request.args.get("d")
    startupParms["quantity"] = request.args.get("q")
    startupParms["ticker"]   = request.args.get("t")
    startupParms["value"]    = request.args.get("v")


    cmdHandlers["update"](**startupParms)
    return output.getvalue()
