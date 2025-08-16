from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, datetime
from config import db
from models import FinancialGoal

goals_bp = Blueprint('goals', __name__, url_prefix='/api/goals')

@goals_bp.route('', methods=['GET'])
@jwt_required()
def get_goals():
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        goal_type = request.args.get('type')
        priority_level = request.args.get('priority')
        include_completed = request.args.get('include_completed', 'false').lower() == 'true'
        
        # Build query
        query = FinancialGoal.query.filter_by(user_id=user_id)
        
        if not include_completed:
            query = query.filter_by(is_completed=False)
            
        if goal_type:
            query = query.filter_by(goal_type=goal_type)
            
        if priority_level:
            query = query.filter_by(priority_level=priority_level)
        
        # Order by priority and target date
        goals = query.order_by(
            FinancialGoal.is_completed,
            db.case(
                (FinancialGoal.priority_level == 'high', 1),
                (FinancialGoal.priority_level == 'medium', 2),
                (FinancialGoal.priority_level == 'low', 3)
            ),
            FinancialGoal.target_date
        ).all()
        
        return jsonify({
            'goals': [goal.to_dict() for goal in goals]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('', methods=['POST'])
@jwt_required()
def create_goal():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['goal_name', 'target_amount', 'goal_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create goal
        goal = FinancialGoal(
            user_id=user_id,
            goal_name=data['goal_name'],
            target_amount=data['target_amount'],
            current_amount=data.get('current_amount', 0.00),
            target_date=date.fromisoformat(data['target_date']) if data.get('target_date') else None,
            goal_type=data['goal_type'],
            priority_level=data.get('priority_level', 'medium'),
            description=data.get('description')
        )
        
        db.session.add(goal)
        db.session.commit()
        
        return jsonify({
            'message': 'Goal created successfully',
            'goal': goal.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_goal(goal_id):
    try:
        user_id = get_jwt_identity()
        goal = FinancialGoal.query.filter_by(
            goal_id=goal_id,
            user_id=user_id
        ).first()
        
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['goal_name', 'target_amount', 'current_amount', 'target_date', 
                         'priority_level', 'description']
        
        for field in allowed_fields:
            if field in data:
                if field == 'target_date':
                    setattr(goal, field, date.fromisoformat(data[field]) if data[field] else None)
                else:
                    setattr(goal, field, data[field])
        
        # Check if goal is completed
        if goal.current_amount >= goal.target_amount and not goal.is_completed:
            goal.is_completed = True
            goal.completed_at = datetime.utcnow()
        elif goal.current_amount < goal.target_amount and goal.is_completed:
            goal.is_completed = False
            goal.completed_at = None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Goal updated successfully',
            'goal': goal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_goal(goal_id):
    try:
        user_id = get_jwt_identity()
        goal = FinancialGoal.query.filter_by(
            goal_id=goal_id,
            user_id=user_id
        ).first()
        
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        db.session.delete(goal)
        db.session.commit()
        
        return jsonify({
            'message': 'Goal deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/<int:goal_id>/contribute', methods=['POST'])
@jwt_required()
def contribute_to_goal(goal_id):
    try:
        user_id = get_jwt_identity()
        goal = FinancialGoal.query.filter_by(
            goal_id=goal_id,
            user_id=user_id
        ).first()
        
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        data = request.get_json()
        
        if 'amount' not in data:
            return jsonify({'error': 'Amount is required'}), 400
        
        # Update current amount
        goal.current_amount += data['amount']
        
        # Check if goal is completed
        if goal.current_amount >= goal.target_amount and not goal.is_completed:
            goal.is_completed = True
            goal.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Contribution added successfully',
            'goal': goal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500