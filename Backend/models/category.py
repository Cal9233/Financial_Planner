from datetime import datetime
from config.db import get_db_connection

class Category:
    """Category model using mysql.connector"""
    
    def __init__(self, category_id=None, user_id=None, name=None,
                 type=None, parent_id=None, is_active=True, created_at=None):
        self.category_id = category_id
        self.user_id = user_id
        self.name = name
        self.type = type  # 'income' or 'expense'
        self.parent_id = parent_id
        self.is_active = is_active
        self.created_at = created_at
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'category_id': self.category_id,
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def save(self):
        """Save category to database"""
        db = get_db_connection()
        if not db.connection:
            raise Exception("No database connection")
        
        try:
            if self.category_id:
                # Update existing category
                query = """
                    UPDATE Categories 
                    SET name=%s, type=%s, parent_id=%s, is_active=%s
                    WHERE category_id=%s AND user_id=%s
                """
                db.execute(query, (
                    self.name, self.type, self.parent_id, self.is_active,
                    self.category_id, self.user_id
                ))
            else:
                # Insert new category
                query = """
                    INSERT INTO Categories (user_id, name, type, parent_id, is_active)
                    VALUES (%s, %s, %s, %s, %s)
                """
                db.execute(query, (
                    self.user_id, self.name, self.type, self.parent_id, self.is_active
                ))
                self.category_id = db.cursor.lastrowid
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_by_user_id(user_id, type=None, active_only=True):
        """Get all categories for a user"""
        db = get_db_connection()
        if not db.connection:
            return []
        
        try:
            query = "SELECT * FROM Categories WHERE user_id = %s"
            params = [user_id]
            
            if type:
                query += " AND type = %s"
                params.append(type)
            
            if active_only:
                query += " AND is_active = TRUE"
            
            query += " ORDER BY type, name"
            
            db.execute(query, params)
            rows = db.fetchall()
            
            categories = []
            for row in rows:
                categories.append(Category(
                    category_id=row['category_id'],
                    user_id=row['user_id'],
                    name=row['name'],
                    type=row['type'],
                    parent_id=row['parent_id'],
                    is_active=row['is_active'],
                    created_at=row['created_at']
                ))
            
            return categories
            
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    @staticmethod
    def create_default_categories(user_id):
        """Create default categories for a new user"""
        db = get_db_connection()
        if not db.connection:
            return False
        
        try:
            default_categories = [
                # Income categories
                ('Salary', 'income'),
                ('Freelance', 'income'),
                ('Investments', 'income'),
                ('Other Income', 'income'),
                
                # Expense categories
                ('Food & Dining', 'expense'),
                ('Transportation', 'expense'),
                ('Shopping', 'expense'),
                ('Entertainment', 'expense'),
                ('Bills & Utilities', 'expense'),
                ('Healthcare', 'expense'),
                ('Education', 'expense'),
                ('Travel', 'expense'),
                ('Other Expenses', 'expense')
            ]
            
            for name, cat_type in default_categories:
                category = Category(
                    user_id=user_id,
                    name=name,
                    type=cat_type,
                    is_active=True
                )
                category.save()
            
            return True
            
        except Exception as e:
            print(f"Error creating default categories: {e}")
            return False