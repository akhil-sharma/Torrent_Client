from bencode import bencode, bdecode
from models.torrent_information import TorrentMetaData
from helpers import generate_sha1_hash

if __name__ == "__main__":
    # data = open("../ubuntu-18.04.3-desktop-amd64.iso.torrent", mode='rb').read()
    data = open("../big-buck-bunny.torrent", mode='rb').read()
    torrent = bdecode(data)
    info_hash = generate_sha1_hash(bencode(torrent.get(b'info')))
    print(info_hash)
    file_content = TorrentMetaData(torrent)
    print(file_content.get_total_file_size())
    print(file_content)