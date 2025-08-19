from functools import wraps
from flask import jsonify, request, session

def require_db_connection(f):
    """Decorator to check database connection"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"[Decorator] require_db_connection called for {f.__name__}")
        print(f"[Decorator] Request method: {request.method}")
        print(f"[Decorator] Session keys: {list(session.keys())}")
        print(f"[Decorator] Session content: {dict(session)}")
        
        if request.method == 'OPTIONS':
            print("[Decorator] Allowing OPTIONS request")
            return '', 200
            
        if 'db_config' not in session:
            print("[Decorator] ERROR: No db_config in session - database connection required")
            return jsonify({'error': 'Database connection required'}), 401
            
        print(f"[Decorator] Database config found in session: {session.get('db_config')}")
        print(f"[Decorator] Proceeding to call {f.__name__}")
        return f(*args, **kwargs)
    return decorated_function