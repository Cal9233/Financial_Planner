from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.category import Category
from config.db import get_db_connection

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@categories_bp.route('', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_categories():
    """Get all categories for user"""
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

@categories_bp.route('/<int:category_id>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_category(category_id):
    """Get specific category"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        categories = Category.get_by_user_id(user_id)
        
        for cat in categories:
            if cat.category_id == category_id:
                return jsonify({'category': cat.to_dict()}), 200
        
        return jsonify({'error': 'Category not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories_bp.route('', methods=['POST'])
@jwt_required()
def create_category():
    """Create new category"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Category name is required'}), 400
        if not data.get('type') or data['type'] not in ['income', 'expense']:
            return jsonify({'error': 'Category type must be "income" or "expense"'}), 400
        
        category = Category(
            user_id=user_id,
            name=data['name'],
            type=data['type'],
            parent_id=data.get('parent_id'),
            is_active=True
        )
        
        category.save()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """Update category"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        categories = Category.get_by_user_id(user_id)
        
        for cat in categories:
            if cat.category_id == category_id:
                # Update fields
                if 'name' in data:
                    cat.name = data['name']
                if 'type' in data and data['type'] in ['income', 'expense']:
                    cat.type = data['type']
                if 'parent_id' in data:
                    cat.parent_id = data['parent_id']
                if 'is_active' in data:
                    cat.is_active = data['is_active']
                
                cat.save()
                
                return jsonify({
                    'message': 'Category updated successfully',
                    'category': cat.to_dict()
                }), 200
        
        return jsonify({'error': 'Category not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """Delete category (soft delete)"""
    try:
        user_id = get_jwt_identity()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        # Check if category exists and belongs to user
        check_query = """
            SELECT category_id FROM Categories 
            WHERE category_id = %s AND user_id = %s
        """
        db.execute(check_query, (category_id, user_id))
        result = db.fetchone()
        
        if not result:
            return jsonify({'error': 'Category not found'}), 404
        
        # Check if category is in use
        usage_query = """
            SELECT COUNT(*) as count FROM Transactions 
            WHERE category_id = %s
        """
        db.execute(usage_query, (category_id,))
        usage = db.fetchone()
        
        if usage and usage['count'] > 0:
            # Soft delete if in use
            update_query = """
                UPDATE Categories 
                SET is_active = FALSE 
                WHERE category_id = %s AND user_id = %s
            """
            db.execute(update_query, (category_id, user_id))
            message = 'Category deactivated (in use by transactions)'
        else:
            # Hard delete if not in use
            delete_query = """
                DELETE FROM Categories 
                WHERE category_id = %s AND user_id = %s
            """
            db.execute(delete_query, (category_id, user_id))
            message = 'Category deleted successfully'
        
        db.commit()
        
        return jsonify({
            'message': message
        }), 200
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/batch', methods=['POST'])
@jwt_required()
def create_default_categories():
    """Create default categories for user"""
    try:
        user_id = get_jwt_identity()
        
        # Check if user already has categories
        existing = Category.get_by_user_id(user_id)
        if existing:
            return jsonify({'error': 'User already has categories'}), 400
        
        # Create default categories
        success = Category.create_default_categories(user_id)
        
        if success:
            categories = Category.get_by_user_id(user_id)
            category_list = [cat.to_dict() for cat in categories]
            
            return jsonify({
                'message': 'Default categories created successfully',
                'categories': category_list
            }), 201
        else:
            return jsonify({'error': 'Failed to create default categories'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500