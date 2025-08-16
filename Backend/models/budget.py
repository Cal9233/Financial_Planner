from datetime import datetime
from config import db

class Budget(db.Model):
    __tablename__ = 'Budgets'
    
    budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'), nullable=False)
    budget_amount = db.Column(db.Numeric(10, 2), nullable=False)
    spent_amount = db.Column(db.Numeric(10, 2), default=0.00)
    period_type = db.Column(db.Enum('weekly', 'monthly', 'yearly'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        budget_dict = {
            'budget_id': self.budget_id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'category_name': self.category.category_name if self.category else None,
            'budget_amount': float(self.budget_amount),
            'spent_amount': float(self.spent_amount),
            'period_type': self.period_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        # Calculate performance metrics
        if self.budget_amount > 0:
            budget_dict['utilization_percentage'] = round((float(self.spent_amount) / float(self.budget_amount)) * 100, 2)
            budget_dict['remaining_budget'] = float(self.budget_amount) - float(self.spent_amount)
            
            if float(self.spent_amount) > float(self.budget_amount):
                budget_dict['status'] = 'Over Budget'
            elif float(self.spent_amount) >= (float(self.budget_amount) * 0.8):
                budget_dict['status'] = 'Near Limit'
            else:
                budget_dict['status'] = 'Within Budget'
        else:
            budget_dict['utilization_percentage'] = 0
            budget_dict['remaining_budget'] = 0
            budget_dict['status'] = 'No Budget Set'
            
        return budget_dict