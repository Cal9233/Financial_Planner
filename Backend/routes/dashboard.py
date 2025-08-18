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

# Account routes moved to accounts.py

# Budget performance route moved to budgets.py

# Goals routes moved to goals.py

# Categories routes moved to categories.py

# Additional endpoints for creating data

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

@dashboard_bp.route('/transactions/<int:transaction_id>', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_transaction(transaction_id):
    """Update a transaction"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Find the transaction
        transaction = Transaction.find_by_id(transaction_id, user_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        # Update fields
        if 'account_id' in data:
            transaction.account_id = data['account_id']
        if 'category_id' in data:
            transaction.category_id = data['category_id']
        if 'transaction_date' in data:
            transaction.transaction_date = data['transaction_date']
        if 'amount' in data:
            transaction.amount = data['amount']
        if 'transaction_type' in data:
            transaction.transaction_type = data['transaction_type']
        if 'description' in data:
            transaction.description = data['description']
        if 'reference_number' in data:
            transaction.reference_number = data['reference_number']
        if 'is_recurring' in data:
            transaction.is_recurring = data['is_recurring']
        
        # Save the transaction
        transaction.save()
        
        return jsonify({
            'message': 'Transaction updated successfully',
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/transactions/<int:transaction_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_transaction(transaction_id):
    """Delete a transaction"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        user_id = get_jwt_identity()
        
        # Find the transaction
        transaction = Transaction.find_by_id(transaction_id, user_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        # Delete the transaction
        transaction.delete()
        
        return jsonify({
            'message': 'Transaction deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500