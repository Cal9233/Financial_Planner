from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from config.db import get_db_connection

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@reports_bp.route('/monthly/<int:year>/<int:month>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_monthly_report(year, month):
    """Get monthly spending report by category"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        # Get spending by category for the specified month
        query = """
            SELECT 
                c.name as category_name,
                c.type as category_type,
                SUM(t.amount) as total
            FROM Transactions t
            INNER JOIN Categories c ON t.category_id = c.category_id
            WHERE t.user_id = %s 
                AND YEAR(t.transaction_date) = %s 
                AND MONTH(t.transaction_date) = %s
                AND t.transaction_type = 'expense'
            GROUP BY c.category_id, c.name, c.type
            ORDER BY total DESC
        """
        
        db.execute(query, (user_id, year, month))
        rows = db.fetchall()
        
        categories = []
        labels = []
        data = []
        total_expense = 0.0
        
        for row in rows:
            amount = float(row['total'])
            categories.append({
                'category': row['category_name'],
                'amount': amount
            })
            labels.append(row['category_name'])
            data.append(amount)
            total_expense += amount
        
        # Also get total income for the month
        income_query = """
            SELECT SUM(amount) as total
            FROM Transactions
            WHERE user_id = %s 
                AND YEAR(transaction_date) = %s 
                AND MONTH(transaction_date) = %s
                AND transaction_type = 'income'
        """
        
        db.execute(income_query, (user_id, year, month))
        income_result = db.fetchone()
        total_income = float(income_result['total']) if income_result['total'] else 0.0
        
        return jsonify({
            'categories': categories,
            'chartData': {
                'labels': labels,
                'datasets': [{
                    'label': 'Spending by Category',
                    'data': data,
                    'backgroundColor': [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40',
                        '#FF6384',
                        '#C9CBCF'
                    ]
                }]
            },
            'total_expense': total_expense,
            'total_income': total_income,
            'net_income': total_income - total_expense
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500