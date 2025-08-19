from datetime import datetime, date
from config.db import get_db_connection

class Budget:
    """Budget model using mysql.connector"""
    
    def __init__(self, budget_id=None, user_id=None, category_id=None,
                 budget_amount=0.00, period_type='monthly', start_date=None,
                 end_date=None, is_active=True, created_at=None, updated_at=None):
        self.budget_id = budget_id
        self.user_id = user_id
        self.category_id = category_id
        self.budget_amount = float(budget_amount) if budget_amount else 0.00
        self.period_type = period_type
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'budget_id': self.budget_id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'budget_amount': self.budget_amount,
            'period_type': self.period_type,
            'start_date': self.start_date.isoformat() if isinstance(self.start_date, date) else self.start_date,
            'end_date': self.end_date.isoformat() if self.end_date and isinstance(self.end_date, date) else self.end_date,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_budget_performance(user_id):
        """Get budget performance for all categories"""
        db = get_db_connection()
        if not db.connection:
            return {
                'budgets': [],
                'total_budgeted': 0.00,
                'total_spent': 0.00,
                'overall_percentage': 0
            }
        
        try:
            # Get current month budgets with spending
            query = """
                SELECT 
                    b.budget_id,
                    b.category_id,
                    c.category_name,
                    b.budget_amount,
                    COALESCE(SUM(
                        CASE 
                            WHEN t.transaction_type = 'expense' 
                            AND MONTH(t.transaction_date) = MONTH(CURRENT_DATE())
                            AND YEAR(t.transaction_date) = YEAR(CURRENT_DATE())
                            THEN t.amount 
                            ELSE 0 
                        END
                    ), 0) as spent
                FROM Budgets b
                INNER JOIN Categories c ON b.category_id = c.category_id
                LEFT JOIN Transactions t ON t.category_id = b.category_id 
                    AND t.user_id = b.user_id
                WHERE b.user_id = %s 
                    AND b.is_active = TRUE 
                    AND b.period_type = 'monthly'
                    AND (b.end_date IS NULL OR b.end_date >= CURRENT_DATE())
                GROUP BY b.budget_id, b.category_id, c.category_name, b.budget_amount
                ORDER BY c.category_name
            """
            
            db.execute(query, (user_id,))
            rows = db.fetchall()
            
            budgets = []
            total_budgeted = 0.00
            total_spent = 0.00
            
            for row in rows:
                budget_amount = float(row['budget_amount'])
                spent = float(row['spent'])
                percentage = int((spent / budget_amount * 100)) if budget_amount > 0 else 0
                
                budgets.append({
                    'budget_id': row['budget_id'],
                    'category_id': row['category_id'],
                    'category': row['category_name'],
                    'budgeted': budget_amount,
                    'spent': spent,
                    'percentage': percentage
                })
                
                total_budgeted += budget_amount
                total_spent += spent
            
            overall_percentage = int((total_spent / total_budgeted * 100)) if total_budgeted > 0 else 0
            
            return {
                'budgets': budgets,
                'total_budgeted': total_budgeted,
                'total_spent': total_spent,
                'overall_percentage': overall_percentage
            }
            
        except Exception as e:
            print(f"Error getting budget performance: {e}")
            return {
                'budgets': [],
                'total_budgeted': 0.00,
                'total_spent': 0.00,
                'overall_percentage': 0
            }