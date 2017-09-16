from datetime import datetime

def readHistoryFile(filename, **kw):
    # Read in history.txt and insert into a list
    lines = [line.rstrip('\n') for line in open(filename)]


    # Remove title line
    title = [line.strip() for line in lines.pop(0).split("|")]

    # Transform to tuples
    def transform(lineStr):
        d = {}
        l = [line.strip() for line in lineStr.split("|")]
        for idx, item in enumerate(l):
            colName = title[idx]
            if "plaintext" in kw:
                d[title[idx]] = item
            else:
                d[title[idx]] = datetime.strptime(item, "%m/%d/%Y").date() if colName == "Date" else item
        return d


    objs = list(map(transform, lines))

    return objs;


if __name__ == "__main__":
    print(readHistoryFile("history.txt"))
