import hashlib
import uuid

def generate_sha1_hash(data):
    hash_function = hashlib.sha1()
    hash_function.update(data)
    return hash_function.digest()

def generate_unique_id(root=None, id_length=20):
    random_string = str(uuid.uuid1())
    if root:
        return root[0:5] + random_string[0: id_length-len(root[0:5])]
    else:
        return random_string[0: id_length]

if __name__ == "__main__":
    print(generate_unique_id('akhil sharma'))
