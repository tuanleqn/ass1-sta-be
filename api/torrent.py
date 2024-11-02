from flask import Blueprint, request, jsonify
from flask_cors import CORS
from db import *

torrent_api = Blueprint('torrent_api', 'torrent_api', url_prefix='/api/torrent')
CORS(torrent_api)

''' @ torrent api docs
POST /api/torrent/add: Thêm một torrent mới. Dữ liệu yêu cầu: torrent_name, file_path, peer_ip, peer_port.
GET /api/torrent/content: Lấy nội dung của tất cả các torrent.
GET /api/torrent/delete: Xóa tất cả các torrent.
'''

@torrent_api.route('/add', methods=['POST'])
def add_torrent_api():
    data = request.get_json()
    torrent_name = data.get('torrent_name')
    peer_ip = data.get('peer_ip')
    peer_port = data.get('peer_port')
    file_path = data.get('file_path')

    if not all([torrent_name, peer_ip, peer_port, file_path]):
        return jsonify({"error": "Missing required fields"}), 400

    torrent_id = add_torrent(torrent_name, peer_ip, peer_port, file_path)
    return jsonify(torrent_id), 201

@torrent_api.route('/content', methods=['GET'])
def get_all_torrent_content():
    torrents = get_all_torrents_file_content()
    for torrent in torrents:
        torrent['_id'] = str(torrent['_id'])
    return jsonify(torrents), 200

@torrent_api.route('/delete', methods=['DELETE'])
def delete_all_torrents_file():
    delete_all_torrents()
    return jsonify({"message": "All torrents deleted successfully."}), 200