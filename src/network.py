import requests

def connect_with_tracker(base_url, payload):
    print(base_url, payload)
    response = requests.get(base_url, params=payload)
    return response.text

def reserve_port_for_torrent():
    pass
