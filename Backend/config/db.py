import mysql.connector
from flask import session, g
import json

class SimpleDBConnection:
    """Simple MySQL connection manager based on DAL.py approach"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self, host='localhost', user=None, password=None, database=None, port=3306):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Successfully connected to database")
            return True
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            return False
    
    def execute(self, query, params=None):
        """Execute a query"""
        try:
            # Simply check if we have a cursor
            if not self.cursor:
                raise Exception("No database cursor available. Please ensure database is connected.")
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except mysql.connector.Error as err:
            print(f"Query execution error: {err}")
            raise err
    
    def fetchone(self):
        """Fetch one result"""
        if not self.cursor:
            raise Exception("No cursor available - query may not have been executed")
        try:
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Fetchone error: {err}")
            raise err
    
    def fetchall(self):
        """Fetch all results"""
        if not self.cursor:
            raise Exception("No cursor available - query may not have been executed")
        try:
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Fetchall error: {err}")
            raise err
    
    def commit(self):
        """Commit transaction"""
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        """Rollback transaction"""
        if self.connection:
            self.connection.rollback()
    
    def close(self):
        """Close connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed")
    
    def test_connection(self):
        """Test if connection is active"""
        try:
            self.connection.ping(reconnect=True)
            return True
        except:
            return False

# Global database instance
db = SimpleDBConnection()

def get_db_connection():
    """Get or create database connection"""
    global db
    
    # Check if we have connection info in session
    if 'db_config' in session:
        config = session['db_config']
        # Always check and reconnect if needed
        if not db.connection or not db.connection.is_connected():
            print(f"[DB] Connecting to database: {config.get('database')} at {config.get('host')}")
            success = db.connect(
                host=config.get('host', 'localhost'),
                user=config.get('user'),
                password=config.get('password'),
                database=config.get('database'),
                port=config.get('port', 3306)
            )
            if not success:
                raise Exception("Failed to connect to database")
        else:
            # Ping to keep connection alive
            try:
                db.connection.ping(reconnect=True)
            except:
                print("[DB] Connection lost, reconnecting...")
                db.connect(
                    host=config.get('host', 'localhost'),
                    user=config.get('user'),
                    password=config.get('password'),
                    database=config.get('database'),
                    port=config.get('port', 3306)
                )
    else:
        print("[DB] No database configuration in session")
    
    return db

def init_db_tables():
    """Initialize database tables if they don't exist"""
    db_conn = get_db_connection()
    if not db_conn.connection:
        return False
    
    try:
        # Users table
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Categories table
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS Categories (
                category_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                type ENUM('income', 'expense') NOT NULL,
                parent_id INT DEFAULT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (parent_id) REFERENCES Categories(category_id) ON DELETE SET NULL
            )
        """)
        
        # Accounts table
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS Accounts (
                account_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                account_name VARCHAR(100) NOT NULL,
                account_type ENUM('checking', 'savings', 'credit_card', 'investment', 'loan', 'other') NOT NULL,
                balance DECIMAL(12, 2) DEFAULT 0.00,
                currency VARCHAR(3) DEFAULT 'USD',
                institution VARCHAR(100),
                account_number VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            )
        """)
        
        # Transactions table
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS Transactions (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                account_id INT NOT NULL,
                category_id INT,
                transaction_date DATE NOT NULL,
                amount DECIMAL(12, 2) NOT NULL,
                transaction_type ENUM('income', 'expense', 'transfer') NOT NULL,
                description TEXT,
                reference_number VARCHAR(100),
                is_recurring BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE SET NULL
            )
        """)
        
        # Transaction Splits table
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS TransactionSplits (
                split_id INT AUTO_INCREMENT PRIMARY KEY,
                transaction_id INT NOT NULL,
                category_id INT NOT NULL,
                amount DECIMAL(12, 2) NOT NULL,
                description TEXT,
                FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
            )
        """)
        
        # Budgets table
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS Budgets (
                budget_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                category_id INT NOT NULL,
                budget_amount DECIMAL(12, 2) NOT NULL,
                period_type ENUM('monthly', 'quarterly', 'yearly') NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
            )
        """)
        
        # Financial Goals table
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS FinancialGoals (
                goal_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                goal_name VARCHAR(200) NOT NULL,
                goal_type ENUM('savings', 'debt_payment', 'investment', 'other') NOT NULL,
                target_amount DECIMAL(12, 2) NOT NULL,
                current_amount DECIMAL(12, 2) DEFAULT 0.00,
                target_date DATE,
                description TEXT,
                is_achieved BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            )
        """)
        
        db_conn.commit()
        print("All tables created successfully")
        return True
        
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
        db_conn.rollback()
        return False