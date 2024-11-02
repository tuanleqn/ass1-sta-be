# from flask import current_app, g
import os
import uuid
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client['myVirtualDatabase']
peer_collection = db['peer']
torrent_collection = db['torrent']

def add_peer(peer_name, password, status, ip_address, port):
    peer_id = str(uuid.uuid4())  # Tạo peer_id duy nhất
    peer_data = {
        "peer_id": peer_id,
        "peer_name": peer_name,
        "password": password,
        "status": status,
        "ip_address": ip_address,
        "port": port
    }
    try:
        peer_collection.insert_one(peer_data)
        print("Peer added successfully with peer_id:", peer_id)
        return peer_data['peer_id']
    except Exception as e:
        print(f"Error adding peer: {e}")

def attach_torrent_file_to_peer(peer_id, file_path):
    with open(file_path, 'r') as file:
        text_content = file.read()
    
    result = peer_collection.update_one(
        {'peer_id': peer_id},
        {'$set': {'text_content': text_content}}
    )
    
    if result.matched_count > 0:
        print("File attached successfully.")
    else:
        print("No peer found with the given peer_id.")

def get_torrent_file_content_by_peer_id(peer_id):
    peer = peer_collection.find_one({'peer_id': peer_id}, {'text_content': 1})
    if peer and 'text_content' in peer:
        print("File content retrieved successfully.")
        return peer['text_content']
    else:
        print("No content found for the given peer_id.")
        return None

def get_peer_by_id(peer_id):
    peer = peer_collection.find_one({'peer_id': peer_id})
    if peer:
        print("Peer information retrieved successfully.")
        return peer
    else:
        print("No peer found for the given peer_id.")
        return None

def update_peer_status(peer_id, new_status):
    result = peer_collection.update_one(
        {'peer_id': peer_id},
        {'$set': {'status': new_status}}
    )
    
    if result.matched_count > 0:
        print("Peer status updated successfully.")
    else:
        print("No peer found with the given peer_id.")

def delete_peer(peer_id):
    result = peer_collection.delete_one({'peer_id': peer_id})
    if result.deleted_count > 0:
        print("Peer deleted successfully.")
    else:
        print("No peer found with the given peer_id.")

def get_all_peers():
    peers = list(peer_collection.find({}))
    if peers:
        print(f"Retrieved {len(peers)} peers.")
        return peers
    else:
        print("No peers found.")
        return []

def is_peer_active(peer_id):
    peer = peer_collection.find_one({'peer_id': peer_id}, {'status': 1})
    if peer and peer['status'] in ['leeching', 'seeding']:
        print(f"Peer {peer_id} is active.")
        return True
    else:
        print(f"Peer {peer_id} is not active.")
        return False

def add_torrent(torrent_name, peer_ip, peer_port, file_path):
    torrent_id = str(uuid.uuid4())
    with open(file_path, 'r') as file:
        text_content = file.read()
    torrent_data = {
        "torrent_id": torrent_id,
        "torrent_name": torrent_name,
        "peer_ip": peer_ip,
        "peer_port": peer_port,
        "text_content": text_content
    }
    try:
        torrent_collection.insert_one(torrent_data)
        print("Torrent added successfully with torrent_id:", torrent_id)
        return torrent_data['torrent_id']
    except Exception as e:
        print(f"Error adding torrent: {e}")

def get_all_torrents_file_content():
    torrents = list(torrent_collection.find({}, {'text_content': 1}))
    if torrents:
        print(f"Retrieved content for {len(torrents)} torrents.")
        return torrents
    else:
        print("No torrents found.")
        return []

def delete_all_torrents():
    result = torrent_collection.delete_many({})
    print(f"{result.deleted_count} torrents deleted successfully.")