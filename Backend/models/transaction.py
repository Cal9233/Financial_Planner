from datetime import datetime
from config import db

class Transaction(db.Model):
    __tablename__ = 'Transactions'
    
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('Accounts.account_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))
    transaction_date = db.Column(db.Date, nullable=False)
    transaction_time = db.Column(db.Time, default='12:00:00')
    transaction_type = db.Column(db.Enum('income', 'expense', 'transfer'), nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled'), default='completed')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    splits = db.relationship('TransactionSplit', backref='transaction', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'category_id': self.category_id,
            'category_name': self.category.category_name if self.category else None,
            'account_name': self.account.account_name if self.account else None,
            'amount': float(self.amount),
            'description': self.description,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'transaction_time': self.transaction_time.isoformat() if self.transaction_time else None,
            'transaction_type': self.transaction_type,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TransactionSplit(db.Model):
    __tablename__ = 'Transaction_Splits'
    
    transaction_id = db.Column(db.Integer, db.ForeignKey('Transactions.transaction_id'), primary_key=True)
    split_number = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'split_number': self.split_number,
            'category_id': self.category_id,
            'amount': float(self.amount),
            'description': self.description
        }