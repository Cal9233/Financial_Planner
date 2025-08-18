from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transaction import Transaction
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transactions_bp.route('', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_transactions():
    """Get all transactions for the current user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get filter parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        category_id = request.args.get('category_id', type=int)
        account_id = request.args.get('account_id', type=int)
        transaction_type = request.args.get('type')
        
        transactions = Transaction.get_by_user(
            user_id,
            page=page,
            per_page=per_page,
            start_date=start_date,
            end_date=end_date,
            category_id=category_id,
            account_id=account_id,
            transaction_type=transaction_type
        )
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions['items']],
            'total': transactions['total'],
            'page': transactions['page'],
            'per_page': transactions['per_page'],
            'total_pages': transactions['total_pages']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction():
    """Create a new transaction"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['amount', 'transaction_type', 'category_id', 'account_id', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create transaction
        transaction = Transaction(
            user_id=user_id,
            amount=float(data['amount']),
            transaction_type=data['transaction_type'],
            category_id=data['category_id'],
            account_id=data['account_id'],
            date=data['date'],
            description=data.get('description', ''),
            is_recurring=data.get('is_recurring', False),
            recurring_frequency=data.get('recurring_frequency')
        )
        
        transaction.save()
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<int:id>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_transaction(id):
    """Get a specific transaction"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        transaction = Transaction.find_by_id(id)
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        if transaction.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({'transaction': transaction.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_transaction(id):
    """Update a transaction"""
    try:
        user_id = get_jwt_identity()
        transaction = Transaction.find_by_id(id)
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        if transaction.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Update fields
        if 'amount' in data:
            transaction.amount = float(data['amount'])
        if 'transaction_type' in data:
            transaction.transaction_type = data['transaction_type']
        if 'category_id' in data:
            transaction.category_id = data['category_id']
        if 'account_id' in data:
            transaction.account_id = data['account_id']
        if 'date' in data:
            transaction.date = data['date']
        if 'description' in data:
            transaction.description = data['description']
        if 'is_recurring' in data:
            transaction.is_recurring = data['is_recurring']
        if 'recurring_frequency' in data:
            transaction.recurring_frequency = data['recurring_frequency']
        
        transaction.save()
        
        return jsonify({
            'message': 'Transaction updated successfully',
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(id):
    """Delete a transaction"""
    try:
        user_id = get_jwt_identity()
        transaction = Transaction.find_by_id(id)
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        if transaction.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        transaction.delete()
        
        return jsonify({'message': 'Transaction deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500