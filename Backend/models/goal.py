from datetime import datetime
from config import db

class FinancialGoal(db.Model):
    __tablename__ = 'Financial_Goals'
    
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    goal_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Numeric(15, 2), nullable=False)
    current_amount = db.Column(db.Numeric(15, 2), default=0.00)
    target_date = db.Column(db.Date)
    goal_type = db.Column(db.Enum('savings', 'debt_payoff', 'investment'), nullable=False)
    priority_level = db.Column(db.Enum('low', 'medium', 'high'), default='medium')
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        goal_dict = {
            'goal_id': self.goal_id,
            'user_id': self.user_id,
            'goal_name': self.goal_name,
            'target_amount': float(self.target_amount),
            'current_amount': float(self.current_amount),
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'goal_type': self.goal_type,
            'priority_level': self.priority_level,
            'description': self.description,
            'is_completed': self.is_completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
        
        # Calculate progress percentage
        if self.target_amount > 0:
            goal_dict['progress_percentage'] = round((float(self.current_amount) / float(self.target_amount)) * 100, 2)
        else:
            goal_dict['progress_percentage'] = 0
            
        return goal_dict