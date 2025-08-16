from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, datetime
from sqlalchemy import and_
from config import db
from models import Budget, Category, Transaction, Account

budgets_bp = Blueprint('budgets', __name__, url_prefix='/api/budgets')

@budgets_bp.route('', methods=['GET'])
@jwt_required()
def get_budgets():
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        period_type = request.args.get('period_type')
        
        # Build query
        query = Budget.query.filter_by(user_id=user_id)
        
        if active_only:
            query = query.filter_by(is_active=True)
            
        if period_type:
            query = query.filter_by(period_type=period_type)
        
        budgets = query.order_by(Budget.start_date.desc()).all()
        
        return jsonify({
            'budgets': [budget.to_dict() for budget in budgets]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@budgets_bp.route('', methods=['POST'])
@jwt_required()
def create_budget():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['category_id', 'budget_amount', 'period_type', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Verify category belongs to user
        category = Category.query.filter_by(
            category_id=data['category_id'],
            user_id=user_id
        ).first()
        
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Check for existing budget in the same period
        existing = Budget.query.filter_by(
            user_id=user_id,
            category_id=data['category_id'],
            start_date=date.fromisoformat(data['start_date']),
            end_date=date.fromisoformat(data['end_date'])
        ).first()
        
        if existing:
            return jsonify({'error': 'Budget already exists for this category and period'}), 400
        
        # Calculate spent amount for the period
        spent_amount = db.session.query(
            db.func.sum(db.func.abs(Transaction.amount))
        ).join(Account).filter(
            Account.user_id == user_id,
            Transaction.category_id == data['category_id'],
            Transaction.transaction_date >= date.fromisoformat(data['start_date']),
            Transaction.transaction_date <= date.fromisoformat(data['end_date']),
            Transaction.transaction_type == 'expense',
            Transaction.status == 'completed'
        ).scalar() or 0
        
        # Create budget
        budget = Budget(
            user_id=user_id,
            category_id=data['category_id'],
            budget_amount=data['budget_amount'],
            spent_amount=spent_amount,
            period_type=data['period_type'],
            start_date=date.fromisoformat(data['start_date']),
            end_date=date.fromisoformat(data['end_date'])
        )
        
        db.session.add(budget)
        db.session.commit()
        
        return jsonify({
            'message': 'Budget created successfully',
            'budget': budget.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@budgets_bp.route('/<int:budget_id>', methods=['PUT'])
@jwt_required()
def update_budget(budget_id):
    try:
        user_id = get_jwt_identity()
        budget = Budget.query.filter_by(
            budget_id=budget_id,
            user_id=user_id
        ).first()
        
        if not budget:
            return jsonify({'error': 'Budget not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['budget_amount', 'is_active']
        for field in allowed_fields:
            if field in data:
                setattr(budget, field, data[field])
        
        # If dates are being updated, recalculate spent amount
        if 'start_date' in data or 'end_date' in data:
            start_date = date.fromisoformat(data.get('start_date', budget.start_date.isoformat()))
            end_date = date.fromisoformat(data.get('end_date', budget.end_date.isoformat()))
            
            spent_amount = db.session.query(
                db.func.sum(db.func.abs(Transaction.amount))
            ).join(Account).filter(
                Account.user_id == user_id,
                Transaction.category_id == budget.category_id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date,
                Transaction.transaction_type == 'expense',
                Transaction.status == 'completed'
            ).scalar() or 0
            
            budget.start_date = start_date
            budget.end_date = end_date
            budget.spent_amount = spent_amount
        
        db.session.commit()
        
        return jsonify({
            'message': 'Budget updated successfully',
            'budget': budget.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@budgets_bp.route('/<int:budget_id>', methods=['DELETE'])
@jwt_required()
def delete_budget(budget_id):
    try:
        user_id = get_jwt_identity()
        budget = Budget.query.filter_by(
            budget_id=budget_id,
            user_id=user_id
        ).first()
        
        if not budget:
            return jsonify({'error': 'Budget not found'}), 404
        
        db.session.delete(budget)
        db.session.commit()
        
        return jsonify({
            'message': 'Budget deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@budgets_bp.route('/performance', methods=['GET'])
@jwt_required()
def get_budget_performance():
    try:
        user_id = get_jwt_identity()
        
        # Get current date
        current_date = date.today()
        
        # Get active budgets that include current date
        budgets = Budget.query.filter(
            Budget.user_id == user_id,
            Budget.is_active == True,
            Budget.start_date <= current_date,
            Budget.end_date >= current_date
        ).all()
        
        performance_data = []
        
        for budget in budgets:
            # Recalculate spent amount
            spent_amount = db.session.query(
                db.func.sum(db.func.abs(Transaction.amount))
            ).join(Account).filter(
                Account.user_id == user_id,
                Transaction.category_id == budget.category_id,
                Transaction.transaction_date >= budget.start_date,
                Transaction.transaction_date <= budget.end_date,
                Transaction.transaction_type == 'expense',
                Transaction.status == 'completed'
            ).scalar() or 0
            
            budget.spent_amount = spent_amount
            
            budget_dict = budget.to_dict()
            
            # Add additional performance metrics
            days_total = (budget.end_date - budget.start_date).days + 1
            days_elapsed = (current_date - budget.start_date).days + 1
            days_remaining = (budget.end_date - current_date).days
            
            budget_dict['days_total'] = days_total
            budget_dict['days_elapsed'] = days_elapsed
            budget_dict['days_remaining'] = days_remaining
            budget_dict['time_progress_percentage'] = round((days_elapsed / days_total) * 100, 2)
            
            # Calculate daily average and projected spending
            if days_elapsed > 0:
                daily_average = float(spent_amount) / days_elapsed
                projected_total = daily_average * days_total
                budget_dict['daily_average'] = round(daily_average, 2)
                budget_dict['projected_total'] = round(projected_total, 2)
                budget_dict['projected_status'] = 'Over Budget' if projected_total > float(budget.budget_amount) else 'Within Budget'
            
            performance_data.append(budget_dict)
        
        db.session.commit()
        
        return jsonify({
            'performance': performance_data,
            'current_date': current_date.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500