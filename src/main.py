import argparse
from Torrent import Torrent
import logging

parser = argparse.ArgumentParser()
parser.add_argument("torrent_file_path", help="Location of the .torrent file")
parser.add_argument("-d", "--destination", help="Destination of the downloaded files.")

args = parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    torrent = Torrent(args.torrent_file_path, args.destination)
