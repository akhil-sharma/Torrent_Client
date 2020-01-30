from bencode import bencode, bdecode
from models.torrent_information import *

if __name__ == "__main__":
    data = open("../ubuntu-18.04.3-desktop-amd64.iso.torrent", mode='rb').read()
    torrent = bdecode(data)
    print(TorrentMetaData(torrent))