from flask import Blueprint, request, jsonify
from flask_cors import CORS
from db import *

peer_api = Blueprint('peer_api', 'peer_api',url_prefix='/api/peer')
CORS(peer_api)

''' @ peer api docs
POST /api/peer/add: Thêm một peer mới. Dữ liệu yêu cầu: peer_name, password, status, ip_address, port.
GET /api/peer/<peer_id>: Lấy thông tin của một peer theo peer_id.
PUT /api/peer/<peer_id>/status: Cập nhật trạng thái của một peer. Dữ liệu yêu cầu: status.
DELETE /api/peer/<peer_id>: Xóa một peer theo peer_id.
GET /api/peer/: Lấy danh sách tất cả peer.
POST /api/peer/<peer_id>/attach: Đính kèm file vào peer. Dữ liệu yêu cầu: file_path.
GET /api/peer/<peer_id>/content: Lấy nội dung file đã đính kèm của một peer.
'''

@peer_api.route('/add', methods=['POST'])
def add_peer_api():
    data = request.get_json()
    peer_name = data.get('peer_name')
    password = data.get('password')
    status = data.get('status')
    ip_address = data.get('ip_address')
    port = data.get('port')
    
    if not all([peer_name, password, status, ip_address, port]):
        return jsonify({"error": "Missing required fields"}), 400

    peer_id = add_peer(peer_name, password, status, ip_address, port)
    return jsonify(peer_id), 201

@peer_api.route('/<peer_id>', methods=['GET'])
def get_peer(peer_id):
    peer = get_peer_by_id(peer_id)
    if peer:
        peer['_id'] = str(peer['_id'])
        return jsonify(peer), 200
    return jsonify({"error": "Peer not found"}), 404

@peer_api.route('/<peer_id>/status', methods=['PUT'])
def update_peer_status_api(peer_id):
    data = request.get_json()
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({"error": "Missing status"}), 400

    update_peer_status(peer_id, new_status)
    return jsonify({"message": "Peer status updated successfully."}), 200

@peer_api.route('/<peer_id>', methods=['DELETE'])
def delete_peer_api(peer_id):
    delete_peer(peer_id)
    return jsonify({"message": "Peer deleted successfully."}), 200

@peer_api.route('/', methods=['GET'])
def get_all_peers_api():
    peers_lists = get_all_peers()
    for peer in peers_lists:
        peer['_id'] = str(peer['_id'])
    return jsonify(peers_lists), 200

@peer_api.route('/<peer_id>/attach', methods=['POST'])
def attach_file_to_peer_api(peer_id):
    data = request.get_json()
    file_path = data.get('file_path')

    if not file_path:
        return jsonify({"error": "Missing file path"}), 400

    attach_torrent_file_to_peer(peer_id, file_path)
    return jsonify({"message": "File attached successfully."}), 200

@peer_api.route('/<peer_id>/content', methods=['GET'])
def get_peer_file_content_api(peer_id):
    content = get_torrent_file_content_by_peer_id(peer_id)
    if content:
        return jsonify({"content": content}), 200
    return jsonify({"error": "No content found for the given peer_id."}), 404
