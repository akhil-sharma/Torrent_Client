import hashlib

def generate_sha1_hash(data):
    hash_function = hashlib.sha1()
    hash_function.update(data)
    return hash_function.digest()