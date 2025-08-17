from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, current_app, has_request_context
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.db_manager import DatabaseManager

# Global database instance - initialize once
db = SQLAlchemy()
engine = None
db_session = None
Base = None
_app_initialized = False

def init_app_db(app):
    """Initialize database with app (called once at startup)"""
    global _app_initialized
    
    if not _app_initialized:
        # Set a dummy URI to satisfy SQLAlchemy
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dummy:dummy@localhost/dummy'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        _app_initialized = True

def init_dynamic_db(app):
    """Initialize database with dynamic connection"""
    global db, engine, db_session, Base
    
    # Ensure app is initialized
    init_app_db(app)
    
    # Check if we have connection info in session
    if not has_request_context():
        return False
        
    conn_info = DatabaseManager.get_connection_info()
    
    if conn_info:
        # Create connection string from session data
        conn_string = DatabaseManager.create_connection_string(
            host=conn_info['host'],
            user=conn_info['user'],
            password=conn_info['password'],
            database=conn_info['database'],
            port=conn_info.get('port', 3306)
        )
        
        # Create engine with the actual connection
        engine = create_engine(conn_string)
        db_session = scoped_session(sessionmaker(bind=engine))
        
        # Update the engine in the db instance
        with app.app_context():
            db.session.remove()
            db.session.configure(bind=engine)
        
        # Import models to ensure they're registered
        from models import User, Category, Account, Transaction, TransactionSplit, Budget, FinancialGoal
        
        return True
    
    return False

def get_dynamic_db():
    """Get the current database instance"""
    global db
    return db

def get_db_session():
    """Get the current database session"""
    global db_session
    return db_session

def close_db_session():
    """Close the database session"""
    global db_session
    if db_session:
        db_session.remove()