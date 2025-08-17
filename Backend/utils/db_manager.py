import pymysql
from flask import session, g
from functools import wraps
import hashlib
import json

class DatabaseManager:
    """Manages dynamic database connections based on user credentials"""
    
    @staticmethod
    def create_connection_string(host, user, password, database, port=3306):
        """Create a SQLAlchemy connection string"""
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    
    @staticmethod
    def test_connection(host, user, password, database, port=3306):
        """Test if database connection is valid"""
        try:
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            connection.close()
            return True, "Connection successful"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_connection_hash(host, user, password, database, port):
        """Generate a unique hash for connection credentials"""
        conn_str = f"{host}:{port}:{user}:{password}:{database}"
        return hashlib.sha256(conn_str.encode()).hexdigest()
    
    @staticmethod
    def store_connection_info(host, user, password, database, port=3306):
        """Store connection info in session"""
        session['db_config'] = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port
        }
        session['db_connected'] = True
        session.permanent = True
    
    @staticmethod
    def get_connection_info():
        """Get connection info from session"""
        return session.get('db_config')
    
    @staticmethod
    def clear_connection_info():
        """Clear connection info from session"""
        session.pop('db_config', None)
        session.pop('db_connected', None)
    
    @staticmethod
    def is_connected():
        """Check if database connection info exists in session"""
        return session.get('db_connected', False)

def require_db_connection(f):
    """Decorator to ensure database connection exists"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request
        # Skip database check for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return '', 200
        if not DatabaseManager.is_connected():
            return {'error': 'Database connection required'}, 401
        return f(*args, **kwargs)
    return decorated_function