class File:
    def __init__(self, file_dict):
        self.file_length = file_dict.get(b'length', 0)
        self.file_path = [x.decode() for x in file_dict.get(b'path')]

    def __str__(self):
        return f'  File \n   Length : {self.file_length} \n   path {"/".join(self.file_path)} \n'


class TorrentInfo:
    def __init__(self, info_dict):
        self.piece_length = info_dict.get(b'piece length', 0)
        self.pieces       = info_dict.get(b'pieces', b'')
        self.private      = info_dict.get(b'private', b'0').decode()
        self.name         = info_dict.get(b'name', b'').decode()
        
        if info_dict.get(b'files'):
            self.multi_file = True # multi file torrent
            self.files = []
            for file_dict in info_dict.get(b'files'):
                self.files.append(File(file_dict))
        else:
            self.multi_file = False #single file torrent
            self.file_length = info_dict.get(b'length')

    def __str__(self):
        info_string = f'\n multi_file: {self.multi_file} \n piece_length: {self.piece_length} \n private: {self.private} \n'
        if self.multi_file:
            final_string = info_string + f' directory_name: {self.name} \n' + "".join([str(single_file) for single_file in self.files])
        else:
            final_string = info_string + f' file_name: {self.name} \n' + f' length: {self.file_length}'          
        return final_string


class TorrentMetaData:
    def __init__(self, torrent_meta_dict):      
        self.info           = TorrentInfo(torrent_meta_dict.get(b'info')) 
        self.announce       = torrent_meta_dict.get(b'announce', b'').decode()
        self.announce_list  = self.decode_announce_list(torrent_meta_dict.get(b'announce-list', [[]]))
        self.creation_date  = torrent_meta_dict.get(b'creation date', '') 
        self.comment        = torrent_meta_dict.get(b'comment', b'').decode()
        self.created_by     = torrent_meta_dict.get(b'created by', b'').decode()
        self.encoding       = torrent_meta_dict.get(b'encoding', b'').decode()

    def __str__(self):
        return f'info: {str(self.info)} \nannounce: {self.announce} \nannounce_list: {self.announce_list} \ncreation_date: {self.creation_date} \ncomment: {self.comment} \ncreated_by: {self.created_by} \nencoding: {self.encoding}'

    def decode_announce_list(self, b_announce_list):
        return [[link.decode() for link in link_list] for link_list in b_announce_list]

    def get_total_file_size(self):
        if self.info.multi_file:
            files_list = self.info.files
            size = 0
            for single_file in files_list:
                size += single_file.file_length
            return size
        else:
            return self.info.file_length
