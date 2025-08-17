from datetime import datetime
from config.db import get_db_connection

class Account:
    """Account model using mysql.connector"""
    
    def __init__(self, account_id=None, user_id=None, account_name=None, 
                 account_type=None, balance=0.00, currency='USD', 
                 institution=None, account_number=None, is_active=True,
                 created_at=None, updated_at=None):
        self.account_id = account_id
        self.user_id = user_id
        self.account_name = account_name
        self.account_type = account_type
        self.balance = float(balance) if balance else 0.00
        self.currency = currency
        self.institution = institution
        self.account_number = account_number
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'account_name': self.account_name,
            'account_type': self.account_type,
            'balance': self.balance,
            'currency': self.currency,
            'institution': self.institution,
            'account_number': self.account_number,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def save(self):
        """Save account to database"""
        db = get_db_connection()
        if not db.connection:
            raise Exception("No database connection")
        
        try:
            if self.account_id:
                # Update existing account
                query = """
                    UPDATE Accounts 
                    SET account_name=%s, account_type=%s, balance=%s, 
                        currency=%s, institution=%s, account_number=%s, is_active=%s
                    WHERE account_id=%s AND user_id=%s
                """
                db.execute(query, (
                    self.account_name, self.account_type, self.balance,
                    self.currency, self.institution, self.account_number, 
                    self.is_active, self.account_id, self.user_id
                ))
            else:
                # Insert new account
                query = """
                    INSERT INTO Accounts (user_id, account_name, account_type, 
                                        balance, currency, institution, account_number, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                db.execute(query, (
                    self.user_id, self.account_name, self.account_type,
                    self.balance, self.currency, self.institution, 
                    self.account_number, self.is_active
                ))
                self.account_id = db.cursor.lastrowid
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_by_user_id(user_id, active_only=True):
        """Get all accounts for a user"""
        db = get_db_connection()
        if not db.connection:
            return []
        
        try:
            query = "SELECT * FROM Accounts WHERE user_id = %s"
            params = [user_id]
            
            if active_only:
                query += " AND is_active = TRUE"
            
            query += " ORDER BY account_name"
            
            db.execute(query, params)
            rows = db.fetchall()
            
            accounts = []
            for row in rows:
                accounts.append(Account(
                    account_id=row['account_id'],
                    user_id=row['user_id'],
                    account_name=row['account_name'],
                    account_type=row['account_type'],
                    balance=row['balance'],
                    currency=row['currency'],
                    institution=row['institution'],
                    account_number=row['account_number'],
                    is_active=row['is_active'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
            
            return accounts
            
        except Exception as e:
            print(f"Error getting accounts: {e}")
            return []
    
    @staticmethod
    def get_total_balance(user_id):
        """Get total balance across all active accounts"""
        db = get_db_connection()
        if not db.connection:
            return 0.00
        
        try:
            query = """
                SELECT SUM(balance) as total 
                FROM Accounts 
                WHERE user_id = %s AND is_active = TRUE
            """
            db.execute(query, (user_id,))
            result = db.fetchone()
            return float(result['total']) if result['total'] else 0.00
            
        except Exception as e:
            print(f"Error getting total balance: {e}")
            return 0.00