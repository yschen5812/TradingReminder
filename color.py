W  = '\033[0m'  # white (normal)
R  = '\033[1;31m' # red
G  = '\033[1;32m' # green
Y  = '\033[1;33m' # yellow
B  = '\033[1;34m' # blue
P  = '\033[1;35m' # purple

class disabled(object):
    def __init__(self):
        self.W = ""
        self.R = ""
        self.G = ""
        self.Y = ""
