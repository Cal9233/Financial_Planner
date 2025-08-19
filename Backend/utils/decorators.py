from functools import wraps
from flask import jsonify, request, session

def require_db_connection(f):
    """Decorator to check database connection"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            return '', 200
        if 'db_config' not in session:
            return jsonify({'error': 'Database connection required'}), 401
        return f(*args, **kwargs)
    return decorated_function