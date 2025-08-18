from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.account import Account

accounts_bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')

@accounts_bp.route('', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_accounts():
    """Get all accounts for user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        accounts = Account.get_by_user_id(user_id)
        account_list = [acc.to_dict() for acc in accounts]
        total_balance = Account.get_total_balance(user_id)
        
        return jsonify({
            'accounts': account_list,
            'total': len(account_list),
            'total_balance': total_balance
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounts_bp.route('/<int:account_id>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_account(account_id):
    """Get specific account"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        accounts = Account.get_by_user_id(user_id)
        
        for acc in accounts:
            if acc.account_id == account_id:
                return jsonify({'account': acc.to_dict()}), 200
        
        return jsonify({'error': 'Account not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounts_bp.route('', methods=['POST'])
@jwt_required()
def create_account():
    """Create new account"""
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

@accounts_bp.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    """Update account"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        accounts = Account.get_by_user_id(user_id)
        
        for acc in accounts:
            if acc.account_id == account_id:
                # Update fields
                if 'account_name' in data:
                    acc.account_name = data['account_name']
                if 'account_type' in data:
                    acc.account_type = data['account_type']
                if 'balance' in data:
                    acc.balance = data['balance']
                if 'institution' in data:
                    acc.institution = data['institution']
                if 'account_number' in data:
                    acc.account_number = data['account_number']
                if 'is_active' in data:
                    acc.is_active = data['is_active']
                
                acc.save()
                
                return jsonify({
                    'message': 'Account updated successfully',
                    'account': acc.to_dict()
                }), 200
        
        return jsonify({'error': 'Account not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@accounts_bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    """Delete account (soft delete)"""
    try:
        user_id = get_jwt_identity()
        accounts = Account.get_by_user_id(user_id)
        
        for acc in accounts:
            if acc.account_id == account_id:
                acc.is_active = False
                acc.save()
                
                return jsonify({
                    'message': 'Account deleted successfully'
                }), 200
        
        return jsonify({'error': 'Account not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500