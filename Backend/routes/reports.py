from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from sqlalchemy import extract
import io
from config import db
from models import Transaction, Account, Category, Budget, FinancialGoal
from services.pdf_generator import generate_monthly_report

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@reports_bp.route('/monthly/<int:year>/<int:month>', methods=['GET'])
@jwt_required()
def get_monthly_report(year, month):
    try:
        user_id = get_jwt_identity()
        
        # Get transactions for the month
        transactions = Transaction.query.join(Account).filter(
            Account.user_id == user_id,
            extract('year', Transaction.transaction_date) == year,
            extract('month', Transaction.transaction_date) == month,
            Transaction.status == 'completed'
        ).order_by(Transaction.transaction_date, Transaction.created_at).all()
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_expenses = sum(abs(t.amount) for t in transactions if t.transaction_type == 'expense')
        net_income = total_income - total_expenses
        
        # Group by category
        category_breakdown = {}
        for transaction in transactions:
            if transaction.category:
                cat_name = transaction.category.category_name
                cat_type = transaction.category.category_type
                
                if cat_name not in category_breakdown:
                    category_breakdown[cat_name] = {
                        'type': cat_type,
                        'total': 0,
                        'count': 0,
                        'transactions': []
                    }
                
                category_breakdown[cat_name]['total'] += abs(transaction.amount)
                category_breakdown[cat_name]['count'] += 1
                category_breakdown[cat_name]['transactions'].append({
                    'date': transaction.transaction_date.isoformat(),
                    'description': transaction.description,
                    'amount': float(transaction.amount)
                })
        
        # Get account balances
        accounts = Account.query.filter_by(user_id=user_id, is_active=True).all()
        account_summary = [{
            'name': acc.account_name,
            'type': acc.account_type,
            'balance': float(acc.balance)
        } for acc in accounts]
        
        # Get budget performance for the month
        budgets = Budget.query.filter(
            Budget.user_id == user_id,
            Budget.start_date <= date(year, month, 1),
            Budget.end_date >= date(year, month, 1)
        ).all()
        
        budget_performance = []
        for budget in budgets:
            # Calculate spent for this specific month
            month_spent = sum(
                abs(t.amount) for t in transactions 
                if t.category_id == budget.category_id and t.transaction_type == 'expense'
            )
            
            budget_performance.append({
                'category': budget.category.category_name,
                'budgeted': float(budget.budget_amount),
                'spent': float(month_spent),
                'remaining': float(budget.budget_amount) - float(month_spent),
                'utilization': round((float(month_spent) / float(budget.budget_amount)) * 100, 2) if budget.budget_amount > 0 else 0
            })
        
        # Get active goals
        goals = FinancialGoal.query.filter_by(
            user_id=user_id,
            is_completed=False
        ).order_by(FinancialGoal.target_date).all()
        
        goal_progress = [{
            'name': goal.goal_name,
            'type': goal.goal_type,
            'target': float(goal.target_amount),
            'current': float(goal.current_amount),
            'progress': goal.to_dict()['progress_percentage'],
            'target_date': goal.target_date.isoformat() if goal.target_date else None
        } for goal in goals]
        
        return jsonify({
            'year': year,
            'month': month,
            'summary': {
                'total_income': float(total_income),
                'total_expenses': float(total_expenses),
                'net_income': float(net_income),
                'transaction_count': len(transactions)
            },
            'category_breakdown': category_breakdown,
            'account_summary': account_summary,
            'budget_performance': budget_performance,
            'goal_progress': goal_progress
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/pdf/<int:year>/<int:month>', methods=['GET'])
@jwt_required()
def download_monthly_pdf(year, month):
    try:
        user_id = get_jwt_identity()
        
        # Get user info
        from models import User
        user = User.query.get(user_id)
        
        # Get all the data (similar to monthly report)
        transactions = Transaction.query.join(Account).filter(
            Account.user_id == user_id,
            extract('year', Transaction.transaction_date) == year,
            extract('month', Transaction.transaction_date) == month,
            Transaction.status == 'completed'
        ).order_by(Transaction.transaction_date, Transaction.created_at).all()
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_expenses = sum(abs(t.amount) for t in transactions if t.transaction_type == 'expense')
        
        # Group by category
        category_data = {}
        for transaction in transactions:
            if transaction.category:
                cat_name = transaction.category.category_name
                cat_type = transaction.category.category_type
                
                if cat_type not in category_data:
                    category_data[cat_type] = {}
                
                if cat_name not in category_data[cat_type]:
                    category_data[cat_type][cat_name] = {
                        'total': 0,
                        'count': 0
                    }
                
                category_data[cat_type][cat_name]['total'] += abs(transaction.amount)
                category_data[cat_type][cat_name]['count'] += 1
        
        # Get accounts
        accounts = Account.query.filter_by(user_id=user_id, is_active=True).all()
        
        # Get budgets
        budgets = Budget.query.filter(
            Budget.user_id == user_id,
            Budget.start_date <= date(year, month, 1),
            Budget.end_date >= date(year, month, 1)
        ).all()
        
        # Get goals
        goals = FinancialGoal.query.filter_by(
            user_id=user_id,
            is_completed=False
        ).order_by(FinancialGoal.target_date).limit(5).all()
        
        # Generate PDF
        pdf_buffer = generate_monthly_report(
            user=user,
            year=year,
            month=month,
            transactions=transactions,
            total_income=float(total_income),
            total_expenses=float(total_expenses),
            category_data=category_data,
            accounts=accounts,
            budgets=budgets,
            goals=goals
        )
        
        # Send file
        pdf_buffer.seek(0)
        filename = f'financial_report_{year}_{month:02d}.pdf'
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500