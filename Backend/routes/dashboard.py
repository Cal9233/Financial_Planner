from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models.transaction import Transaction
from models.account import Account
from models.category import Category
from models.budget import Budget
from models.goal import FinancialGoal
from utils.decorators import require_db_connection

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/summary', methods=['GET', 'OPTIONS'])
@jwt_required()
@require_db_connection
def get_dashboard_summary():
    """Get dashboard summary data"""
    print(f"[Dashboard] /summary endpoint hit - Method: {request.method}")
    if request.method == 'OPTIONS':
        print("[Dashboard] Handling OPTIONS request")
        return '', 200
    
    try:
        user_id = int(get_jwt_identity())
        print(f"[Dashboard] User ID from JWT: {user_id}")
        
        # Get transaction summary for current month
        today = datetime.now()
        start_of_month = datetime(today.year, today.month, 1)
        print(f"[Dashboard] Date range: {start_of_month} to {today}")
        
        summary = Transaction.get_summary_for_period(user_id, start_of_month, today)
        print(f"[Dashboard] Summary data retrieved: {summary}")
        
        response_data = {
            'total_income': summary.get('total_income', 0),
            'total_expenses': summary.get('total_expenses', 0),
            'net_income': summary.get('net_income', 0),
            'transaction_count': summary.get('transaction_count', 0)
        }
        print(f"[Dashboard] Sending response: {response_data}")
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"[Dashboard] Error in /summary: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/recent-transactions', methods=['GET', 'OPTIONS'])
@jwt_required()
@require_db_connection
def get_recent_transactions():
    """Get recent transactions for dashboard"""
    print(f"[Dashboard] /recent-transactions endpoint hit - Method: {request.method}")
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = int(get_jwt_identity())
        limit = request.args.get('limit', 5, type=int)
        print(f"[Dashboard] Getting recent transactions for user {user_id}, limit: {limit}")
        
        transactions = Transaction.get_recent_transactions(user_id, limit=limit)
        print(f"[Dashboard] Retrieved {len(transactions) if transactions else 0} transactions")
        
        return jsonify({
            'transactions': transactions
        }), 200
        
    except Exception as e:
        print(f"[Dashboard] Error in /recent-transactions: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/spending-by-category', methods=['GET', 'OPTIONS'])
@jwt_required()
@require_db_connection
def get_spending_by_category():
    """Get spending breakdown by category"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = int(get_jwt_identity())
        period = request.args.get('period', 'month')
        
        spending = Transaction.get_spending_by_category(user_id, period)
        
        return jsonify({
            'categories': spending
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/transactions/summary', methods=['GET', 'OPTIONS'])
@jwt_required()
@require_db_connection
def get_transaction_summary():
    """Get transaction summary for dashboard"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = int(get_jwt_identity())
        period = request.args.get('period', 'month')
        
        summary = Transaction.get_transaction_summary(user_id, period)
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

