import json
from odoo import http
from odoo.http import request
import logging
from werkzeug.security import generate_password_hash,check_password_hash

# Configure logging
_logger = logging.getLogger(__name__)

class UserController(http.Controller):
    
    @http.route('/hello_world', type='json', auth='public', methods=['POST'], csrf=False)
    def hello_world(self, **kwargs):
        return "Hello, World from Odoo!"
    
    @http.route('/test', type='json', auth='public', methods=['POST'], csrf=False)
    def test_data(self, **kwargs):
        # Dummy data array
        data = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
            {"id": 4, "name": "David", "email": "david@example.com"},
            {"id": 5, "name": "Eve", "email": "eve@example.com"},
        ]
        return data

    @http.route('/airplanes', type='json', auth='public', methods=['GET'], csrf=False)
    def get_airplanes(self, **kwargs):
        # Dummy airplane data
        airplanes = [
            {"id": 1, "model": "Boeing 737", "airline": "Airways A", "capacity": 200},
            {"id": 2, "model": "Airbus A320", "airline": "Airways B", "capacity": 180},
            {"id": 3, "model": "Boeing 777", "airline": "Airways C", "capacity": 350},
            {"id": 4, "model": "Airbus A380", "airline": "Airways D", "capacity": 500},
            {"id": 5, "model": "Boeing 787", "airline": "Airways E", "capacity": 250},
        ]
        return {"data" :airplanes}
    
    @http.route('/api/user/register', type='json', auth='public', methods=['POST'], csrf=False)
    def register_user(self, **kwargs):
        # Ambil data JSON dari permintaan
        post_data = request.httprequest.data
        post = json.loads(post_data)  # Ubah data menjadi JSON

        # Ambil data dari post
        name = post.get('name')
        email = post.get('email')
        password = post.get('password')
        phone = post.get('phone', False)
        groups = post.get('groups', [])

        # Validasi field yang dibutuhkan
        if not name or not email or not password:
            return {'status': 'error', 'message': 'Missing required fields: name, email, password'}

        # Cek apakah pengguna sudah ada
        existing_user = request.env['custom.user'].sudo().search([('login', '=', email)], limit=1)
        if existing_user:
            return {'status': 'error', 'message': 'Email is already registered'}

        try:
            # Membuat pengguna baru
            user = request.env['custom.user'].sudo().create({
                'name': name,
                'login': email,
                'password': generate_password_hash(password),  # Hash password
                'phone': phone,
                'groups_id': [(6, 0, groups)],
            })
            return {'status': 'success', 'message': 'User registered successfully', 'user_id': user.id}
        except Exception as e:
            _logger.error("Error creating user: %s", str(e))
            return {'status': 'error', 'message': str(e)}


    @http.route('/api/user/update', type='json', auth='public', methods=['POST'], csrf=False)
    def update_user(self, **kwargs):
        # Ambil data JSON dari permintaan
        post_data = request.httprequest.data
        post = json.loads(post_data)  # Ubah data menjadi JSON

        # Ambil data dari post
        user_id = post.get('user_id')
        name = post.get('name')
        email = post.get('email')
        password = post.get('password')
        phone = post.get('phone', False)
        groups = post.get('groups', [])

        # Validasi field yang dibutuhkan
        if not user_id:
            return {'status': 'error', 'message': 'Missing required field: user_id'}

        # Cek apakah pengguna ada
        user = request.env['custom.user'].sudo().search([('id', '=', user_id)], limit=1)
        if not user:
            return {'status': 'error', 'message': 'User not found'}

        try:
            # Update informasi pengguna
            if name:
                user.name = name
            if email:
                user.login = email
            if password:
                user.password = generate_password_hash(password)  # Hash password
            if phone:
                user.phone = phone
            if groups:
                user.groups_id = [(6, 0, groups)]

            return {'status': 'success', 'message': 'User updated successfully', 'user_id': user.id}
        except Exception as e:
            _logger.error("Error updating user: %s", str(e))
            return {'status': 'error', 'message': str(e)}


    @http.route('/api/user/login', type='json', auth='public', methods=['POST'], csrf=False)
    def login_user(self, **kwargs):
        # Ambil data JSON dari permintaan
        post_data = request.httprequest.data
        post = json.loads(post_data)  # Ubah data menjadi JSON

        # Ambil data dari post
        email = post.get('email')
        password = post.get('password')

        # Validasi field yang dibutuhkan
        if not email or not password:
            return {'status': 'error', 'message': 'Missing required fields: email, password'}

        # Cek apakah pengguna ada
        user = request.env['custom.user'].sudo().search([('login', '=', email)], limit=1)
        if not user or not check_password_hash(user.password, password):
            return {'status': 'error', 'message': 'Invalid email or password'}

        # Jika berhasil login, simpan id pengguna di session
        request.session.uid = user.id

        return {
            'status': 'success',
            'message': 'User logged in successfully',
            'user_id': user.id,
            'user_name': user.name,
        }

