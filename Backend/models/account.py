from datetime import datetime
from config import db

class Account(db.Model):
    __tablename__ = 'Accounts'
    
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.Enum('checking', 'savings', 'credit', 'investment'), nullable=False)
    balance = db.Column(db.Numeric(15, 2), default=0.00)
    currency = db.Column(db.String(3), default='USD')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='account', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'account_name': self.account_name,
            'account_type': self.account_type,
            'balance': float(self.balance),
            'currency': self.currency,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'is_active': self.is_active
        }