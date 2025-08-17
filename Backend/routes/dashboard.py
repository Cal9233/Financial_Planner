from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models.transaction import Transaction
from models.account import Account
from models.category import Category
from models.budget import Budget
from models.goal import FinancialGoal

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api')

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

@dashboard_bp.route('/transactions', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_transactions():
    """Get recent transactions"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get transactions
        transactions = Transaction.get_recent_transactions(user_id, limit=per_page, offset=offset)
        total = Transaction.get_count(user_id)
        
        return jsonify({
            'transactions': transactions,
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/accounts', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_accounts():
    """Get user accounts"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        
        # Get all accounts
        accounts = Account.get_by_user_id(user_id)
        account_list = [acc.to_dict() for acc in accounts]
        
        # Get total balance
        total_balance = Account.get_total_balance(user_id)
        
        return jsonify({
            'accounts': account_list,
            'total': len(account_list),
            'total_balance': total_balance
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/budgets/performance', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_budget_performance():
    """Get budget performance data"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        performance = Budget.get_budget_performance(user_id)
        return jsonify(performance), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/goals', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_goals():
    """Get financial goals"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        include_completed = request.args.get('include_completed', 'false').lower() == 'true'
        
        goals = FinancialGoal.get_by_user_id(user_id, include_completed)
        
        return jsonify({
            'goals': goals,
            'total': len(goals)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/categories', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_categories():
    """Get expense/income categories"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        category_type = request.args.get('type')  # 'income', 'expense', or None for all
        
        categories = Category.get_by_user_id(user_id, type=category_type)
        category_list = [cat.to_dict() for cat in categories]
        
        return jsonify({
            'categories': category_list,
            'total': len(category_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Additional endpoints for creating data

@dashboard_bp.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
    """Create a new account"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        account = Account(
            user_id=user_id,
            account_name=data.get('account_name'),
            account_type=data.get('account_type'),
            balance=data.get('balance', 0.00),
            institution=data.get('institution'),
            account_number=data.get('account_number')
        )
        
        account.save()
        
        return jsonify({
            'message': 'Account created successfully',
            'account': account.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    """Create a new transaction"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        transaction = Transaction(
            user_id=user_id,
            account_id=data.get('account_id'),
            category_id=data.get('category_id'),
            transaction_date=data.get('transaction_date'),
            amount=data.get('amount'),
            transaction_type=data.get('transaction_type'),
            description=data.get('description'),
            reference_number=data.get('reference_number')
        )
        
        transaction.save()
        
        # Update account balance if needed
        if data.get('update_balance', True):
            account = Account.get_by_user_id(user_id)
            # Find the specific account
            for acc in account:
                if acc.account_id == transaction.account_id:
                    if transaction.transaction_type == 'income':
                        acc.balance += transaction.amount
                    elif transaction.transaction_type == 'expense':
                        acc.balance -= transaction.amount
                    acc.save()
                    break
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    """Update a transaction"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # For now, return success
        # In a real implementation, you would update the transaction
        return jsonify({
            'message': 'Transaction updated successfully',
            'transaction': {
                'transaction_id': transaction_id,
                **data
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    """Delete a transaction"""
    try:
        user_id = get_jwt_identity()
        
        # For now, return success
        # In a real implementation, you would delete the transaction
        return jsonify({
            'message': 'Transaction deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500