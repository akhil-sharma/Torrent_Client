from bencode import bencode, bdecode
from models.torrent_information import TorrentMetaData
from helpers import generate_sha1_hash, generate_unique_id
from network import connect_with_tracker;

if __name__ == "__main__":
    PEER_ID = generate_unique_id('Akhil')
    PORT = 6883
    UPLOADED = 0
    DOWNLOADED = 0

    # data = open("../ubuntu-18.04.3-desktop-amd64.iso.torrent", mode='rb').read()
    # data = open("../big-buck-bunny.torrent", mode='rb').read()
    data = open("../2015_fall_psets_1_hacker1_hacker1.pdf.torrent", mode='rb').read()
    
    torrent = bdecode(data)
    info_hash = generate_sha1_hash(bencode(torrent.get(b'info')))
    print(info_hash)

    file_content = TorrentMetaData(torrent)
    print(file_content.get_total_file_size())
    print(file_content)

    LEFT = file_content.get_total_file_size()
    COMPACT = "1"
    EVENT="started"

    print(connect_with_tracker(file_content.announce, {
        "peer_id" : PEER_ID,
        "info_hash" : info_hash,
        "port" : PORT,
        "uploaded" : UPLOADED,
        "downloaded" : DOWNLOADED,
        "left" : file_content.get_total_file_size(),
        "compact" : COMPACT,
        "event" : EVENT
    }))