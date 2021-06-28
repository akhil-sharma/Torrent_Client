import hashlib
import uuid
import socket
import logging

def generate_sha1_hash(data):
    hash_function = hashlib.sha1()
    hash_function.update(data)
    return hash_function.digest()

def generate_unique_id(root=None, id_length=20, allowed_root_length = 8):
    random_string = str(uuid.uuid1())
    if root:
        return bytes(root[0:allowed_root_length] + random_string[0: id_length - allowed_root_length], 'utf-8')
    else:
        return bytes(random_string[0: id_length], 'utf-8')

def read_from_socket(sock):
    data = b''
    while True:
        try:
            buff = sock.recv(4096)
            if len(buff) <= 0:
                break

            data += buff
        except socket.error as e:
            err = e.args[0]
            # if err != errno.EAGAIN or err != errno.EWOULDBLOCK:
            logging.debug("Wrong errno {}".format(err))
            break
        except Exception:
            logging.exception("Recv failed")
            break

    return data

if __name__ == "__main__":
    print(generate_unique_id('-AS0001-'))
