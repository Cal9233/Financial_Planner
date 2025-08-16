from datetime import datetime
from config import db

class Category(db.Model):
    __tablename__ = 'Categories'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    category_name = db.Column(db.String(50), nullable=False)
    category_type = db.Column(db.Enum('income', 'expense'), nullable=False)
    description = db.Column(db.Text)
    color_code = db.Column(db.String(7))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='category', lazy='dynamic')
    budgets = db.relationship('Budget', backref='category', lazy='dynamic')
    
    def to_dict(self):
        return {
            'category_id': self.category_id,
            'user_id': self.user_id,
            'category_name': self.category_name,
            'category_type': self.category_type,
            'description': self.description,
            'color_code': self.color_code,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }