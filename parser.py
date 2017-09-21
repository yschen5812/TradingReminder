import sys
import argparse


def parseCmdArgs(args):
    if len(args) == 0:
        print("Invalid arguments:", args)
        return

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="topic", help="sub-command help")

    # create a parser for 'Update' command
    parser_remind = subparsers.add_parser("update", aliases=["u"], help="The update mode. Insert new record.")
    parser_remind.add_argument(
        "-n",
        "--ticker",
        help="Ticker name",
        required=True)

    parser_remind.add_argument(
        "-v",
        "--value",
        type=float,
        required=True,
        help="Trade value")

    parser_remind.add_argument(
        "-m",
        "--amount",
        type=int,
        required=True,
        help="Trade amount")

    parser_remind.add_argument(
        "-t",
        "--tradetype",
        choices=["sell", "buy"],
        required=True,
        help="Trade type")

    parser_remind.add_argument(
        "-d",
        "--tradedate",
        required=True,
        help="Trade date")

    # create a parser for 'Remind' command
    parser_remind = subparsers.add_parser("remind", aliases=["r"], help="Show what stocks/equities and the amount are permitted to be sold.")
    parser_remind.add_argument(
        "-dt",
        "--detail",
        help="Detail mode",
        action="store_true")
    #group = parser_remind.add_mutually_exclusive_group(required=True)

    # create a parser for 'List' command
    parser_list = subparsers.add_parser("list", aliases=["l"], help="Display current holdings")
    parser_list.add_argument(
        "-hf",
        "--history",
        help="History filename")


    return parser.parse_args(args)


if __name__ == "__main__":
    sys.argv.pop(0)
    print(parseCmdArgs(sys.argv))

