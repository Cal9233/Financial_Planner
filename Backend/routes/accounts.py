from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import Account

accounts_bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')

@accounts_bp.route('', methods=['GET'])
@jwt_required()
def get_accounts():
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        account_type = request.args.get('type')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        # Build query
        query = Account.query.filter_by(user_id=user_id)
        
        if active_only:
            query = query.filter_by(is_active=True)
            
        if account_type:
            query = query.filter_by(account_type=account_type)
        
        accounts = query.order_by(Account.account_type, Account.account_name).all()
        
        # Calculate total balance by type
        totals = {}
        for account in accounts:
            if account.account_type not in totals:
                totals[account.account_type] = 0
            totals[account.account_type] += float(account.balance)
        
        return jsonify({
            'accounts': [acc.to_dict() for acc in accounts],
            'totals': totals
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounts_bp.route('', methods=['POST'])
@jwt_required()
def create_account():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['account_name', 'account_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new account
        account = Account(
            user_id=user_id,
            account_name=data['account_name'],
            account_type=data['account_type'],
            balance=data.get('balance', 0.00),
            currency=data.get('currency', 'USD')
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify({
            'message': 'Account created successfully',
            'account': account.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@accounts_bp.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    try:
        user_id = get_jwt_identity()
        account = Account.query.filter_by(
            account_id=account_id,
            user_id=user_id
        ).first()
        
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['account_name', 'balance', 'currency', 'is_active']
        for field in allowed_fields:
            if field in data:
                setattr(account, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Account updated successfully',
            'account': account.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@accounts_bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    try:
        user_id = get_jwt_identity()
        account = Account.query.filter_by(
            account_id=account_id,
            user_id=user_id
        ).first()
        
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        # Soft delete by setting is_active to False
        account.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'Account deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500