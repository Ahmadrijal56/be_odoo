import logging
from odoo import http
from odoo.http import request
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
_logger = logging.getLogger(__name__)

class HelloWorldController(http.Controller):
    
    @http.route('/hello_world', type='json', auth='none', methods=['POST'], csrf=False)
    def hello_world(self, **kwargs):
        return "Hello, World from Odoo!"
    
    @http.route('/test', type='json', auth='none', methods=['POST'], csrf=False)
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

    @http.route('/airplanes', type='json', auth='none', methods=['GET'], csrf=False)
    def get_airplanes(self, **kwargs):
        # Dummy airplane data
        airplanes = [
            {"id": 1, "model": "Boeing 737", "airline": "Airways A", "capacity": 200},
            {"id": 2, "model": "Airbus A320", "airline": "Airways B", "capacity": 180},
            {"id": 3, "model": "Boeing 777", "airline": "Airways C", "capacity": 350},
            {"id": 4, "model": "Airbus A380", "airline": "Airways D", "capacity": 500},
            {"id": 5, "model": "Boeing 787", "airline": "Airways E", "capacity": 250},
        ]
        return airplanes

    @http.route('/api/user/register', type='json', auth='none', methods=['POST'], csrf=False)
    def register_user(self):
        post = request.jsonrequest
        name = post.get('name')
        email = post.get('email')
        password = post.get('password')
        phone = post.get('phone', False)
        groups = post.get('groups', [])

        # Validate required fields
        if not name or not email or not password:
            return {'status': 'error', 'message': 'Missing required fields: name, email, password'}

        # Check for existing user
        existing_user = request.env['custom.user'].sudo().search([('login', '=', email)], limit=1)
        if existing_user:
            return {'status': 'error', 'message': 'Email is already registered'}

        try:
            # Create new user
            user = request.env['custom.user'].sudo().create({
                'name': name,
                'login': email,
                'password': generate_password_hash(password),  # Hash the password
                'phone': phone,
                'groups_id': [(6, 0, groups)],
            })
            return {'status': 'success', 'message': 'User registered successfully', 'user_id': user.id}
        except Exception as e:
            _logger.error("Error creating user: %s", str(e))
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/user/update', type='json', auth='user', methods=['POST'], csrf=False)
    def update_user(self):
        post = request.jsonrequest
        _logger.info("Incoming request data for update: %s", post)

        user_id = post.get('user_id')
        name = post.get('name')
        email = post.get('email')
        password = post.get('password')
        phone = post.get('phone', False)
        groups = post.get('groups', [])

        if not user_id:
            return {'status': 'error', 'message': 'Missing required field: user_id'}

        # Check if user exists
        user = request.env['custom.user'].sudo().search([('id', '=', user_id)], limit=1)
        if not user:
            return {'status': 'error', 'message': 'User not found'}

        # Update user details
        try:
            if name:
                user.name = name
            if email:
                user.login = email
            if password:
                user.password = generate_password_hash(password)  # Hash the password
            if phone:
                user.phone = phone
            if groups:
                user.groups_id = [(6, 0, groups)]

            return {'status': 'success', 'message': 'User updated successfully', 'user_id': user.id}
        except Exception as e:
            _logger.error("Error updating user: %s", str(e))
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/user/login', type='json', auth='none', methods=['POST'], csrf=False)
    def login_user(self):
        post = request.jsonrequest
        _logger.info("Incoming request data for login: %s", post)

        email = post.get('email')
        password = post.get('password')

        if not email or not password:
            return {'status': 'error', 'message': 'Missing required fields: email, password'}

        # Authenticate the user
        user = request.env['custom.user'].sudo().search([('login', '=', email)], limit=1)
        if not user or not check_password_hash(user.password, password):
            return {'status': 'error', 'message': 'Invalid email or password'}

        # Create a session
        request.session.uid = user.id

        return {
            'status': 'success',
            'message': 'User logged in successfully',
            'user_id': user.id,
            'user_name': user.name,
        }
