from datetime import datetime, date
from config.db import get_db_connection

class FinancialGoal:
    """Financial Goal model using mysql.connector"""
    
    def __init__(self, goal_id=None, user_id=None, goal_name=None,
                 goal_type=None, target_amount=0.00, current_amount=0.00,
                 target_date=None, description=None, is_achieved=False,
                 created_at=None, updated_at=None):
        self.goal_id = goal_id
        self.user_id = user_id
        self.goal_name = goal_name
        self.goal_type = goal_type
        self.target_amount = float(target_amount) if target_amount else 0.00
        self.current_amount = float(current_amount) if current_amount else 0.00
        self.target_date = target_date
        self.description = description
        self.is_achieved = is_achieved
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """Convert to dictionary"""
        progress = 0
        if self.target_amount > 0:
            progress = int((self.current_amount / self.target_amount) * 100)
            if progress > 100:
                progress = 100
        
        return {
            'goal_id': self.goal_id,
            'user_id': self.user_id,
            'goal_name': self.goal_name,
            'goal_type': self.goal_type,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'progress_percentage': progress,
            'target_date': self.target_date.isoformat() if isinstance(self.target_date, date) else self.target_date,
            'description': self.description,
            'is_achieved': self.is_achieved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_by_user_id(user_id, include_completed=True):
        """Get all goals for a user"""
        db = get_db_connection()
        if not db.connection:
            return []
        
        try:
            query = "SELECT * FROM FinancialGoals WHERE user_id = %s"
            params = [user_id]
            
            if not include_completed:
                query += " AND is_achieved = FALSE"
            
            query += " ORDER BY target_date, created_at"
            
            db.execute(query, params)
            rows = db.fetchall()
            
            goals = []
            for row in rows:
                goal = FinancialGoal(
                    goal_id=row['goal_id'],
                    user_id=row['user_id'],
                    goal_name=row['goal_name'],
                    goal_type=row['goal_type'],
                    target_amount=row['target_amount'],
                    current_amount=row['current_amount'],
                    target_date=row['target_date'],
                    description=row['description'],
                    is_achieved=row['is_achieved'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                goals.append(goal.to_dict())
            
            return goals
            
        except Exception as e:
            print(f"Error getting goals: {e}")
            return []