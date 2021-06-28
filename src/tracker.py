import requests
import logging
from bencode import bencode, bdecode
import socket
from urllib.parse import urlparse
from helpers import read_from_socket
from message import UdpTrackerConnection, UdpTrackerAnnounceResponse, UdpTrackerAnnounce

class SockAddr:
    def __init__(self, ip, port, allowed=True):
        self.ip = ip
        self.port = port
        self.allowed = allowed
    
    def __hash__(self):
        return "%s%d" % (self.ip, self.port)

class Tracker():
    def __init__(self, torrent):
        self.torrent = torrent
        self.connected_peers = {}
        self.dict_sock_addr = {}

    def get_peers_from_trackers(self):
        # for i, tracker in enumerate(self.torrent.announce_list):
        for tracker in self.torrent.announce_list:
            if tracker[0][:3] == b'udp':
                try:
                    ##
                    print(tracker[0])
                    self.udp_scrapper(tracker[0])
                except Exception as e:
                    print("Udp Scrapper Failed: ", str(e))

    def udp_scrapper(self, announce):
        torrent = self.torrent
        parsed = urlparse(announce)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(4)
        ip, port = socket.gethostbyname(parsed.hostname), parsed.port
        tracker_connection_input = UdpTrackerConnection()
        response = self.send_message((ip, port), sock, tracker_connection_input)
        if not response:
            raise Exception("No response for UdpTrackerConnection") 
        tracker_connection_output = UdpTrackerConnection()
        tracker_connection_output.from_bytes(response)

        tracker_announce_input = UdpTrackerAnnounce(torrent.peer_id, torrent.info_hash, 
                                    tracker_connection_output.conn_id)
        response = self.send_message((ip, port), sock, tracker_announce_input)

        if not response:
            raise Exception("No response for UdpTrackerAnnounce")
        
        tracker_announce_output = UdpTrackerAnnounceResponse()
        tracker_announce_output.from_bytes(response)

        for ip, port in tracker_announce_output.address_list:
            sock_addr = SockAddr(ip, port)

            if sock_addr.__hash__() not in self.dict_sock_addr:
                self.dict_sock_addr[sock_addr.__hash__()] = sock_addr

        print(F"Got {len(self.dict_sock_addr)} peers")
        print(self.dict_sock_addr)

    def send_message(self, conn, sock, tracker_message):
        message = tracker_message.to_bytes()
        trans_id = tracker_message.trans_id
        action = tracker_message.action
        size = len(message)

        sock.sendto(message, conn)

        try:
            # response = self.read_from_socket(sock)
            response = read_from_socket(sock)
        except socket.timeout as e:
            logging.debug("Timeout : %s" % e)
            return
        except Exception as e:
            logging.exception("Unexpected error when sending message : %s" % e.__str__())
            return

        if len(response) < size:
            logging.debug("Did not get full message.")

        if action != response[0:4] or trans_id != response[4:8]:
            logging.debug("Transaction or Action ID did not match")

        return response

