from flask import Blueprint, request, jsonify
from flask_cors import CORS
from db import client

test_api = Blueprint('test_api', 'test_api', url_prefix='/api/test')
CORS(test_api)

@test_api.route('/check-db', methods=['GET'])
def check_db():
    try:
        # Kiểm tra kết nối với MongoDB bằng lệnh ping
        client.admin.command('ping')
        return jsonify(message="Database is connected successfully"), 200
    except Exception as e:
        return jsonify(message="Failed to connect to the database", error=str(e)), 500
