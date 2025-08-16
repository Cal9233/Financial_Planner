from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from sqlalchemy import and_, extract
from config import db
from models import Transaction, Account, Category, TransactionSplit

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transactions_bp.route('', methods=['GET'])
@jwt_required()
def get_transactions():
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        account_id = request.args.get('account_id')
        category_id = request.args.get('category_id')
        transaction_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query - join with accounts to filter by user
        query = Transaction.query.join(Account).filter(Account.user_id == user_id)
        
        # Apply filters
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
            
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
            
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
            
        if start_date:
            query = query.filter(Transaction.transaction_date >= date.fromisoformat(start_date))
            
        if end_date:
            query = query.filter(Transaction.transaction_date <= date.fromisoformat(end_date))
        
        # Paginate results
        pagination = query.order_by(Transaction.transaction_date.desc(), Transaction.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        transactions = [trans.to_dict() for trans in pagination.items]
        
        return jsonify({
            'transactions': transactions,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['account_id', 'category_id', 'amount', 'transaction_date', 'transaction_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Verify account belongs to user
        account = Account.query.filter_by(
            account_id=data['account_id'],
            user_id=user_id
        ).first()
        
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        # Verify category belongs to user
        category = Category.query.filter_by(
            category_id=data['category_id'],
            user_id=user_id
        ).first()
        
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Create transaction
        transaction = Transaction(
            account_id=data['account_id'],
            category_id=data['category_id'],
            amount=data['amount'],
            description=data.get('description'),
            transaction_date=date.fromisoformat(data['transaction_date']),
            transaction_time=data.get('transaction_time', '12:00:00'),
            transaction_type=data['transaction_type'],
            status=data.get('status', 'completed'),
            notes=data.get('notes')
        )
        
        db.session.add(transaction)
        
        # Update account balance
        if transaction.status == 'completed':
            if transaction.transaction_type == 'income':
                account.balance += transaction.amount
            elif transaction.transaction_type == 'expense':
                account.balance -= abs(transaction.amount)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    try:
        user_id = get_jwt_identity()
        
        # Get transaction with user verification
        transaction = Transaction.query.join(Account).filter(
            Transaction.transaction_id == transaction_id,
            Account.user_id == user_id
        ).first()
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        data = request.get_json()
        old_amount = transaction.amount
        old_type = transaction.transaction_type
        old_status = transaction.status
        
        # Update allowed fields
        allowed_fields = ['amount', 'description', 'transaction_date', 'transaction_time', 
                         'transaction_type', 'status', 'notes']
        for field in allowed_fields:
            if field in data:
                if field == 'transaction_date':
                    setattr(transaction, field, date.fromisoformat(data[field]))
                else:
                    setattr(transaction, field, data[field])
        
        # Update account balance if amount, type, or status changed
        if (old_amount != transaction.amount or old_type != transaction.transaction_type 
            or old_status != transaction.status):
            
            account = transaction.account
            
            # Reverse old transaction
            if old_status == 'completed':
                if old_type == 'income':
                    account.balance -= old_amount
                elif old_type == 'expense':
                    account.balance += abs(old_amount)
            
            # Apply new transaction
            if transaction.status == 'completed':
                if transaction.transaction_type == 'income':
                    account.balance += transaction.amount
                elif transaction.transaction_type == 'expense':
                    account.balance -= abs(transaction.amount)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction updated successfully',
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    try:
        user_id = get_jwt_identity()
        
        # Get transaction with user verification
        transaction = Transaction.query.join(Account).filter(
            Transaction.transaction_id == transaction_id,
            Account.user_id == user_id
        ).first()
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        # Update account balance
        if transaction.status == 'completed':
            account = transaction.account
            if transaction.transaction_type == 'income':
                account.balance -= transaction.amount
            elif transaction.transaction_type == 'expense':
                account.balance += abs(transaction.amount)
        
        # Delete transaction (splits will be cascade deleted)
        db.session.delete(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_transaction_summary():
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))
        
        # Get transactions for the specified month
        transactions = Transaction.query.join(Account).filter(
            Account.user_id == user_id,
            extract('year', Transaction.transaction_date) == year,
            extract('month', Transaction.transaction_date) == month,
            Transaction.status == 'completed'
        ).all()
        
        # Calculate summary
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_expenses = sum(abs(t.amount) for t in transactions if t.transaction_type == 'expense')
        net_income = total_income - total_expenses
        
        # Group by category
        category_summary = {}
        for transaction in transactions:
            if transaction.category:
                cat_name = transaction.category.category_name
                cat_type = transaction.category.category_type
                
                if cat_name not in category_summary:
                    category_summary[cat_name] = {
                        'type': cat_type,
                        'total': 0,
                        'count': 0
                    }
                
                category_summary[cat_name]['total'] += abs(transaction.amount)
                category_summary[cat_name]['count'] += 1
        
        return jsonify({
            'year': year,
            'month': month,
            'total_income': float(total_income),
            'total_expenses': float(total_expenses),
            'net_income': float(net_income),
            'transaction_count': len(transactions),
            'category_summary': category_summary
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500