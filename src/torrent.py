'''
Reads a torrent file and stores the
necessary information present in it.
'''
from os import PathLike
from pathlib import Path
from math import ceil, log
import logging

from bencode import bdecode, bencode

from helpers import generate_sha1_hash, generate_unique_id

class Torrent:
    def __init__(self, torrent_file_path: str, destination: str = None) -> None:
        self.total_length = 0
        self.files = []
        self._load_from_file(torrent_file_path)
        self._init_files(destination)
        logging.debug(self.get_files())
        logging.debug(self.get_total_file_size())
        logging.debug(self.get_total_piece_count())

    def _load_from_file(self, torrent_file_path: str):
        file = open(Path(torrent_file_path), mode='rb').read()
        file_contents = bdecode(file)
        self.peer_id = generate_unique_id('-AS0001-')
        self.info = file_contents[b'info']
        self.name = file_contents[b'info'][b'name']
        self.pieces = file_contents[b'info'][b'pieces']
        self.piece_length = file_contents[b'info'][b'piece length']
        self.announce_list = self._get_trackers(file_contents)
        self.info_hash = generate_sha1_hash(bencode(self.info))
        logging.debug(self.announce_list)        

    def _get_trackers(self, file_contents: dict) -> list:
        '''
        Returns the list of trackers mentions in the torrent file.
        '''
        if b'announce-list' in file_contents:
            return file_contents.get(b'announce-list')
        else:
            return [[file_contents.get(b'announce')]]

    def _init_files(self, dest: str):
        '''
        Creates the root directory for the files to be downloaded
        and populates the files list locations and sizes of the 
        individual files.
        '''
        root = Path(self.name.decode())
        if dest:
            destination = Path(dest)
            if not destination.exists():
                Path.mkdir(destination)
            
            root = Path(destination) / root
        
        if b'files' in self.info:
            if not root.exists():
                Path.mkdir(root)
            for file in self.info[b'files']:
                file_path = Path("/".join([x.decode() for x in file[b'path']]))
                self.files.append({"file_path": root / file_path, "length": file[b'length']})
                self.total_length += file[b'length']
        else:
            self.files.append({"file_path": root, "length": self.info[b'length']})
            self.total_length = self.info[b'length']

    def get_total_file_size(self):
        return self.total_length

    def get_total_piece_count(self):
        return ceil(self.total_length / self.piece_length)

    def get_files(self) -> list:
        return self.files

    def get_announce_list(self) -> list:
        return self.announce_list

    def __repr__(self) -> str:
        pass
