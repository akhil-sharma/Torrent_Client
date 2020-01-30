# from bencode import bencode, bdecode

# if __name__ == "__main__":
#     data = open("../ubuntu-18.04.3-desktop-amd64.iso.torrent", mode='rb').read()
#     torrent = bdecode(data)
#     print(torrent)


# class Name:
#     def __init__(self, fname, lname):
#         self.fname = fname
#         self.lname = lname
    
#     def __str__(self):
#         return self.fname + self.lname

# if __name__ == "__main__":
#     print(Name("akhil", "sharma"))

a = ['akhil', 'sharma']

print(f'My name is {" ".join(a)}')