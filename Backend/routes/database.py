from flask import Blueprint, request, jsonify, session
from config.db import get_db_connection, init_db_tables, SimpleDBConnection
import mysql.connector

database_bp = Blueprint('database', __name__, url_prefix='/api/database')

@database_bp.route('/connect', methods=['POST', 'OPTIONS'])
def connect_database():
    """Connect to MySQL database with provided credentials"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['host', 'user', 'password', 'database']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Test connection
        test_db = SimpleDBConnection()
        success = test_db.connect(
            host=data.get('host', 'localhost'),
            user=data.get('user'),
            password=data.get('password'),
            database=data.get('database'),
            port=int(data.get('port', 3306))
        )
        
        if not success:
            return jsonify({
                'connected': False,
                'error': 'Failed to connect to database'
            }), 400
        
        # Store connection info in session
        session['db_config'] = {
            'host': data.get('host', 'localhost'),
            'user': data.get('user'),
            'password': data.get('password'),
            'database': data.get('database'),
            'port': int(data.get('port', 3306))
        }
        session['db_connected'] = True
        session.permanent = True
        
        # Initialize tables
        init_db_tables()
        
        # Close test connection
        test_db.close()
        
        return jsonify({
            'connected': True,
            'message': 'Successfully connected to database'
        }), 200
        
    except Exception as e:
        return jsonify({
            'connected': False,
            'error': str(e)
        }), 500

@database_bp.route('/disconnect', methods=['POST'])
def disconnect_database():
    """Disconnect from database"""
    try:
        # Clear session
        session.pop('db_config', None)
        session.pop('db_connected', None)
        
        # Close any existing connection
        db = get_db_connection()
        if db.connection:
            db.close()
        
        return jsonify({
            'connected': False,
            'message': 'Disconnected from database'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@database_bp.route('/status', methods=['GET', 'OPTIONS'])
def database_status():
    """Check database connection status"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        is_connected = session.get('db_connected', False)
        
        # Try to ping the database if we think we're connected
        if is_connected:
            db = get_db_connection()
            if db.connection:
                try:
                    db.connection.ping(reconnect=True)
                except:
                    is_connected = False
            else:
                is_connected = False
        
        return jsonify({
            'connected': is_connected,
            'database': session.get('db_config', {}).get('database') if is_connected else None
        }), 200
        
    except Exception as e:
        return jsonify({
            'connected': False,
            'error': str(e)
        }), 500

@database_bp.route('/test', methods=['POST'])
def test_connection():
    """Test database connection with provided credentials"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['host', 'user', 'password', 'database']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Test connection
        test_db = SimpleDBConnection()
        success = test_db.connect(
            host=data.get('host', 'localhost'),
            user=data.get('user'),
            password=data.get('password'),
            database=data.get('database'),
            port=int(data.get('port', 3306))
        )
        
        if success:
            # Check if tables exist
            test_db.execute("SHOW TABLES")
            tables = [row['Tables_in_' + data['database']] for row in test_db.fetchall()]
            
            required_tables = ['Users', 'Categories', 'Accounts', 'Transactions', 
                             'TransactionSplits', 'Budgets', 'FinancialGoals']
            missing_tables = [t for t in required_tables if t not in tables]
            
            test_db.close()
            
            return jsonify({
                'success': True,
                'message': 'Connection successful',
                'schema_valid': len(missing_tables) == 0,
                'missing_tables': missing_tables if missing_tables else None
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to connect to database'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500