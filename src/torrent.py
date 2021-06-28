from bencode import bencode, bdecode
from pathlib import Path
import logging
from helpers import generate_sha1_hash, generate_unique_id
from math import ceil

class TorrentInfo:
    def __init__(self, info_dict):
        self.info_dict    = info_dict
        self.piece_length = info_dict.get(b'piece length', 0)
        self.pieces       = info_dict.get(b'pieces', b'')
        self.private      = info_dict.get(b'private', b'0')
        self.name         = info_dict.get(b'name')
        self.total_length = 0 #lenght of a single file or the sum of all files.
        self.files        = [] #list of dictionaries containing file details
        self.multi_file   = None
        self.init_files()

    def init_files(self):
        root = Path(self.name.decode())
        if b'files' in self.info_dict:
            if not root.exists():
                Path.mkdir(root)
            
            for file in self.info_dict.get(b'files'):
                file_path = Path("/".join([x.decode() for x in file.get(b'path')]))
                self.files.append({"file_path" : root / file_path, "length" : file.get(b'length')})
                self.total_length += file.get(b'length')
        else:
            self.files.append({"file_path" : root, "length" : self.info_dict.get(b'length')})
            self.total_length = self.info_dict.get(b'length')

class Torrent:
    def __init__(self):
        self.torrent_file = None
        self.peer_id = None
        self.info_hash = None
        self.info = None
        self.file_list = None
        self.announce_list = None
        self.creation_data = None
        self.comment = None
        self.created_by = None
        self.encoding = 'utf-8'

    def load_from_file(self, file_path):
        file = open(Path(file_path), mode='rb').read()
        file_contents = bdecode(file)

        self.torrent_file = file_contents
        self.peer_id = generate_unique_id('-AS0001-')
        self.info = TorrentInfo(self.torrent_file.get(b'info'))
        self.announce_list = self.get_trakers()
        self.creation_data = self.torrent_file.get(b'creation date')
        self.comment = self.torrent_file.get(b'comment')
        self.created_by = self.torrent_file.get(b'created by')
        self.info_hash = generate_sha1_hash(bencode(self.torrent_file.get(b'info')))
        if b'encoding' in self.torrent_file:
            self.encoding = self.torrent_file.get(b'encoding')
        
        logging.debug(self.announce_list)

        assert(self.info.total_length > 0)
        assert(len(self.info.files) > 0)
    
    def get_trakers(self):
        if b'announce-list' in self.torrent_file:
            return self.torrent_file.get(b'announce-list')
        else:
            return [[self.torrent_file.get(b'announce')]]

    def get_total_file_size(self):
        return self.info.total_length

    def get_total_piece_count(self):
        if self.info.piece_length == 0:
            return 0
        return ceil(self.info.total_length / self.info.piece_length)

