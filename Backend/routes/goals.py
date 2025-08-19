from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.goal import FinancialGoal
from config.db import get_db_connection
from datetime import datetime
from utils.decorators import require_db_connection

goals_bp = Blueprint('goals', __name__, url_prefix='/api/goals')

@goals_bp.route('', methods=['GET', 'OPTIONS'])
@jwt_required()
@require_db_connection
def get_goals():
    """Get all goals for user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = int(get_jwt_identity())
        include_completed = request.args.get('include_completed', 'false').lower() == 'true'
        
        goals = FinancialGoal.get_by_user_id(user_id, include_completed)
        
        return jsonify({
            'goals': goals,
            'total': len(goals)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/<int:goal_id>', methods=['GET', 'OPTIONS'])
@jwt_required()
@require_db_connection
def get_goal(goal_id):
    """Get specific goal"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = int(get_jwt_identity())
        goals = FinancialGoal.get_by_user_id(user_id, include_completed=True)
        
        for goal in goals:
            if goal['goal_id'] == goal_id:
                return jsonify({'goal': goal}), 200
        
        return jsonify({'error': 'Goal not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('', methods=['POST'])
@jwt_required()
@require_db_connection
def create_goal():
    """Create new goal"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        insert_query = """
            INSERT INTO FinancialGoals 
            (user_id, goal_name, goal_type, target_amount, current_amount, target_date, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        db.execute(insert_query, (
            user_id,
            data.get('goal_name'),
            data.get('goal_type'),
            data.get('target_amount'),
            data.get('current_amount', 0),
            data.get('target_date'),
            data.get('description')
        ))
        
        goal_id = db.cursor.lastrowid
        db.commit()
        
        return jsonify({
            'message': 'Goal created successfully',
            'goal_id': goal_id
        }), 201
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/<int:goal_id>', methods=['PUT'])
@jwt_required()
@require_db_connection
def update_goal(goal_id):
    """Update goal"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        # Build update query dynamically
        update_fields = []
        params = []
        
        if 'goal_name' in data:
            update_fields.append('goal_name = %s')
            params.append(data['goal_name'])
        if 'goal_type' in data:
            update_fields.append('goal_type = %s')
            params.append(data['goal_type'])
        if 'target_amount' in data:
            update_fields.append('target_amount = %s')
            params.append(data['target_amount'])
        if 'current_amount' in data:
            update_fields.append('current_amount = %s')
            params.append(data['current_amount'])
        if 'target_date' in data:
            update_fields.append('target_date = %s')
            params.append(data['target_date'])
        if 'description' in data:
            update_fields.append('description = %s')
            params.append(data['description'])
        if 'is_achieved' in data:
            update_fields.append('is_achieved = %s')
            params.append(data['is_achieved'])
        
        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400
        
        update_fields.append('updated_at = %s')
        params.append(datetime.utcnow())
        
        params.extend([goal_id, user_id])
        
        update_query = f"""
            UPDATE FinancialGoals 
            SET {', '.join(update_fields)}
            WHERE goal_id = %s AND user_id = %s
        """
        
        db.execute(update_query, params)
        db.commit()
        
        return jsonify({
            'message': 'Goal updated successfully'
        }), 200
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
@jwt_required()
@require_db_connection
def delete_goal(goal_id):
    """Delete goal"""
    try:
        user_id = int(get_jwt_identity())
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        delete_query = """
            DELETE FROM FinancialGoals 
            WHERE goal_id = %s AND user_id = %s
        """
        
        db.execute(delete_query, (goal_id, user_id))
        db.commit()
        
        return jsonify({
            'message': 'Goal deleted successfully'
        }), 200
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/<int:goal_id>/progress', methods=['PUT'])
@jwt_required()
@require_db_connection
def update_goal_progress(goal_id):
    """Update goal progress (current amount)"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        current_amount = data.get('current_amount', 0)
        
        # Check if goal is achieved
        check_query = """
            SELECT target_amount FROM FinancialGoals 
            WHERE goal_id = %s AND user_id = %s
        """
        db.execute(check_query, (goal_id, user_id))
        result = db.fetchone()
        
        if not result:
            return jsonify({'error': 'Goal not found'}), 404
        
        target_amount = float(result['target_amount'])
        is_achieved = current_amount >= target_amount
        
        update_query = """
            UPDATE FinancialGoals 
            SET current_amount = %s, is_achieved = %s, updated_at = %s
            WHERE goal_id = %s AND user_id = %s
        """
        
        db.execute(update_query, (
            current_amount,
            is_achieved,
            datetime.utcnow(),
            goal_id,
            user_id
        ))
        
        db.commit()
        
        return jsonify({
            'message': 'Goal progress updated successfully',
            'is_achieved': is_achieved
        }), 200
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500