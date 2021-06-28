import argparse
from Torrent(n) import Torrent

parser = argparse.ArgumentParser()
parser.add_argument("torrent-file-path", help="Location of the .torrent file", type="str")
parser.add_argument("-d", "--destination", help="Destination of the downloaded files.", type="str")

args = parser.parse_args()

if not args.destination:
    pass