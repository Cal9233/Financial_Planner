from flask import Blueprint, request, jsonify, session
from utils.db_manager import DatabaseManager
from config.dynamic_config import init_dynamic_db, get_dynamic_db
import pymysql

database_bp = Blueprint('database', __name__, url_prefix='/api/database')

@database_bp.route('/connect', methods=['POST'])
def connect_database():
    """Connect to MySQL database with provided credentials"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['host', 'user', 'password', 'database']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        host = data['host']
        user = data['user']
        password = data['password']
        database = data['database']
        port = data.get('port', 3306)
        
        # Test connection
        success, message = DatabaseManager.test_connection(host, user, password, database, port)
        
        if not success:
            return jsonify({
                'error': 'Connection failed',
                'message': message
            }), 400
        
        # Store connection info in session
        DatabaseManager.store_connection_info(host, user, password, database, port)
        
        # Initialize database with new connection
        from flask import current_app
        init_dynamic_db(current_app)
        
        return jsonify({
            'message': 'Database connected successfully',
            'connected': True,
            'database': database
        }), 200
        
    except Exception as e:
        import traceback
        error_details = {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }
        print(f"\nDatabase connection error: {error_details}")
        return jsonify(error_details), 500

@database_bp.route('/disconnect', methods=['POST'])
def disconnect_database():
    """Disconnect from current database"""
    try:
        DatabaseManager.clear_connection_info()
        
        return jsonify({
            'message': 'Database disconnected successfully',
            'connected': False
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@database_bp.route('/status', methods=['GET'])
def database_status():
    """Check database connection status"""
    try:
        is_connected = DatabaseManager.is_connected()
        conn_info = DatabaseManager.get_connection_info()
        
        response = {
            'connected': is_connected
        }
        
        if is_connected and conn_info:
            response['database'] = conn_info.get('database')
            response['host'] = conn_info.get('host')
            response['user'] = conn_info.get('user')
            
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@database_bp.route('/test', methods=['POST'])
def test_connection():
    """Test database connection without saving"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['host', 'user', 'password', 'database']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        host = data['host']
        user = data['user']
        password = data['password']
        database = data['database']
        port = data.get('port', 3306)
        
        # Test connection
        success, message = DatabaseManager.test_connection(host, user, password, database, port)
        
        if success:
            # Check if database has the required schema
            try:
                connection = pymysql.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=port
                )
                cursor = connection.cursor()
                
                # Check for required tables
                required_tables = ['Users', 'Categories', 'Accounts', 'Transactions', 
                                 'Budgets', 'Financial_Goals', 'Transaction_Splits']
                
                cursor.execute("SHOW TABLES")
                existing_tables = [table[0] for table in cursor.fetchall()]
                
                missing_tables = [table for table in required_tables if table not in existing_tables]
                
                cursor.close()
                connection.close()
                
                if missing_tables:
                    return jsonify({
                        'success': True,
                        'message': 'Connection successful but schema incomplete',
                        'missing_tables': missing_tables,
                        'schema_valid': False
                    }), 200
                else:
                    return jsonify({
                        'success': True,
                        'message': 'Connection successful and schema valid',
                        'schema_valid': True
                    }), 200
                    
            except Exception as e:
                return jsonify({
                    'success': True,
                    'message': 'Connection successful but could not verify schema',
                    'error': str(e),
                    'schema_valid': False
                }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500