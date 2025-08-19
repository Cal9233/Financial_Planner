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
                c.category_name as category_name,
                c.category_type as category_type,
                SUM(t.amount) as total
            FROM Transactions t
            INNER JOIN Categories c ON t.category_id = c.category_id
            WHERE t.user_id = %s 
                AND YEAR(t.transaction_date) = %s 
                AND MONTH(t.transaction_date) = %s
                AND t.transaction_type = 'expense'
            GROUP BY c.category_id, c.category_name, c.category_type
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

@reports_bp.route('/yearly/<int:year>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_yearly_report(year):
    """Get yearly report with monthly breakdown"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        # Get monthly breakdown for the year
        query = """
            SELECT 
                MONTH(transaction_date) as month,
                transaction_type,
                SUM(amount) as total
            FROM Transactions
            WHERE user_id = %s 
                AND YEAR(transaction_date) = %s
            GROUP BY MONTH(transaction_date), transaction_type
            ORDER BY month
        """
        
        db.execute(query, (user_id, year))
        rows = db.fetchall()
        
        # Initialize monthly data
        monthly_data = {}
        for month in range(1, 13):
            monthly_data[month] = {
                'income': 0.0,
                'expense': 0.0,
                'net': 0.0
            }
        
        # Fill in actual data
        for row in rows:
            month = row['month']
            if row['transaction_type'] == 'income':
                monthly_data[month]['income'] = float(row['total'])
            elif row['transaction_type'] == 'expense':
                monthly_data[month]['expense'] = float(row['total'])
        
        # Calculate net income
        for month in monthly_data:
            monthly_data[month]['net'] = monthly_data[month]['income'] - monthly_data[month]['expense']
        
        # Convert to list format for charts
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        chart_data = {
            'labels': months,
            'datasets': [
                {
                    'label': 'Income',
                    'data': [monthly_data[i+1]['income'] for i in range(12)],
                    'backgroundColor': '#4CAF50',
                    'borderColor': '#4CAF50'
                },
                {
                    'label': 'Expenses',
                    'data': [monthly_data[i+1]['expense'] for i in range(12)],
                    'backgroundColor': '#F44336',
                    'borderColor': '#F44336'
                },
                {
                    'label': 'Net Income',
                    'data': [monthly_data[i+1]['net'] for i in range(12)],
                    'type': 'line',
                    'backgroundColor': '#2196F3',
                    'borderColor': '#2196F3'
                }
            ]
        }
        
        # Calculate totals
        total_income = sum(monthly_data[m]['income'] for m in monthly_data)
        total_expense = sum(monthly_data[m]['expense'] for m in monthly_data)
        
        return jsonify({
            'year': year,
            'monthly_data': monthly_data,
            'chart_data': chart_data,
            'total_income': total_income,
            'total_expense': total_expense,
            'net_income': total_income - total_expense
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/expense-trends', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_expense_trends():
    """Get expense trends over last 6 months"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        # Get expense trends by category over last 6 months
        query = """
            SELECT 
                DATE_FORMAT(t.transaction_date, '%Y-%m') as month,
                c.category_name as category_name,
                SUM(t.amount) as total
            FROM Transactions t
            INNER JOIN Categories c ON t.category_id = c.category_id
            WHERE t.user_id = %s 
                AND t.transaction_type = 'expense'
                AND t.transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(t.transaction_date, '%Y-%m'), c.category_id, c.category_name
            ORDER BY month, total DESC
        """
        
        db.execute(query, (user_id,))
        rows = db.fetchall()
        
        # Organize data by month and category
        trends = {}
        categories = set()
        
        for row in rows:
            month = row['month']
            category = row['category_name']
            amount = float(row['total'])
            
            if month not in trends:
                trends[month] = {}
            trends[month][category] = amount
            categories.add(category)
        
        # Get top 5 categories by total spending
        category_totals = {}
        for category in categories:
            total = sum(trends[month].get(category, 0) for month in trends)
            category_totals[category] = total
        
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        top_category_names = [cat[0] for cat in top_categories]
        
        # Create chart data
        months = sorted(trends.keys())
        datasets = []
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        
        for i, category in enumerate(top_category_names):
            datasets.append({
                'label': category,
                'data': [trends[month].get(category, 0) for month in months],
                'backgroundColor': colors[i % len(colors)],
                'borderColor': colors[i % len(colors)]
            })
        
        return jsonify({
            'months': months,
            'categories': top_category_names,
            'chart_data': {
                'labels': months,
                'datasets': datasets
            },
            'category_totals': dict(top_categories)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/cashflow', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_cashflow_report():
    """Get cashflow report"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        user_id = get_jwt_identity()
        period = request.args.get('period', 'month')  # month, quarter, year
        db = get_db_connection()
        
        if not db.connection:
            return jsonify({'error': 'No database connection'}), 500
        
        # Get cashflow data
        if period == 'month':
            date_format = '%Y-%m-%d'
            interval = 'DAY'
            days = 30
        elif period == 'quarter':
            date_format = '%Y-%m'
            interval = 'MONTH'
            days = 90
        else:  # year
            date_format = '%Y-%m'
            interval = 'MONTH'
            days = 365
        
        query = f"""
            SELECT 
                DATE_FORMAT(transaction_date, %s) as date,
                transaction_type,
                SUM(amount) as total
            FROM Transactions
            WHERE user_id = %s 
                AND transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
            GROUP BY DATE_FORMAT(transaction_date, %s), transaction_type
            ORDER BY date
        """
        
        db.execute(query, (date_format, user_id, date_format))
        rows = db.fetchall()
        
        # Organize cashflow data
        cashflow = {}
        for row in rows:
            date = row['date']
            if date not in cashflow:
                cashflow[date] = {'income': 0.0, 'expense': 0.0}
            
            if row['transaction_type'] == 'income':
                cashflow[date]['income'] = float(row['total'])
            elif row['transaction_type'] == 'expense':
                cashflow[date]['expense'] = float(row['total'])
        
        # Calculate running balance
        dates = sorted(cashflow.keys())
        running_balance = 0.0
        balance_data = []
        
        for date in dates:
            running_balance += cashflow[date]['income'] - cashflow[date]['expense']
            balance_data.append(running_balance)
        
        # Create chart data
        chart_data = {
            'labels': dates,
            'datasets': [
                {
                    'label': 'Income',
                    'data': [cashflow[date]['income'] for date in dates],
                    'type': 'bar',
                    'backgroundColor': '#4CAF50'
                },
                {
                    'label': 'Expenses',
                    'data': [cashflow[date]['expense'] for date in dates],
                    'type': 'bar',
                    'backgroundColor': '#F44336'
                },
                {
                    'label': 'Running Balance',
                    'data': balance_data,
                    'type': 'line',
                    'borderColor': '#2196F3',
                    'fill': False
                }
            ]
        }
        
        return jsonify({
            'period': period,
            'cashflow': cashflow,
            'chart_data': chart_data,
            'final_balance': running_balance
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500