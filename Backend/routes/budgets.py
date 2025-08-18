from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.budget import Budget
from config.db import get_db_connection

budgets_bp = Blueprint('budgets', __name__, url_prefix='/api/budgets')

@budgets_bp.route('/performance', methods=['GET', 'OPTIONS'])
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

@budgets_bp.route('', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_budgets():
    """Get all budgets for user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        query = """
            SELECT b.*, c.name as category_name, c.type as category_type
            FROM Budgets b
            INNER JOIN Categories c ON b.category_id = c.category_id
            WHERE b.user_id = %s AND b.is_active = TRUE
            ORDER BY c.name
        """
        
        db.execute(query, (user_id,))
        rows = db.fetchall()
        
        budgets = []
        for row in rows:
            budgets.append({
                'budget_id': row['budget_id'],
                'category_id': row['category_id'],
                'category_name': row['category_name'],
                'category_type': row['category_type'],
                'budget_amount': float(row['budget_amount']),
                'period_type': row['period_type'],
                'start_date': row['start_date'].isoformat() if row['start_date'] else None,
                'end_date': row['end_date'].isoformat() if row['end_date'] else None,
                'is_active': row['is_active']
            })
        
        return jsonify({
            'budgets': budgets,
            'total': len(budgets)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@budgets_bp.route('', methods=['POST'])
@jwt_required()
def create_budget():
    """Create new budget"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        # Check if budget already exists for this category
        check_query = """
            SELECT budget_id FROM Budgets 
            WHERE user_id = %s AND category_id = %s AND is_active = TRUE
        """
        db.execute(check_query, (user_id, data.get('category_id')))
        existing = db.fetchone()
        
        if existing:
            return jsonify({'error': 'Budget already exists for this category'}), 400
        
        # Insert new budget
        insert_query = """
            INSERT INTO Budgets (user_id, category_id, budget_amount, period_type, start_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        db.execute(insert_query, (
            user_id,
            data.get('category_id'),
            data.get('budget_amount'),
            data.get('period_type', 'monthly'),
            data.get('start_date')
        ))
        
        budget_id = db.cursor.lastrowid
        db.commit()
        
        return jsonify({
            'message': 'Budget created successfully',
            'budget_id': budget_id
        }), 201
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500

@budgets_bp.route('/<int:budget_id>', methods=['PUT'])
@jwt_required()
def update_budget(budget_id):
    """Update budget"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        # Update budget
        update_query = """
            UPDATE Budgets 
            SET budget_amount = %s, period_type = %s
            WHERE budget_id = %s AND user_id = %s
        """
        
        db.execute(update_query, (
            data.get('budget_amount'),
            data.get('period_type', 'monthly'),
            budget_id,
            user_id
        ))
        
        db.commit()
        
        return jsonify({
            'message': 'Budget updated successfully'
        }), 200
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500

@budgets_bp.route('/<int:budget_id>', methods=['DELETE'])
@jwt_required()
def delete_budget(budget_id):
    """Delete budget"""
    try:
        user_id = get_jwt_identity()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        # Soft delete
        update_query = """
            UPDATE Budgets 
            SET is_active = FALSE 
            WHERE budget_id = %s AND user_id = %s
        """
        
        db.execute(update_query, (budget_id, user_id))
        db.commit()
        
        return jsonify({
            'message': 'Budget deleted successfully'
        }), 200
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500