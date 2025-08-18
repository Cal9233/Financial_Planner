from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models.transaction import Transaction
from models.account import Account
from models.category import Category
from models.budget import Budget
from models.goal import FinancialGoal

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/summary', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_dashboard_summary():
    """Get dashboard summary data"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        
        # Get transaction summary for current month
        today = datetime.now()
        start_of_month = datetime(today.year, today.month, 1)
        
        summary = Transaction.get_summary_for_period(user_id, start_of_month, today)
        
        return jsonify({
            'total_income': summary.get('total_income', 0),
            'total_expenses': summary.get('total_expenses', 0),
            'net_income': summary.get('net_income', 0),
            'transaction_count': summary.get('transaction_count', 0)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/recent-transactions', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_recent_transactions():
    """Get recent transactions for dashboard"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 5, type=int)
        
        transactions = Transaction.get_recent_transactions(user_id, limit=limit)
        
        return jsonify({
            'transactions': transactions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/spending-by-category', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_spending_by_category():
    """Get spending breakdown by category"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        period = request.args.get('period', 'month')
        
        spending = Transaction.get_spending_by_category(user_id, period)
        
        return jsonify({
            'categories': spending
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/transactions/summary', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_transaction_summary():
    """Get transaction summary for dashboard"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        period = request.args.get('period', 'month')
        
        summary = Transaction.get_transaction_summary(user_id, period)
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

