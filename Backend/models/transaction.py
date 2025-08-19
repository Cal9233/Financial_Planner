from datetime import datetime, date
from config.db import get_db_connection

class Transaction:
    """Transaction model using mysql.connector"""
    
    def __init__(self, transaction_id=None, user_id=None, account_id=None,
                 category_id=None, transaction_date=None, amount=0.00,
                 transaction_type=None, description=None, reference_number=None,
                 is_recurring=False, created_at=None, updated_at=None):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.account_id = account_id
        self.category_id = category_id
        self.transaction_date = transaction_date
        self.amount = float(amount) if amount else 0.00
        self.transaction_type = transaction_type
        self.description = description
        self.reference_number = reference_number
        self.is_recurring = is_recurring
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'account_id': self.account_id,
            'category_id': self.category_id,
            'transaction_date': self.transaction_date.isoformat() if isinstance(self.transaction_date, date) else self.transaction_date,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'description': self.description,
            'reference_number': self.reference_number,
            'is_recurring': self.is_recurring,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def save(self):
        """Save transaction to database"""
        db = get_db_connection()
        if not db.connection:
            raise Exception("No database connection")
        
        try:
            if self.transaction_id:
                # Update existing transaction
                query = """
                    UPDATE Transactions 
                    SET account_id=%s, category_id=%s, transaction_date=%s,
                        amount=%s, transaction_type=%s, description=%s,
                        reference_number=%s, is_recurring=%s
                    WHERE transaction_id=%s AND user_id=%s
                """
                db.execute(query, (
                    self.account_id, self.category_id, self.transaction_date,
                    self.amount, self.transaction_type, self.description,
                    self.reference_number, self.is_recurring,
                    self.transaction_id, self.user_id
                ))
            else:
                # Insert new transaction
                query = """
                    INSERT INTO Transactions (user_id, account_id, category_id,
                                            transaction_date, amount, transaction_type,
                                            description, reference_number, is_recurring)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                db.execute(query, (
                    self.user_id, self.account_id, self.category_id,
                    self.transaction_date, self.amount, self.transaction_type,
                    self.description, self.reference_number, self.is_recurring
                ))
                self.transaction_id = db.cursor.lastrowid
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_recent_transactions(user_id, limit=10, offset=0):
        """Get recent transactions for a user"""
        db = get_db_connection()
        if not db.connection:
            return []
        
        try:
            query = """
                SELECT t.*, a.account_name, c.category_name
                FROM Transactions t
                LEFT JOIN Accounts a ON t.account_id = a.account_id
                LEFT JOIN Categories c ON t.category_id = c.category_id
                WHERE t.user_id = %s
                ORDER BY t.transaction_date DESC, t.created_at DESC
                LIMIT %s OFFSET %s
            """
            db.execute(query, (user_id, limit, offset))
            rows = db.fetchall()
            
            transactions = []
            for row in rows:
                trans = Transaction(
                    transaction_id=row['transaction_id'],
                    user_id=row['user_id'],
                    account_id=row['account_id'],
                    category_id=row['category_id'],
                    transaction_date=row['transaction_date'],
                    amount=row['amount'],
                    transaction_type=row['transaction_type'],
                    description=row['description'],
                    reference_number=row['reference_number'],
                    is_recurring=row['is_recurring'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                # Add extra fields for display
                trans_dict = trans.to_dict()
                trans_dict['account_name'] = row['account_name']
                trans_dict['category_name'] = row['category_name']
                transactions.append(trans_dict)
            
            return transactions
            
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    @staticmethod
    def get_transaction_summary(user_id, period='month'):
        """Get transaction summary (income, expenses, etc.)"""
        db = get_db_connection()
        if not db.connection:
            return {
                'total_income': 0.00,
                'total_expense': 0.00,
                'net_income': 0.00,
                'income_trend': 0.0,
                'expense_trend': 0.0,
                'period': period
            }
        
        try:
            # Get current period data
            if period == 'month':
                current_query = """
                    SELECT 
                        SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income,
                        SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense
                    FROM Transactions
                    WHERE user_id = %s 
                    AND MONTH(transaction_date) = MONTH(CURRENT_DATE())
                    AND YEAR(transaction_date) = YEAR(CURRENT_DATE())
                """
                previous_query = """
                    SELECT 
                        SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income,
                        SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense
                    FROM Transactions
                    WHERE user_id = %s 
                    AND MONTH(transaction_date) = MONTH(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH))
                    AND YEAR(transaction_date) = YEAR(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH))
                """
            else:  # Default to year
                current_query = """
                    SELECT 
                        SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income,
                        SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense
                    FROM Transactions
                    WHERE user_id = %s 
                    AND YEAR(transaction_date) = YEAR(CURRENT_DATE())
                """
                previous_query = """
                    SELECT 
                        SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income,
                        SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense
                    FROM Transactions
                    WHERE user_id = %s 
                    AND YEAR(transaction_date) = YEAR(DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR))
                """
            
            # Get current period
            db.execute(current_query, (user_id,))
            current = db.fetchone()
            current_income = float(current['income']) if current['income'] else 0.00
            current_expense = float(current['expense']) if current['expense'] else 0.00
            
            # Get previous period for trend calculation
            db.execute(previous_query, (user_id,))
            previous = db.fetchone()
            previous_income = float(previous['income']) if previous['income'] else 0.00
            previous_expense = float(previous['expense']) if previous['expense'] else 0.00
            
            # Calculate trends
            income_trend = 0.0
            if previous_income > 0:
                income_trend = ((current_income - previous_income) / previous_income) * 100
            
            expense_trend = 0.0
            if previous_expense > 0:
                expense_trend = ((current_expense - previous_expense) / previous_expense) * 100
            
            return {
                'total_income': current_income,
                'total_expense': current_expense,
                'net_income': current_income - current_expense,
                'income_trend': round(income_trend, 1),
                'expense_trend': round(expense_trend, 1),
                'period': period
            }
            
        except Exception as e:
            print(f"Error getting transaction summary: {e}")
            return {
                'total_income': 0.00,
                'total_expense': 0.00,
                'net_income': 0.00,
                'income_trend': 0.0,
                'expense_trend': 0.0,
                'period': period
            }
    
    @staticmethod
    def get_count(user_id):
        """Get total transaction count for a user"""
        db = get_db_connection()
        if not db.connection:
            return 0
        
        try:
            query = "SELECT COUNT(*) as count FROM Transactions WHERE user_id = %s"
            db.execute(query, (user_id,))
            result = db.fetchone()
            return result['count'] if result else 0
            
        except Exception as e:
            print(f"Error getting transaction count: {e}")
            return 0
    
    @staticmethod
    def get_summary_for_period(user_id, start_date, end_date):
        """Get transaction summary for a specific period"""
        db = get_db_connection()
        if not db.connection:
            return {'total_income': 0, 'total_expenses': 0, 'net_income': 0, 'transaction_count': 0}
        
        try:
            query = """
                SELECT 
                    SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN t.transaction_type = 'expense' THEN ABS(t.amount) ELSE 0 END) as total_expenses,
                    COUNT(*) as transaction_count
                FROM Transactions t
                JOIN Accounts a ON t.account_id = a.account_id
                WHERE a.user_id = %s AND t.transaction_date BETWEEN %s AND %s
            """
            db.execute(query, (user_id, start_date, end_date))
            result = db.fetchone()
            
            if result:
                total_income = float(result['total_income'] or 0)
                total_expenses = float(result['total_expenses'] or 0)
                return {
                    'total_income': total_income,
                    'total_expenses': total_expenses,
                    'net_income': total_income - total_expenses,
                    'transaction_count': result['transaction_count']
                }
            
            return {'total_income': 0, 'total_expenses': 0, 'net_income': 0, 'transaction_count': 0}
            
        except Exception as e:
            print(f"Error getting summary for period: {e}")
            return {'total_income': 0, 'total_expenses': 0, 'net_income': 0, 'transaction_count': 0}
    
    @staticmethod
    def get_spending_by_category(user_id, period='month'):
        """Get spending breakdown by category"""
        db = get_db_connection()
        if not db.connection:
            return []
        
        try:
            # Calculate date range based on period
            end_date = datetime.now()
            if period == 'month':
                start_date = end_date - timedelta(days=30)
            elif period == 'week':
                start_date = end_date - timedelta(days=7)
            elif period == 'year':
                start_date = end_date - timedelta(days=365)
            else:
                start_date = datetime(end_date.year, end_date.month, 1)
            
            query = """
                SELECT 
                    c.category_id,
                    c.category_name,
                    c.category_type,
                    c.icon,
                    SUM(t.amount) as total_amount,
                    COUNT(t.transaction_id) as transaction_count
                FROM Categories c
                LEFT JOIN Transactions t ON c.category_id = t.category_id 
                    AND t.user_id = %s 
                    AND t.transaction_date BETWEEN %s AND %s
                    AND t.transaction_type = 'expense'
                WHERE c.user_id = %s OR c.is_default = 1
                GROUP BY c.category_id, c.category_name, c.category_type, c.icon
                HAVING total_amount > 0
                ORDER BY total_amount DESC
            """
            
            db.execute(query, (user_id, start_date, end_date, user_id))
            results = db.fetchall()
            
            categories = []
            for row in results:
                categories.append({
                    'category_id': row['category_id'],
                    'category_name': row['category_name'],
                    'category_type': row['category_type'],
                    'icon': row['icon'],
                    'total_amount': float(row['total_amount'] or 0),
                    'transaction_count': row['transaction_count']
                })
            
            return categories
            
        except Exception as e:
            print(f"Error getting spending by category: {e}")
            return []
    
    @staticmethod
    def find_by_id(transaction_id, user_id=None):
        """Find transaction by ID and optionally user ID"""
        db = get_db_connection()
        if not db.connection:
            return None
        
        try:
            query = """
                SELECT t.*, a.account_name, c.category_name
                FROM Transactions t
                LEFT JOIN Accounts a ON t.account_id = a.account_id
                LEFT JOIN Categories c ON t.category_id = c.category_id
                WHERE t.transaction_id = %s AND t.user_id = %s
            """
            db.execute(query, (transaction_id, user_id))
            row = db.fetchone()
            
            if row:
                trans = Transaction(
                    transaction_id=row['transaction_id'],
                    user_id=row['user_id'],
                    account_id=row['account_id'],
                    category_id=row['category_id'],
                    transaction_date=row['transaction_date'],
                    amount=row['amount'],
                    transaction_type=row['transaction_type'],
                    description=row['description'],
                    reference_number=row['reference_number'],
                    is_recurring=row['is_recurring'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                return trans
            return None
            
        except Exception as e:
            print(f"Error finding transaction: {e}")
            return None
    
    def delete(self):
        """Delete transaction from database"""
        db = get_db_connection()
        if not db.connection:
            raise Exception("No database connection")
        
        try:
            query = "DELETE FROM Transactions WHERE transaction_id = %s AND user_id = %s"
            db.execute(query, (self.transaction_id, self.user_id))
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise e