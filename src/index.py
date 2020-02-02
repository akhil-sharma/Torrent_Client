from torrent import Torrent
from network import connect_with_tracker

if __name__ == "__main__":
    new_torrent = Torrent()
    new_torrent.load_from_file("D:\Practice\Projects\Torrent_Client\Ford v Ferrari (2019) [1080p] [BluRay] [5.1] [YTS.LT].torrent")
    # new_torrent.load_from_file("D:\Practice\Projects\Torrent_Client\\01-CS50x_2018-52da574b6412862e199abeaea63e51bf8cea2140.torrent")
    print(new_torrent.info.files)