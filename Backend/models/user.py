from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config.db import get_db_connection

class SimpleUser:
    """Simple User model using mysql.connector"""
    
    def __init__(self, user_id=None, username=None, email=None, password_hash=None,
                 first_name=None, last_name=None, date_created=None, 
                 last_login=None, is_active=True):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.date_created = date_created
        self.last_login = last_login
        self.is_active = is_active
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
    
    def save(self):
        """Save user to database"""
        db = get_db_connection()
        if not db.connection:
            raise Exception("No database connection")
        
        try:
            if self.user_id:
                # Update existing user
                query = """
                    UPDATE Users 
                    SET username=%s, email=%s, password_hash=%s, 
                        first_name=%s, last_name=%s, is_active=%s
                    WHERE user_id=%s
                """
                db.execute(query, (
                    self.username, self.email, self.password_hash,
                    self.first_name, self.last_name, self.is_active,
                    self.user_id
                ))
            else:
                # Insert new user
                query = """
                    INSERT INTO Users (username, email, password_hash, first_name, last_name)
                    VALUES (%s, %s, %s, %s, %s)
                """
                db.execute(query, (
                    self.username, self.email, self.password_hash,
                    self.first_name, self.last_name
                ))
                self.user_id = db.cursor.lastrowid
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        db = get_db_connection()
        if not db.connection:
            return None
        
        try:
            query = "SELECT * FROM Users WHERE username = %s"
            db.execute(query, (username,))
            row = db.fetchone()
            
            if row:
                return SimpleUser(
                    user_id=row['user_id'],
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    date_created=row['date_created'],
                    last_login=row['last_login'],
                    is_active=row['is_active']
                )
            return None
            
        except Exception as e:
            print(f"Error finding user: {e}")
            return None
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        db = get_db_connection()
        if not db.connection:
            return None
        
        try:
            query = "SELECT * FROM Users WHERE email = %s"
            db.execute(query, (email,))
            row = db.fetchone()
            
            if row:
                return SimpleUser(
                    user_id=row['user_id'],
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    date_created=row['date_created'],
                    last_login=row['last_login'],
                    is_active=row['is_active']
                )
            return None
            
        except Exception as e:
            print(f"Error finding user: {e}")
            return None
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        db = get_db_connection()
        if not db.connection:
            return None
        
        try:
            query = "SELECT * FROM Users WHERE user_id = %s"
            db.execute(query, (user_id,))
            row = db.fetchone()
            
            if row:
                return SimpleUser(
                    user_id=row['user_id'],
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    date_created=row['date_created'],
                    last_login=row['last_login'],
                    is_active=row['is_active']
                )
            return None
            
        except Exception as e:
            print(f"Error finding user: {e}")
            return None
    
    def update_last_login(self):
        """Update last login timestamp"""
        db = get_db_connection()
        if not db.connection:
            return False
        
        try:
            query = "UPDATE Users SET last_login = %s WHERE user_id = %s"
            db.execute(query, (datetime.utcnow(), self.user_id))
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating last login: {e}")
            return False