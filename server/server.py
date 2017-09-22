import sys
sys.path.insert(0, "../")

import main
import os
from io import StringIO
from flask import request

from flask import Flask, url_for, send_from_directory
app = Flask(__name__)

cmdHandlers = {
    "u"     :  main.updateHistory,
    "update":  main.updateHistory,
    "r"     :  main.showReminder,
    "remind":  main.showReminder,
    "l"     :  main.listRecords,
    "list"  :  main.listRecords
}

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, '../image'), 'terminal.ico')

@app.route("/list")
def listRecordsRP():

    output = StringIO()
    startupParms = { "historyFile": "../history.txt", "outputStream": output }

    cmdHandlers["list"](**startupParms)
    return output.getvalue()


@app.route("/remind")
def remindSellLimitRP():

    output = StringIO()
    startupParms = { "historyFile": "../history.txt", "outputStream": output }

    # requests arguments
    if request.args.get("d") != None:
        startupParms["detail"] = ""

    cmdHandlers["remind"](**startupParms)
    return output.getvalue()


@app.route("/update")
def updateHistoryRP():

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
