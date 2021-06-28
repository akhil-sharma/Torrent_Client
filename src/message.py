from struct import pack, unpack
import random
import socket
import constants

class Message:
    def to_bytes(self):
        raise NotImplementedError()

    def from_bytes(self):
        raise NotImplementedError()

class UdpTrackerConnection(Message):
    """
    CONNECTING

    int64_t	connection_id  0x41727101980 for identifying protocol
    int32_t	action	       0 for a connection request
    int32_t	transaction_id Randomized by client.
    """
    def __init__(self):
        super(UdpTrackerConnection, self).__init__()
        self.conn_id = pack('>Q', 0x41727101980)
        self.action = pack('>I', 0)
        self.trans_id = pack('>I', random.randint(0, 100000))

    def to_bytes(self):
        return self.conn_id + self.action + self.trans_id

    def from_bytes(self, payload):
        self.conn_id, = unpack('>Q', payload[0:8])
        self.action, = unpack('>I', payload[8:12])
        self.trans_id, = unpack('>I', payload[12:])

class UdpTrackerAnnounce(Message):
    """
    ANNOUNCING

    int64_t	    connection_id	The connection id acquired from establishing the connection.
    int32_t	    action	        in this case, 1 for announce
    int32_t	    transaction_id	Randomized by client.
    int8_t[20]	info_hash	    The info-hash of the torrent you want announce yourself in.
    int8_t[20]	peer_id	        Your peer id.
    int64_t	    downloaded	    The number of byte you've downloaded in this session.
    int64_t	    left	        The number of bytes you have left to download until you're finished.
    int64_t	    uploaded	    The number of bytes you have uploaded in this session.
    int32_t	    event
                    none      = 0
                    completed = 1
                    started   = 2
                    stopped   = 3
    uint32_t	ip	Your ip address. Set to 0 if you want the tracker to use the sender of this UDP packet.
    uint32_t	key	A unique key that is randomized by the client.
    int32_t	    num_want	The maximum number of peers you want in the reply. Use -1 for default.
    uint16_t	port	The port you're listening on.
    """

    def __init__(self, peer_id, info_hash, conn_id):
        super(UdpTrackerAnnounce, self).__init__()
        self.peer_id = peer_id
        self.info_hash = info_hash
        self.conn_id = conn_id
        self.trans_id = pack('>I', random.randint(0, 100000))
        self.action = pack('>I', 1)

    def to_bytes(self):
        conn_id = pack('>Q', self.conn_id)
        action = self.action
        trans_id = self.trans_id
        event = pack('>I', 0)  
        downloaded = pack('>Q', 0) 
        left = pack('>Q', 0)	       
        uploaded = pack('>Q', 0)
        num_want = pack('>i', -1)
        ip = pack('>I', 0)
        key = pack('>I', 0)
        port = pack('>h', 8000)
        
        message = (conn_id + action + trans_id + self.info_hash + self.peer_id + downloaded + 
                    left + uploaded + event + ip + key + num_want + port)
        return message

    def from_bytes(self):
        pass


class UdpTrackerAnnounceResponse:
    """
    RESPONSE TO ANNOUNCE

    int32_t	action	        1 for announce 0
    int32_t	transaction_id	trans_id in Announce 4
    int32_t	interval	    Seconds till next re-announcing. 8
    int32_t	leechers	    The number 12
    int32_t	seeders	        The number 16
    32-bit integer IP address
    16-bit integer TCP port
    """
    def __init__(self):
        self.action = None
        self.trans_id = None
        self.interval = None
        self.leachers = None
        self.seeders = None
        self.address_list = []

    def from_bytes(self, payload):
        self.action = unpack('>I', payload[:4])
        self.trans_id = unpack('>I', payload[4:8])
        self.interval = unpack('>I', payload[8:12])
        self.leachers = unpack('>I', payload[12:16])
        self.seeders = unpack('>I', payload[16:20])
        self.address_list = self._parse_socket_addresses(payload[20:])

    def to_bytes(self):
        pass

    def _parse_socket_addresses(self, payload):
        # <ip 4-bytes><port 2-bytes> = 6 bytes
        socket_address_list = []

        for i in range(int(len(payload) / 6)):
            start_index = i
            end_index = i + 6
            ip = socket.inet_ntoa(payload[start_index: (end_index-2)])
            raw_port = payload[(end_index - 2): end_index]
            port = raw_port[1] + raw_port[0] * 256

            socket_address_list.append((ip, port))
        return socket_address_list
    

class Handshake(Message):
    """
        handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
                    1-byte   19-bytes 8-bytes 20-bytes 20-bytes
    """
    total_length = 68 #1 + 19 + 8 + 20 + 20

    def __init__(self, info_hash, peer_id):
        super(Handshake, self).__init__()

        assert len(info_hash) == 20
        assert len(peer_id) == 20
        self.peer_id = peer_id
        self.info_hash = info_hash

    def to_bytes(self):
        reserved = b'\x00' * 8 #8 bytes zeros
        handshake = pack(F'>B{constants.HANDSHAKE_PSTR_LEN}s8s20s20s',
                         constants.HANDSHAKE_PSTR_LEN,
                         constants.HANDSHAKE_PSTR_V1,
                         reserved,
                         self.info_hash,
                         self.peer_id)
        return handshake

    @classmethod
    def from_bytes(cls, payload):
        pstrlen = unpack('>B', payload[:1])
        pstr, reserved, info_hash, peer_id = unpack(F'>{constants.HANDSHAKE_PSTR_LEN}s8s20s20s', payload[1:cls.total_length])

        if pstr != constants.HANDSHAKE_PSTR_V1:
            raise ValueError("Invalid handshake protocol")

        return Handshake(info_hash, peer_id)
    
# Other Messages

class KeepAlive(Message):
    """
    keep-alive: <len=0000> 4-bytes
    """
    payload_length = 0
    total_length = 4

    def __init__(self):
        super(KeepAlive, self).__init__()

    @classmethod
    def to_bytes(cls, payload):
        return pack('>I', cls.payload_length)
    
    @classmethod
    def from_bytes(cls, payload):
        payload_length = unpack('>I', payload[:cls.total_length])

        if payload_length != 0:
            raise Exception("Not a keep-alive Message")

        return KeepAlive()
        

class Choke(Message):
    """
    choke: <len=0001><id=0> 4-bytes + 1-byte
    """
    payload_length = 1
    message_id = 0
    total_length = 5

    def __init__(self):
        super(Choke, self).__init__()
    
    @classmethod
    def to_bytes(cls):
        return pack('>IB', cls.payload_length, cls.message_id)
    
    @classmethod
    def from_bytes(cls, payload):
        payload_length, message_id = unpack(F'>IB', payload[:cls.total_length])
        if message_id != cls.message_id:
            raise Exception('Not a choke message.')

        return Choke()

class UnChoke(Message):
    """
    choke: <len=0001><id=0> 4-bytes + 1-byte
    """
    payload_length = 1
    message_id = 1
    total_length = 5

    def __init__(self):
        super(UnChoke, self).__init__()

    @classmethod
    def to_bytes(cls):
        return pack('>IB', cls.payload_length, cls.message_id)
    
    @classmethod
    def from_bytes(cls, payload):
        payload_length, message_id = unpack('>IB', payload[:cls.total_length])
        if message_id != cls.message_id:
            raise Exception('Not an unchoke message.')

        return UnChoke()

class Interested(Message):
    """
    interested: <len=0001><id=2>
    """
    payload_length = 1
    message_id = 2
    total_length = 5

    def __init__(self):
        super(Interested, self).__init__()

    @classmethod
    def to_bytes(cls):
        return pack('IB', cls.payload_length, cls.message_id)
            
    @classmethod
    def from_bytes(cls, payload):
        payload_length, message_id = unpack('>IB', payload[:cls.payload_length])
        if message_id != cls.message_id:
            raise Exception("Not an Interested message.")

        return Interested()

class NotInterested(Message):
    """
    not interested: <len=0001><id=3>
    """
    payload_length = 1
    message_id = 2
    total_length = 5

    def __init__(self):
        super(NotInterested, self).__init__()

    @classmethod
    def to_bytes(cls):
        return pack('>IB', cls.payload_length, cls.message_id)
    
    @classmethod
    def from_bytes(cls, payload):
        payload_length, message_id = unpack('>IB', payload[:cls.total_length])
        if message_id != cls.message_id:
            raise Exception("Not a Not-Interested message.")
        
        return NotInterested()

class Have(Message):
    """
    have: <len=0005><id=4><piece index> 4-bytes + 1-byte + 4-bytes
    """
    payload_length = 5
    message_id = 4
    total_length = 4 + payload_length


    def __init__(self, piece_index):
        super(Have, self).__init__()
        self.piece_index = piece_index

    def to_bytes(self):
        return pack('>IBI', self.payload_length, self.message_id ,self.piece_index)
    
    @classmethod
    def from_bytes(cls, payload):
        payload_length, message_id, piece_index = unpack('>IBI', payload[:cls.total_length])
        if message_id != cls.message_id:
            raise Exception("Not a Have message.")
        
        return Have(piece_index)

class BitField(Message): #bitfield is a bitarray
    """
    bitfield: <len=0001+X><id=5><bitfield>
    """
    def __init__(self):
        super(BitField, self).__init__()

    @classmethod
    def to_bytes(cls):
        pass
    
    @classmethod
    def from_bytes(cls, payload):
        pass

class Request(Message):
    """
    bitfield: <len=0001+X><id=5><bitfield>
    """
    def __init__(self):
        super(Request, self).__init__()

    @classmethod
    def to_bytes(cls):
        pass
    
    @classmethod
    def from_bytes(cls, payload):
        pass

class Piece(Message):
    """
    bitfield: <len=0001+X><id=5><bitfield>
    """
    def __init__(self):
        super(Piece, self).__init__()

    @classmethod
    def to_bytes(cls):
        pass
    
    @classmethod
    def from_bytes(cls, payload):
        pass

class Cancel(Message):
    """
    bitfield: <len=0001+X><id=5><bitfield>
    """
    def __init__(self):
        super(Cancel, self).__init__()

    @classmethod
    def to_bytes(cls):
        pass
    
    @classmethod
    def from_bytes(cls, payload):
        pass

class Port(Message):
    """
    bitfield: <len=0001+X><id=5><bitfield>
    """
    def __init__(self):
        super(Port, self).__init__()

    @classmethod
    def to_bytes(cls):
        pass
    
    @classmethod
    def from_bytes(cls, payload):
        pass



        

        

