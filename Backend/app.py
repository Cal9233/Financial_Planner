from flask import Flask, jsonify, session, g
from flask_cors import CORS
from datetime import datetime, timedelta
import os

from config import jwt
from config.config import config
from config.dynamic_config import init_dynamic_db, get_dynamic_db, close_db_session
from utils.db_manager import DatabaseManager

# Import routes
from routes import (
    auth_bp, users_bp, categories_bp, accounts_bp,
    transactions_bp, budgets_bp, goals_bp, reports_bp
)
from routes.database import database_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Use simple session instead of filesystem
    # This avoids the bytes/string issue with flask-session
    app.config['SESSION_COOKIE_NAME'] = 'pfm_session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    
    # Initialize JWT
    jwt.init_app(app)
    
    # Configure CORS with credentials
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Register database blueprint first (doesn't require auth)
    app.register_blueprint(database_bp)
    
    # Initialize database if connection info exists
    @app.before_request
    def before_request():
        # Make session permanent
        session.permanent = True
        
        # Only initialize if not already done
        if DatabaseManager.is_connected() and not hasattr(g, 'db_initialized'):
            init_dynamic_db(app)
            g.db = get_dynamic_db()
            g.db_initialized = True
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_db_session()
    
    # Register other blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(budgets_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(reports_bp)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token has expired',
            'message': 'The token has expired. Please login again.'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Invalid token',
            'message': 'Signature verification failed.'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Authorization required',
            'message': 'Request does not contain an access token.'
        }), 401
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Personal Finance Management API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'users': '/api/users',
                'database': '/api/database',
                'categories': '/api/categories',
                'accounts': '/api/accounts',
                'transactions': '/api/transactions',
                'budgets': '/api/budgets',
                'goals': '/api/goals',
                'reports': '/api/reports'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        # Don't rollback if db.session doesn't exist
        if hasattr(g, 'db') and g.db:
            g.db.session.rollback()
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print("Starting Flask app WITHOUT filesystem sessions")
    print("This should avoid the bytes/string TypeError")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)