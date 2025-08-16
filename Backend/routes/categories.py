from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import Category

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@categories_bp.route('', methods=['GET'])
@jwt_required()
def get_categories():
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        category_type = request.args.get('type')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        # Build query
        query = Category.query.filter_by(user_id=user_id)
        
        if active_only:
            query = query.filter_by(is_active=True)
            
        if category_type:
            query = query.filter_by(category_type=category_type)
        
        categories = query.order_by(Category.category_type, Category.category_name).all()
        
        return jsonify({
            'categories': [cat.to_dict() for cat in categories]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories_bp.route('', methods=['POST'])
@jwt_required()
def create_category():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['category_name', 'category_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if category name already exists for this user
        existing = Category.query.filter_by(
            user_id=user_id,
            category_name=data['category_name']
        ).first()
        
        if existing:
            return jsonify({'error': 'Category name already exists'}), 400
        
        # Create new category
        category = Category(
            user_id=user_id,
            category_name=data['category_name'],
            category_type=data['category_type'],
            description=data.get('description'),
            color_code=data.get('color_code')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    try:
        user_id = get_jwt_identity()
        category = Category.query.filter_by(
            category_id=category_id,
            user_id=user_id
        ).first()
        
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['category_name', 'description', 'color_code', 'is_active']
        for field in allowed_fields:
            if field in data:
                setattr(category, field, data[field])
        
        # Check if category name already exists for this user
        if 'category_name' in data:
            existing = Category.query.filter(
                Category.user_id == user_id,
                Category.category_name == data['category_name'],
                Category.category_id != category_id
            ).first()
            
            if existing:
                return jsonify({'error': 'Category name already exists'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Category updated successfully',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    try:
        user_id = get_jwt_identity()
        category = Category.query.filter_by(
            category_id=category_id,
            user_id=user_id
        ).first()
        
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Soft delete by setting is_active to False
        category.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'Category deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500