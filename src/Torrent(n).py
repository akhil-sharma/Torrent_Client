'''
Reads a torrent file and stores the
necessary information present in it.
'''
from pathlib import Path

from bencode import bdecode

class Torrent:
    def __init__(self) -> None:
        pass

    def _load_from_file(self, torrent_file_path: str):
        file = open(Path(torrent_file_path), mode='rb').read()
        file_contents = bdecode(file)

        
