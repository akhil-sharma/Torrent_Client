from bencode import bencode, bdecode
from helpers import generate_sha1_hash, generate_unique_id
from pathlib import Path

class File:
    def __init__(self, file_dict):
        self.file_length = file_dict.get(b'length')
        path_list = [x.decode() for x in file_dict.get(b'path')]
        self.file_path = Path("/".join(path_list))

class TorrentInfo:
    def __init__(self, info_dict):
        self.piece_length = info_dict.get(b'piece length', 0)
        self.pieces       = info_dict.get(b'pieces', b'')
        self.private      = info_dict.get(b'private', b'0')
        self.name         = info_dict.get(b'name', b'')

        if b'files' in info_dict:
            self.multi_file = True # multi file torrent
            self.files = []
            for file_dict in info_dict.get(b'files'):
                self.files.append(File(file_dict))
        else:
            self.multi_file = False #single file torrent
            self.file_length = info_dict.get(b'length')

class Torrent:
    def __init__(self):
        self.torrent_file = None
        self.peer_id = None
        self.info_hash = None
        self.info = None
        self.announce_list = None
        self.creation_data = None
        self.comment = None
        self.created_by = None
        self.encoding = 'utf-8'

    def load_from_file(self, file_path):
        file = open(Path(file_path), mode='rb').read()
        file_contents = bdecode(file)

        self.torrent_file = file_contents
        self.peer_id = generate_unique_id('Test')
        self.info = TorrentInfo(self.torrent_file.get(b'info'))
        self.announce_list = self.get_trakers()
        self.creation_data = self.torrent_file.get(b'creation date')
        self.comment = self.torrent_file.get(b'comment')
        self.created_by = self.torrent_file.get(b'created by')
        self.info_hash = generate_sha1_hash(bencode(self.torrent_file.get(b'info')))
        if b'encoding' in self.torrent_file:
            self.encoding = self.torrent_file.get(b'encoding')
        
    
    def get_trakers(self):
        if b'announce-list' in self.torrent_file:
            return self.torrent_file.get(b'announce-list')
        else:
            return [[self.torrent_file.get(b'announce')]]

    def get_total_file_size(self):
        if self.info.multi_file:
            return sum([file.file_length for file in self.file_list])
        else:
            return self.info.file_length


if __name__ == "__main__":
    new_torrent = Torrent()
    new_torrent.load_from_file("D:\Practice\Projects\Torrent_Client\Ford v Ferrari (2019) [1080p] [BluRay] [5.1] [YTS.LT].torrent")
    print(new_torrent.info_hash)
        