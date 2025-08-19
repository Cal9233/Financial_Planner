from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime
from models.user import SimpleUser
from models.category import Category
from config.db import get_db_connection
from utils.decorators import require_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
@require_db_connection
def register():
    """Register a new user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        existing_user = SimpleUser.find_by_username(data['username'])
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        
        existing_email = SimpleUser.find_by_email(data['email'])
        if existing_email:
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = SimpleUser(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password'])
        
        # Save user
        user.save()
        
        # Create default categories for the new user
        Category.create_default_categories(user.user_id)
        
        # Create tokens (identity must be string)
        access_token = create_access_token(identity=str(user.user_id))
        refresh_token = create_refresh_token(identity=str(user.user_id))
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@require_db_connection
def login():
    """Login user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Find user by username or email
        user = SimpleUser.find_by_username(data['username'])
        if not user:
            user = SimpleUser.find_by_email(data['username'])
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Update last login
        user.update_last_login()
        
        # Create tokens (identity must be string)
        access_token = create_access_token(identity=str(user.user_id))
        refresh_token = create_refresh_token(identity=str(user.user_id))
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
@jwt_required(optional=True)
def logout():
    """Logout user"""
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/refresh', methods=['POST', 'OPTIONS'])
@jwt_required(refresh=True, optional=True)
def refresh():
    """Refresh access token"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Check if we have a valid refresh token
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'Invalid refresh token'}), 401
        
        access_token = create_access_token(identity=str(user_id))
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
@require_db_connection
def get_current_user():
    """Get current user info"""
    try:
        user_id = get_jwt_identity()
        user = SimpleUser.find_by_id(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500